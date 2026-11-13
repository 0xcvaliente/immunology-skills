#!/usr/bin/env python3
"""First-pass QC for VHH / VH domains: IMGT regions, hallmark residues, cysteines,
sequence liabilities, charge and size.  Standard library only (Python 3.9+).

    vhh_qc.py SEQ_OR_FILE [...]                  # FASTA, CSV/TSV, or raw sequences
    vhh_qc.py designs.csv --annotate -o qc.csv   # add qc_* columns to a design table
    vhh_qc.py seqs.fasta --numbering anarcii     # exact IMGT numbering (pip install anarcii)

Segmentation is a documented heuristic: it anchors on the conserved Cys23, Trp41,
Cys104 and the FR4 tail, and was checked against ANARCII (see references/vhh.md for
the validation numbers and known limits).  It reads one VH/VHH domain; a sequence it
cannot place is reported as such, never guessed.  Positions in the output are raw
1-based indices into the input sequence, plus the region they fall in; they are not
IMGT or Kabat numbers.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import sys

STANDARD = set("ACDEFGHIKLMNPQRSTVWY")

# ---------------------------------------------------------------- segmentation
FR2_STRICT = re.compile(r"W[VIFYLAMGCT][RKQHLEPAT][QRKELVPAT]")  # IMGT Trp41 + positions 42-44
FR2_LOOSE = re.compile(r"W[A-Z]{3}")
FR3_MOTIF = re.compile(r"[RKQ][FVAL][TAIVS][ILMVF]")            # R-F-T-I of IMGT 74-77
FR4_TAIL = re.compile(r"[A-Z][GS][A-Z]G[A-Z]{3}[TS]VS")         # IMGT 118-127; residue 118 may be W/R/H/F/Y/I/L, 119 G/S
FR4_LOOSE = re.compile(r"[WRH]G[A-Z]G[TAIS]")
LIGHT_CHAIN_SIGNATURE = re.compile(r"[RK]FSGS")                 # FR3 of kappa/lambda, absent from VH/VHH

REGIONS = ("FR1", "CDR1", "FR2", "CDR2", "FR3", "CDR3", "FR4")
IMGT_RANGES = {"FR1": (1, 26), "CDR1": (27, 38), "FR2": (39, 55), "CDR2": (56, 65),
               "FR3": (66, 104), "CDR3": (105, 117), "FR4": (118, 128)}
CONVENTIONAL_HALLMARKS = ("V", "G", "L", "W")                    # IMGT 42, 49, 50, 52 in a conventional VH


def segment_vh(seq):
    """Place IMGT regions on one VH/VHH domain by anchoring on conserved residues.

    Returns (labels, info).  labels[i] is the region of residue i ('ext' before the
    domain, 'tail' after FR4); labels is None when the sequence cannot be placed, and
    info['reason'] says why.  info also carries the anchor indices.
    """
    s = seq
    found = None
    for pattern in (FR2_STRICT, FR2_LOOSE):
        for m in re.finditer("C", s):
            i = m.start()
            if i > 45:                                    # Cys23 sits within ~40 residues of the N-terminus
                break
            for j in range(i + 9, min(i + 21, len(s) - 3)):
                if pattern.match(s, j):
                    found = (i, j)
                    break
            if found:
                break
        if found:
            break
    if not found:
        return None, {"reason": "no Cys23 with a Trp41 10-18 residues downstream (not a VH/VHH domain, or Cys23 is mutated)"}
    c23, w41 = found
    c104 = next((k for k in range(w41 + 54, min(w41 + 69, len(s))) if s[k] == "C"), None)
    if c104 is None:
        return None, {"reason": "no Cys104 where a VH/VHH FR3 ends (truncated, or Cys104 is mutated)"}
    if c104 + 1 < len(s) and s[c104 + 1] == "C":      # '...YCC' at the end of FR3: the second Cys is Cys104
        c104 += 1
    w118 = None
    for rx in (FR4_TAIL, FR4_LOOSE):
        hits = [m.start() for m in re.finditer("(?=(%s))" % rx.pattern, s) if m.start() >= c104 + 2]
        if hits:
            w118 = hits[-1]
            break
    if w118 is None:
        return None, {"reason": "no FR4 (G-x-G ... TVS) after Cys104 (truncated, or not a VH/VHH domain)"}
    fr3 = c104 - 37                                   # FR3 is 38 residues in nearly all VH/VHH
    for k in range(max(0, c104 - 35), c104 - 24):     # unless an insertion moves the R-F-T-I motif
        if FR3_MOTIF.match(s, k):
            fr3 = k - 8
            break
    if not (c23 + 4 < w41 - 2 < w41 + 15 < fr3 < c104 < w118):
        return None, {"reason": "conserved anchors are out of order (not a single VH/VHH domain)"}
    if LIGHT_CHAIN_SIGNATURE.search(s[fr3:c104 + 1]):
        return None, {"reason": "FR3 carries a light-chain signature (R-F-S-G-S); this looks like VL, not VH/VHH"}
    labels = ["ext"] * len(s)
    bounds = [("FR1", max(0, c23 - 22), c23 + 4), ("CDR1", c23 + 4, w41 - 2), ("FR2", w41 - 2, w41 + 15),
              ("CDR2", w41 + 15, fr3), ("FR3", fr3, c104 + 1), ("CDR3", c104 + 1, w118),
              ("FR4", w118, min(len(s), w118 + 11))]
    for name, a, b in bounds:
        for i in range(a, b):
            labels[i] = name
    for i in range(min(len(s), w118 + 11), len(s)):
        labels[i] = "tail"
    return labels, {"c23": c23, "w41": w41, "c104": c104, "w118": w118, "method": "heuristic"}


def segment_anarcii(seqs, gpu=False, min_score=25.0):
    """Number sequences with ANARCII (IMGT) and return [(labels, info), ...] in input order.

    ANARCII will number a shark VNAR as a heavy chain, only with a much lower score: in four
    PDB-derived sets every heavy-chain domain scored 26.2 or more and the two VNARs scored
    17.9 and 19.5, so scores below min_score are reported as unplaced.  The floor is empirical.
    """
    try:
        from anarcii import Anarcii
    except ImportError:
        sys.exit("anarcii is not installed: pip install anarcii (or use the default heuristic numbering)")
    model = Anarcii(seq_type="antibody", cpu=not gpu, verbose=False)
    results = model.number(list(seqs))
    out = []
    for seq, res in zip(seqs, results.values()):
        numbering = res.get("numbering")
        if res.get("error") or not numbering:
            out.append((None, {"reason": "ANARCII could not number it: %s" % res.get("error")}))
            continue
        labels = ["ext"] * len(seq)
        k = res.get("query_start", 0)
        last = k
        info = {"method": "anarcii", "chain_type": res.get("chain_type"), "score": round(float(res.get("score", 0.0)), 1)}
        for (pos, icode), aa in numbering:
            if aa == "-":
                continue
            name = next((r for r, (a, b) in IMGT_RANGES.items() if a <= pos <= b), "tail")
            if k < len(seq):
                labels[k] = name
                if aa == "C" and icode.strip() == "" and pos in (23, 104):
                    info["c23" if pos == 23 else "c104"] = k
            last = k
            k += 1
        for i in range(last + 1, len(seq)):
            labels[i] = "tail"
        if info["chain_type"] != "H":
            out.append((None, {"reason": "ANARCII calls this a %s chain, not a heavy-chain variable domain" % info["chain_type"], **info}))
            continue
        if info["score"] < min_score:
            out.append((None, {"reason": "ANARCII score %.1f is below %.1f: numbered as a heavy chain with low confidence (for example a shark VNAR)" % (info["score"], min_score), **info}))
            continue
        out.append((labels, info))
    return out


def regions_from_labels(seq, labels):
    return {r: "".join(seq[i] for i, lab in enumerate(labels) if lab == r) for r in REGIONS}


def hallmarks(seq, labels, info):
    """Residues at IMGT 42, 49, 50, 52 (FR2 'VHH tetrad'), or None if unplaced."""
    if "w41" in info:
        w = info["w41"]
        idx = (w + 1, w + 8, w + 9, w + 11)
    else:  # ANARCII path: FR2 starts at IMGT 39, so 42/49/50/52 are FR2 offsets 3/10/11/13 -> only valid without gaps
        fr2 = [i for i, lab in enumerate(labels) if lab == "FR2"]
        if len(fr2) != 17:
            return None
        idx = (fr2[3], fr2[10], fr2[11], fr2[13])
    return "".join(seq[i] for i in idx)


# ------------------------------------------------------------------ liabilities
# (name, regex, severity in a CDR, severity elsewhere in the domain, note)
RULES = [
    ("NG", r"(?=(NG))", "high", "medium", "Asn-Gly: fastest deamidation"),
    ("DG", r"(?=(DG))", "high", "medium", "Asp-Gly: isomerisation"),
    ("N-glyc", r"(?=(N[^P][ST]))", "high", "high", "N-X-S/T sequon (X is not Pro): N-glycosylation in eukaryotic hosts"),
    ("DP", r"(?=(DP))", "medium", "low", "Asp-Pro: acid-labile bond"),
    ("NS", r"(?=(NS))", "medium", "low", "Asn-Ser: deamidation"),
    ("NH", r"(?=(NH))", "medium", "low", "Asn-His: deamidation"),
    ("NT", r"(?=(NT))", "low", "info", "Asn-Thr: slower deamidation"),
    ("NN", r"(?=(NN))", "low", "info", "Asn-Asn: slower deamidation"),
    ("DS", r"(?=(DS))", "low", "info", "Asp-Ser: slower isomerisation"),
    ("DT", r"(?=(DT))", "low", "info", "Asp-Thr: slower isomerisation"),
    ("DD", r"(?=(DD))", "low", "info", "Asp-Asp: slower isomerisation"),
    ("DH", r"(?=(DH))", "low", "info", "Asp-His: slower isomerisation"),
    ("M-ox", r"(?=(M))", "medium", "info", "Met: oxidation (matters when solvent-exposed)"),
    ("W-ox", r"(?=(W))", "low", "info", "Trp: oxidation (matters when solvent-exposed)"),
    ("hydrophobic-run", r"[AILMFWVY]{6,}", "medium", "medium", "6+ consecutive hydrophobic residues: aggregation"),
    ("polybasic", r"[KR]{3,}", "low", "low", "3+ consecutive Lys/Arg: proteolysis, charge patch"),
]
SEVERITY_ORDER = {"high": 3, "medium": 2, "low": 1, "info": 0}


def scan_liabilities(seq, labels):
    hits = []
    for name, pattern, sev_cdr, sev_fr, note in RULES:
        for m in re.finditer(pattern, seq):
            start = m.start()
            text = m.group(1) if m.groups() else m.group(0)
            region = labels[start] if labels else "unknown"
            if region in ("ext", "tail"):
                continue                                  # tags and linkers are not part of the binder
            in_cdr = region.startswith("CDR")
            sev = sev_cdr if in_cdr else sev_fr
            hits.append({"motif": name, "text": text, "pos": start + 1, "region": region,
                         "severity": sev, "note": note})
    hits.sort(key=lambda h: (-SEVERITY_ORDER[h["severity"]], h["pos"]))
    return hits


# ---------------------------------------------------------------- biophysics
RESIDUE_MASS = {"G": 57.0519, "A": 71.0788, "S": 87.0782, "P": 97.1167, "V": 99.1326, "T": 101.1051,
                "C": 103.1388, "L": 113.1594, "I": 113.1594, "N": 114.1038, "D": 115.0886, "Q": 128.1307,
                "K": 128.1741, "E": 129.1155, "M": 131.1926, "H": 137.1411, "F": 147.1766, "R": 156.1875,
                "Y": 163.1760, "W": 186.2132}
KYTE_DOOLITTLE = {"A": 1.8, "R": -4.5, "N": -3.5, "D": -3.5, "C": 2.5, "Q": -3.5, "E": -3.5, "G": -0.4, "H": -3.2,
                  "I": 4.5, "L": 3.8, "K": -3.9, "M": 1.9, "F": 2.8, "P": -1.6, "S": -0.8, "T": -0.7, "W": -0.9,
                  "Y": -1.3, "V": 4.2}
PKA_POS = {"Nterm": 8.6, "K": 10.8, "R": 12.5, "H": 6.5}        # EMBOSS pKa set; +/-0.3 is realistic
PKA_NEG = {"Cterm": 3.6, "D": 3.9, "E": 4.1, "C": 8.5, "Y": 10.1}


def net_charge(seq, ph):
    pos = 1.0 / (1.0 + 10 ** (ph - PKA_POS["Nterm"]))
    neg = 1.0 / (1.0 + 10 ** (PKA_NEG["Cterm"] - ph))
    for aa in seq:
        if aa in PKA_POS:
            pos += 1.0 / (1.0 + 10 ** (ph - PKA_POS[aa]))
        elif aa in PKA_NEG:
            neg += 1.0 / (1.0 + 10 ** (PKA_NEG[aa] - ph))
    return pos - neg


def isoelectric_point(seq):
    lo, hi = 0.0, 14.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if net_charge(seq, mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def biophysics(seq):
    seq = "".join(a for a in seq if a in STANDARD)    # X, B, Z ... are reported as invalid_residues, not computed on
    if not seq:
        return {}
    return {"mw_kda": round((sum(RESIDUE_MASS[a] for a in seq) + 18.0153) / 1000.0, 2),
            "pI": round(isoelectric_point(seq), 2),
            "charge_ph74": round(net_charge(seq, 7.4), 2),
            "charge_ph65": round(net_charge(seq, 6.5), 2),
            "gravy": round(sum(KYTE_DOOLITTLE[a] for a in seq) / len(seq), 3)}


# ------------------------------------------------------------------- one record
def clean(raw):
    s = re.sub(r"\s+", "", raw or "").upper().rstrip("*")
    s = s.replace("-", "")
    bad = sorted({c for c in s if c not in STANDARD})
    return s, bad


def analyse_one(name, raw, labels_info):
    seq, bad = clean(raw)
    labels, info = labels_info if labels_info else (None, {"reason": "empty sequence"})
    rec = {"id": name, "length": len(seq), "invalid_residues": "".join(bad), "method": info.get("method", "-")}
    flags = []
    if bad:
        flags.append("invalid_residues:" + "".join(bad))
    if len(seq) > 160:
        flags.append("long_input:%daa (tags, linkers or tandem domains? one domain is parsed)" % len(seq))
    placed = labels is not None
    rec["status"] = "ok" if placed else "unplaced: " + info.get("reason", "unknown")
    regs = regions_from_labels(seq, labels) if placed else {r: "" for r in REGIONS}
    for r in REGIONS:
        rec[r.lower()] = regs[r]
    rec["cdr_lengths"] = "/".join(str(len(regs[r])) for r in ("CDR1", "CDR2", "CDR3")) if placed else ""
    rec["cdr_total_len"] = sum(len(regs[r]) for r in ("CDR1", "CDR2", "CDR3")) if placed else None
    # hallmarks
    hm = hallmarks(seq, labels, info) if placed else None
    rec["hallmarks"] = hm or ""
    if hm:
        matches = sum(1 for a, b in zip(hm, CONVENTIONAL_HALLMARKS) if a == b)
        rec["hallmark_class"] = "VHH-type" if matches <= 1 else ("VH-type" if matches == 4 else "mixed")
    else:
        rec["hallmark_class"] = ""
    # cysteines
    cys = [i for i, a in enumerate(seq) if a == "C"]
    domain_cys = [i for i in cys if labels and labels[i] not in ("ext", "tail")] if placed else cys
    canon = {info.get("c23"), info.get("c104")} if placed and "c23" in info else set()
    extras = [i for i in domain_cys if i not in canon] if canon else []
    rec["cys"] = len(domain_cys)
    rec["extra_cys"] = ",".join("%s@%d" % (labels[i], i + 1) for i in extras)
    if len(domain_cys) % 2:
        flags.append("odd_cys:%d (free thiol)" % len(domain_cys))
    elif extras:
        flags.append("extra_cys:%d (needs a disulfide partner, as in some camelid VHHs)" % len(extras))
    elif placed and len(domain_cys) < 2:
        flags.append("missing_canonical_cys")
    # liabilities
    hits = scan_liabilities(seq, labels if placed else None)
    rec["liabilities"] = hits
    rec["liab_high"] = sum(1 for h in hits if h["severity"] == "high")
    rec["liab_medium"] = sum(1 for h in hits if h["severity"] == "medium")
    summary = {}
    for h in hits:
        if h["severity"] in ("high", "medium"):
            key = "%s:%s" % (h["region"] if h["region"].startswith("CDR") else "FR" if h["region"] != "unknown" else "?", h["motif"])
            summary[key] = summary.get(key, 0) + 1
    for key, n in sorted(summary.items()):
        flags.append("%s x%d" % (key, n) if n > 1 else key)
    # biophysics on the domain (tags and N-terminal extensions removed when placed)
    dom = "".join(a for a, lab in zip(seq, labels) if lab not in ("ext", "tail")) if placed else seq
    rec.update(biophysics(dom))
    his = [i for i, a in enumerate(seq) if a == "H" and (not placed or labels[i] not in ("ext", "tail"))]
    rec["his_total"] = len(his)
    rec["his_cdr"] = sum(1 for i in his if placed and labels[i].startswith("CDR"))
    rec["flags"] = flags
    rec["sequence"] = seq
    return rec


# ----------------------------------------------------------------------- input
def read_records(inputs, seq_col, id_col):
    """Yield (id, sequence, source_row_or_None) from files or raw sequences."""
    out = []
    for item in inputs:
        if os.path.isfile(item):
            with open(item, newline="") as fh:
                head = fh.read(4096)
                fh.seek(0)
                if head.lstrip().startswith(">"):
                    name, buf = None, []
                    for line in fh:
                        line = line.strip()
                        if line.startswith(">"):
                            if name is not None:
                                out.append((name, "".join(buf), None))
                            name, buf = line[1:].split()[0] if line[1:].split() else "seq%d" % (len(out) + 1), []
                        elif line:
                            buf.append(line)
                    if name is not None:
                        out.append((name, "".join(buf), None))
                else:
                    delim = "\t" if head.count("\t") > head.count(",") else ","
                    reader = csv.DictReader(fh, delimiter=delim)
                    cols = reader.fieldnames or []
                    sc = seq_col or next((c for c in cols if c.lower() in ("sequence", "seq", "aa_sequence")), None)
                    ic = id_col or next((c for c in cols if c.lower() in ("name", "id", "design", "design_id")), None)
                    if sc not in cols:
                        sys.exit("%s: no sequence column (columns: %s); pass --seq-col" % (item, ", ".join(cols)))
                    for n, row in enumerate(reader, 1):
                        out.append(((row.get(ic) if ic else None) or "row%d" % n, row[sc], row))
        elif re.fullmatch(r"[A-Za-z\-\s*]{20,}", item):
            out.append(("seq%d" % (len(out) + 1), item, None))
        else:
            sys.exit("not a file or a sequence: %r" % item[:40])
    return out


# ---------------------------------------------------------------------- output
ANNOTATE_COLS = ["status", "cdr1", "cdr2", "cdr3", "cdr_lengths", "cdr_total_len", "hallmarks", "hallmark_class",
                 "cys", "extra_cys", "mw_kda", "pI", "charge_ph74", "charge_ph65", "gravy", "his_total", "his_cdr",
                 "liab_high", "liab_medium"]


def render_text(rec):
    L = ["%s  (%d aa)  %s" % (rec["id"], rec["length"], rec["status"])]
    if rec["status"] == "ok":
        L.append("  FR1 %s | CDR1 %s | FR2 %s" % (rec["fr1"], rec["cdr1"], rec["fr2"]))
        L.append("  CDR2 %s | FR3 %s" % (rec["cdr2"], rec["fr3"]))
        L.append("  CDR3 %s | FR4 %s" % (rec["cdr3"], rec["fr4"]))
        L.append("  CDR lengths %s (total %s) | hallmarks 42/49/50/52 = %s (%s) | Cys %d%s"
                 % (rec["cdr_lengths"], rec["cdr_total_len"], rec["hallmarks"] or "?", rec["hallmark_class"] or "?",
                    rec["cys"], " + extra " + rec["extra_cys"] if rec["extra_cys"] else ""))
    if "mw_kda" in rec:
        L.append("  %.2f kDa | pI %.2f | charge pH7.4 %+.1f, pH6.5 %+.1f | GRAVY %.2f | His %d (in CDRs %d)"
                 % (rec["mw_kda"], rec["pI"], rec["charge_ph74"], rec["charge_ph65"], rec["gravy"], rec["his_total"], rec["his_cdr"]))
    shown = [h for h in rec["liabilities"] if h["severity"] in ("high", "medium")]
    low = sum(1 for h in rec["liabilities"] if h["severity"] == "low")
    if shown or low:
        L.append("  liabilities (raw 1-based positions):")
        for h in shown:
            L.append("    %-6s %-15s %-4s at %d (%s)  %s" % (h["severity"], h["motif"], h["text"] if len(h["text"]) < 6 else h["text"][:5] + "+", h["pos"], h["region"], h["note"]))
        if low:
            L.append("    + %d low-severity motifs (use --format json to list)" % low)
    L.append("  flags: " + ("; ".join(rec["flags"]) if rec["flags"] else "none"))
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="FASTA/CSV/TSV files or raw amino-acid sequences")
    ap.add_argument("--seq-col", help="sequence column in CSV/TSV (default: sequence|seq)")
    ap.add_argument("--id-col", help="id column in CSV/TSV (default: name|id)")
    ap.add_argument("--numbering", choices=("heuristic", "anarcii"), default="heuristic")
    ap.add_argument("--gpu", action="store_true", help="let ANARCII use a GPU (default: CPU)")
    ap.add_argument("--min-anarcii-score", type=float, default=25.0, help="with --numbering anarcii, treat a lower ANARCII score as unplaced (default 25, empirical)")
    ap.add_argument("--format", choices=("text", "tsv", "json"), help="default: text for <=12 records, else tsv")
    ap.add_argument("--annotate", action="store_true", help="CSV in, CSV out: input rows plus qc_* columns")
    ap.add_argument("-o", "--output", help="output file (default: stdout)")
    args = ap.parse_args(argv)

    records = read_records(args.inputs, args.seq_col, args.id_col)
    if not records:
        sys.exit("no sequences found")
    cleaned = [clean(r[1])[0] for r in records]
    if args.numbering == "anarcii":
        placed = segment_anarcii(cleaned, gpu=args.gpu, min_score=args.min_anarcii_score)
    else:
        placed = [segment_vh(s) if s else (None, {"reason": "empty sequence"}) for s in cleaned]
    results = [analyse_one(r[0], r[1], p) for r, p in zip(records, placed)]

    out = open(args.output, "w", newline="") if args.output else sys.stdout
    try:
        if args.annotate:
            rows = [r[2] for r in records]
            if any(row is None for row in rows):
                sys.exit("--annotate needs a CSV/TSV input with a sequence column")
            fields = list(rows[0].keys()) + ["qc_" + c for c in ANNOTATE_COLS] + ["qc_flags"]
            w = csv.DictWriter(out, fieldnames=fields)
            w.writeheader()
            for row, rec in zip(rows, results):
                row = dict(row)
                for c in ANNOTATE_COLS:
                    row["qc_" + c] = rec.get(c, "")
                row["qc_flags"] = "; ".join(rec["flags"])
                w.writerow(row)
            return 0
        fmt = args.format or ("text" if len(results) <= 12 else "tsv")
        if fmt == "json":
            json.dump(results, out, indent=1)
            out.write("\n")
        elif fmt == "tsv":
            cols = ["id", "length", "status"] + ANNOTATE_COLS[1:] + ["flags"]
            w = csv.writer(out, delimiter="\t")
            w.writerow(cols)
            for rec in results:
                w.writerow([("; ".join(rec["flags"]) if c == "flags" else rec.get(c, "")) for c in cols])
        else:
            out.write("\n\n".join(render_text(r) for r in results) + "\n")
    finally:
        if args.output:
            out.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
