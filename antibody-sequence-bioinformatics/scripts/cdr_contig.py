#!/usr/bin/env python3
"""Turn a VHH structure into residue ranges and a contig for CDR redesign.

    cdr_contig.py 1ZVY.cif --chain A --target-chain B                 # redesign CDR3, native length
    cdr_contig.py 1ZVY.pdb --chain A --target-chain B --design CDR3 --length CDR3=16-24
    cdr_contig.py nb.pdb --chain H --design CDR1,CDR2,CDR3 --style rfdiffusion

Why a script: IMGT positions are not PDB residue numbers, and a contig must use the
file's own numbering.  This reads the structure (PDB or mmCIF, standard library only),
finds the IMGT CDRs on the chain's sequence with vhh_qc.py, maps them to the residue
numbers in the file, and drops any residue whose backbone (N, CA, C) is incomplete,
because a contig that names an unresolved residue fails inside the design tool.

The output string follows the participant-guide syntax (comma separated, '/0' chain
break) or RFdiffusion syntax.  Both are conventions of the tool you paste them into:
check the tool's own documentation and the numbering it expects (author numbering,
which is what these files use) before relying on it.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vhh_qc  # noqa: E402

THREE_TO_ONE = {"ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q", "GLU": "E", "GLY": "G",
                "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P", "SER": "S",
                "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V", "MSE": "M"}
BACKBONE = {"N", "CA", "C"}


def parse_structure(path):
    """Return {chain: [residue, ...]}; residue = dict(num, icode, name, atoms:set)."""
    with open(path) as fh:
        text = fh.read()
    if "_atom_site." in text:
        return _parse_mmcif(text)
    return _parse_pdb(text)


def _add(chains, order, chain, num, icode, name, atom, xyz=None):
    key = (chain, num, icode)
    if key not in order:
        order[key] = {"num": num, "icode": icode, "name": name, "atoms": set(), "xyz": {}}
        chains.setdefault(chain, []).append(order[key])
    order[key]["atoms"].add(atom)
    if xyz is not None:
        order[key]["xyz"][atom] = xyz


def _parse_pdb(text):
    chains, order = {}, {}
    for line in text.splitlines():
        if line.startswith("ENDMDL"):
            break
        if not line.startswith(("ATOM", "HETATM")):
            continue
        name = line[17:20].strip()
        if line.startswith("HETATM") and name != "MSE":
            continue
        if line[16] not in " A":                       # first alternate location only
            continue
        _add(chains, order, line[21], int(line[22:26]), line[26].strip(), name, line[12:16].strip(),
             (float(line[30:38]), float(line[38:46]), float(line[46:54])))
    return chains


def _parse_mmcif(text):
    chains, order = {}, {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip() == "loop_" and i + 1 < len(lines) and lines[i + 1].startswith("_atom_site."):
            cols = []
            i += 1
            while i < len(lines) and lines[i].startswith("_atom_site."):
                cols.append(lines[i].strip().split(".", 1)[1])
                i += 1
            ix = {c: n for n, c in enumerate(cols)}
            seq_col = "auth_seq_id" if "auth_seq_id" in ix else "label_seq_id"
            chain_col = "auth_asym_id" if "auth_asym_id" in ix else "label_asym_id"
            atom_col = "label_atom_id" if "label_atom_id" in ix else "auth_atom_id"
            comp_col = "label_comp_id" if "label_comp_id" in ix else "auth_comp_id"
            first_model = None
            while i < len(lines) and not lines[i].startswith(("#", "loop_", "_")):
                tok = re.findall(r"'[^']*'|\"[^\"]*\"|\S+", lines[i])
                i += 1
                if len(tok) < len(cols):
                    continue
                if tok[ix["group_PDB"]] == "HETATM" and tok[ix[comp_col]] != "MSE":
                    continue
                model = tok[ix["pdbx_PDB_model_num"]] if "pdbx_PDB_model_num" in ix else "1"
                first_model = first_model or model
                if model != first_model:
                    break
                alt = tok[ix["label_alt_id"]] if "label_alt_id" in ix else "."
                if alt not in (".", "?", "A"):
                    continue
                icode = tok[ix["pdbx_PDB_ins_code"]] if "pdbx_PDB_ins_code" in ix else "?"
                xyz = None
                if "Cartn_x" in ix:
                    try:
                        xyz = (float(tok[ix["Cartn_x"]]), float(tok[ix["Cartn_y"]]), float(tok[ix["Cartn_z"]]))
                    except ValueError:
                        xyz = None
                _add(chains, order, tok[ix[chain_col]], int(tok[ix[seq_col]]), "" if icode in ("?", ".") else icode,
                     tok[ix[comp_col]], tok[ix[atom_col]].strip("'\""), xyz)
            break
        i += 1
    return chains


def residue_label(chain, r):
    return "%s%d%s" % (chain, r["num"], r["icode"])


def contiguous(a, b):
    return a["icode"] == "" and b["icode"] == "" and b["num"] == a["num"] + 1


def segments(chain, residues):
    """Group resolved residues into runs of consecutive numbers -> 'A2-96'."""
    out, run = [], []
    for r in residues:
        if run and not contiguous(run[-1], r):
            out.append(run)
            run = []
        run.append(r)
    if run:
        out.append(run)
    return [(residue_label(chain, g[0]), residue_label(chain, g[-1])) for g in out]


def fmt_range(chain, first, last):
    return first if first == last else "%s-%s" % (first, last[len(chain):] if last.startswith(chain) else last)


def parse_lengths(items, designed, native):
    lengths = {}
    for it in items or []:
        m = re.fullmatch(r"(CDR[123])=(\d+)(?:-(\d+))?", it.upper())
        if not m:
            sys.exit("--length expects CDR3=20 or CDR3=16-24, got %r" % it)
        lo, hi = int(m.group(2)), int(m.group(3) or m.group(2))
        if lo > hi:
            sys.exit("--length %s: low > high" % it)
        lengths[m.group(1)] = (lo, hi)
    for d in designed:
        lengths.setdefault(d, (native[d], native[d]))
    return lengths


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("structure", help="PDB or mmCIF file")
    ap.add_argument("--chain", required=True, help="chain id of the VHH (author chain id)")
    ap.add_argument("--target-chain", help="comma-separated chain ids kept fixed as the target")
    ap.add_argument("--design", default="CDR3", help="CDR1,CDR2,CDR3 subset or 'all' (default CDR3)")
    ap.add_argument("--length", action="append", help="new loop length, e.g. CDR3=20 or CDR3=16-24 (default: native length)")
    ap.add_argument("--style", choices=("guide", "rfdiffusion"), default="guide")
    ap.add_argument("--numbering", choices=("heuristic", "anarcii"), default="heuristic")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)

    chains = parse_structure(args.structure)
    if args.chain not in chains:
        sys.exit("chain %r not found; chains in file: %s" % (args.chain, ", ".join(sorted(chains))))
    res = [r for r in chains[args.chain] if "CA" in r["atoms"] and r["name"] in THREE_TO_ONE]
    unresolved = [r for r in res if not BACKBONE <= r["atoms"]]
    seq = "".join(THREE_TO_ONE[r["name"]] for r in res)
    if args.numbering == "anarcii":
        labels, info = vhh_qc.segment_anarcii([seq])[0]
    else:
        labels, info = vhh_qc.segment_vh(seq)
    if labels is None:
        sys.exit("chain %s is not placed as a VH/VHH domain: %s" % (args.chain, info.get("reason")))

    regs = {name: [i for i, lab in enumerate(labels) if lab == name] for name in vhh_qc.REGIONS}
    native = {k: len(regs[k]) for k in ("CDR1", "CDR2", "CDR3")}
    designed = ["CDR1", "CDR2", "CDR3"] if args.design.lower() == "all" else [d.strip().upper() for d in args.design.split(",")]
    if any(d not in native for d in designed):
        sys.exit("--design must be CDR1, CDR2, CDR3 (comma separated) or 'all'")
    lengths = parse_lengths(args.length, designed, native)

    # fixed segments and new loops, in chain order
    domain = [i for i, lab in enumerate(labels) if lab in vhh_qc.REGIONS]
    tokens, run, skipped = [], [], []

    def flush():
        nonlocal run
        for first, last in segments(args.chain, run):
            tokens.append(("fixed", fmt_range(args.chain, first, last)))
        run = []

    prev_region = None
    for i in domain:
        reg = labels[i]
        if reg in designed:
            if prev_region != reg:
                flush()
                lo, hi = lengths[reg]
                tokens.append(("new", str(lo) if lo == hi else "%d-%d" % (lo, hi)))
            prev_region = reg
            continue
        prev_region = reg
        if BACKBONE <= res[i]["atoms"]:
            run.append(res[i])
        else:
            skipped.append(residue_label(args.chain, res[i]))
            flush()
    flush()

    gaps = [(residue_label(args.chain, a), residue_label(args.chain, b)) for a, b in zip(res, res[1:])
            if not contiguous(a, b) and labels[res.index(a)] in vhh_qc.REGIONS and labels[res.index(b)] in vhh_qc.REGIONS]
    inscodes = [residue_label(args.chain, r) for r in res if r["icode"]]

    target_tokens = []
    for tc in [c for c in (args.target_chain or "").split(",") if c]:
        if tc not in chains:
            sys.exit("target chain %r not found" % tc)
        tres = [r for r in chains[tc] if BACKBONE <= r["atoms"] and r["name"] in THREE_TO_ONE]
        target_tokens += [fmt_range(tc, a, b) for a, b in segments(tc, tres)]

    if args.style == "guide":      # B1-129, /0, A2-96, 20, A117-125
        parts = []
        for t in target_tokens:
            parts += [t, "/0"]
        contig = ", ".join(parts + [t for _, t in tokens])
    else:                          # [B1-129/0 A2-96/20-20/A117-125]
        binder = "/".join(("%s-%s" % (t, t) if k == "new" and "-" not in t else t) for k, t in tokens)
        contig = "[" + " ".join([t + "/0" for t in target_tokens] + [binder]) + "]"

    report = {"structure": os.path.basename(args.structure), "chain": args.chain, "residues_with_ca": len(res),
              "numbering_method": info.get("method"), "hallmarks": vhh_qc.hallmarks(seq, labels, info),
              "regions": {}, "designed": designed, "new_lengths": {k: "%d-%d" % v if v[0] != v[1] else str(v[0]) for k, v in lengths.items()},
              "excluded_incomplete_backbone": skipped, "unresolved_in_chain": [residue_label(args.chain, r) for r in unresolved],
              "numbering_gaps_in_domain": gaps, "insertion_codes": inscodes, "contig": contig}
    for name in vhh_qc.REGIONS:
        idx = regs[name]
        if idx:
            report["regions"][name] = {"seq": "".join(seq[i] for i in idx), "first": residue_label(args.chain, res[idx[0]]),
                                       "last": residue_label(args.chain, res[idx[-1]]), "n": len(idx)}
    if args.json:
        json.dump(report, sys.stdout, indent=1)
        print()
        return 0

    print("%s chain %s: %d residues with C-alpha; %s numbering" % (report["structure"], args.chain, len(res), info.get("method")))
    print("hallmarks (IMGT 42/49/50/52): %s" % (report["hallmarks"] or "n/a"))
    for name in vhh_qc.REGIONS:
        if name in report["regions"]:
            r = report["regions"][name]
            mark = "  <- redesigned, new length %s" % report["new_lengths"][name] if name in designed else ""
            print("  %-4s %-26s %s..%s (%d aa)%s" % (name, r["seq"], r["first"], r["last"], r["n"], mark))
    if skipped:
        print("excluded (backbone N/CA/C incomplete): " + ", ".join(skipped))
    if gaps:
        print("WARNING numbering gaps inside the domain at %s: region boundaries may be approximate" % gaps)
    if inscodes:
        print("WARNING insertion codes present (%s): ranges above use plain residue numbers; check how your tool handles them" % ", ".join(inscodes[:6]))
    print("\ncontig (%s style):\n  %s" % (args.style, contig))
    print("\nCheck before pasting: the tool's numbering convention, and that every fixed range is resolved in the file you upload.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
