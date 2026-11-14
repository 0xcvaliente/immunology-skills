#!/usr/bin/env python3
"""Where does a predicted binder touch its target?  Interface contacts, hotspot coverage
and CDR contribution from one or many complex structures (PDB or mmCIF).

    interface_contacts.py design.cif --binder H --target A --hotspots A45,A67,A89
    interface_contacts.py out/*.cif --binder B --target A --hotspots A45,A67 > contacts.tsv   # one row per file

A contact is a heavy-atom pair within --cutoff (distance <= cutoff, default 4.5 A).  This answers the
questions a confidence score cannot: does the design sit on the intended epitope
(hotspot coverage), is the interface made by the CDRs or by framework (a framework-only
interface is a warning sign for a designed VHH), and is it plausibly sized.  It does not
estimate affinity, buried surface area or energetics.

Hotspots are target residue labels as they appear in the file (chain + author number,
e.g. A45; a bare number such as 45 means the first --target chain).  CDR labels come from
vhh_qc.py's IMGT heuristic (or ANARCII with --numbering anarcii) on the binder chain.
Standard library only.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cdr_contig  # noqa: E402
import vhh_qc  # noqa: E402


def heavy_atoms(res):
    for name, xyz in res["xyz"].items():
        if name.lstrip("0123456789")[:1] != "H":
            yield name, xyz


def contact_pairs(binder_res, target_res, cutoff):
    """Residue pairs (i, j) with a heavy-atom pair at distance <= cutoff, found with a cell grid."""
    cell = cutoff
    grid = {}
    for j, r in enumerate(target_res):
        for _, (x, y, z) in heavy_atoms(r):
            grid.setdefault((int(x // cell), int(y // cell), int(z // cell)), []).append((j, x, y, z))
    pairs, atom_pairs = {}, 0
    cut2 = cutoff * cutoff
    for i, r in enumerate(binder_res):
        for _, (x, y, z) in heavy_atoms(r):
            cx, cy, cz = int(x // cell), int(y // cell), int(z // cell)
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        for j, a, b, c in grid.get((cx + dx, cy + dy, cz + dz), ()):
                            if (x - a) ** 2 + (y - b) ** 2 + (z - c) ** 2 <= cut2:
                                pairs.setdefault((i, j), 0)
                                pairs[(i, j)] += 1
                                atom_pairs += 1
    return pairs, atom_pairs


def analyse(path, binder, targets, cutoff, hotspots, numbering):
    chains = cdr_contig.parse_structure(path)
    if binder not in chains:
        raise ValueError("binder chain %r not in %s (chains: %s)" % (binder, os.path.basename(path), ", ".join(sorted(chains))))
    bres = [r for r in chains[binder] if r["name"] in cdr_contig.THREE_TO_ONE and r["xyz"]]
    tres, tlabels = [], []
    for tc in targets:
        if tc not in chains:
            raise ValueError("target chain %r not in %s" % (tc, os.path.basename(path)))
        for r in chains[tc]:
            if r["name"] in cdr_contig.THREE_TO_ONE and r["xyz"]:
                tres.append(r)
                tlabels.append(cdr_contig.residue_label(tc, r))
    seq = "".join(cdr_contig.THREE_TO_ONE[r["name"]] for r in bres)
    labels, info = (vhh_qc.segment_anarcii([seq])[0] if numbering == "anarcii" else vhh_qc.segment_vh(seq))
    pairs, atom_pairs = contact_pairs(bres, tres, cutoff)
    b_in = sorted({i for i, _ in pairs})
    t_in = sorted({j for _, j in pairs})
    out = {"file": os.path.basename(path), "binder_chain": binder, "target_chains": targets, "cutoff": cutoff,
           "binder_residues": len(bres), "contact_residue_pairs": len(pairs), "contact_atom_pairs": atom_pairs,
           "binder_contact_residues": len(b_in), "target_contact_residues": len(t_in),
           "binder_region_known": labels is not None}
    if labels is not None:
        counts = {}
        for i in b_in:
            counts[labels[i]] = counts.get(labels[i], 0) + 1
        out["binder_contacts_by_region"] = counts
        n = max(1, len(b_in))
        out["cdr_fraction"] = round(sum(v for k, v in counts.items() if k.startswith("CDR")) / n, 3)
        out["cdr3_fraction"] = round(counts.get("CDR3", 0) / n, 3)
        out["framework_fraction"] = round(sum(v for k, v in counts.items() if k.startswith("FR")) / n, 3)
    else:
        out["region_note"] = "binder chain not placed as a VH/VHH domain: %s" % info.get("reason", "")
    if hotspots:
        wanted = []
        for h in hotspots:
            wanted.append(h if h[:1].isalpha() else targets[0] + h)
        touched = {tlabels[j] for j in t_in}
        out["hotspots"] = {h: (h in touched) for h in wanted}
        out["hotspots_missing_from_file"] = [h for h in wanted if h not in set(tlabels)]
        out["hotspot_coverage"] = round(sum(out["hotspots"].values()) / len(wanted), 3)
    out["target_contact_labels"] = [tlabels[j] for j in t_in]
    return out


TSV_COLS = ["file", "binder_residues", "contact_residue_pairs", "contact_atom_pairs", "binder_contact_residues", "target_contact_residues",
            "cdr_fraction", "cdr3_fraction", "framework_fraction", "hotspot_coverage"]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("structures", nargs="+")
    ap.add_argument("--binder", required=True, help="binder chain id (author id)")
    ap.add_argument("--target", required=True, help="comma-separated target chain ids")
    ap.add_argument("--cutoff", type=float, default=4.5)
    ap.add_argument("--hotspots", help="comma-separated target residues, e.g. A45,A67 (bare numbers use the first target chain)")
    ap.add_argument("--numbering", choices=("heuristic", "anarcii"), default="heuristic")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    targets = [c for c in args.target.split(",") if c]
    hotspots = [h.strip() for h in (args.hotspots or "").split(",") if h.strip()]
    results = []
    for path in args.structures:
        try:
            results.append(analyse(path, args.binder, targets, args.cutoff, hotspots, args.numbering))
        except ValueError as e:
            sys.exit(str(e))
    if args.json:
        json.dump(results if len(results) > 1 else results[0], sys.stdout, indent=1)
        print()
    elif len(results) > 1:
        print("\t".join(TSV_COLS))
        for r in results:
            print("\t".join(str(r.get(c, "")) for c in TSV_COLS))
    else:
        r = results[0]
        print("%s: binder %s vs target %s, cutoff %.1f A" % (r["file"], r["binder_chain"], ",".join(targets), r["cutoff"]))
        print("  %d binder residues touch %d target residues (%d residue pairs, %d atom pairs)" % (r["binder_contact_residues"], r["target_contact_residues"], r["contact_residue_pairs"], r["contact_atom_pairs"]))
        if r["binder_region_known"]:
            print("  binder contacts by region: %s | CDR %.0f%%, CDR3 %.0f%%, framework %.0f%%" % (r["binder_contacts_by_region"], 100 * r["cdr_fraction"], 100 * r["cdr3_fraction"], 100 * r["framework_fraction"]))
            if r["binder_contact_residues"] and r["cdr_fraction"] < 0.5:
                print("  WARNING less than half of the contacting residues are in CDRs: the interface is largely framework")
        else:
            print("  " + r["region_note"])
        if "hotspots" in r:
            print("  hotspots touched: %d/%d (%.0f%%): %s" % (sum(r["hotspots"].values()), len(r["hotspots"]), 100 * r["hotspot_coverage"],
                                                             ", ".join("%s%s" % (h, "" if v else " (no)") for h, v in r["hotspots"].items())))
            if r["hotspots_missing_from_file"]:
                print("  WARNING hotspot labels not present in the file (check chain and numbering): " + ", ".join(r["hotspots_missing_from_file"]))
        if r["contact_residue_pairs"] == 0:
            print("  WARNING no contacts: the binder is not in contact with the target in this structure")
    return 0


if __name__ == "__main__":
    sys.exit(main())
