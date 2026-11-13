#!/usr/bin/env python3
"""Validate a design submission CSV before it is sent.

    check_submission.py submission.csv --max-designs 10
    check_submission.py submission.csv --max-designs 20 --max-len 250 --json

Format checked (Anthropic x Adaptyv design competition FAQ, retrieved 2026-11-13):
columns name, sequence, molecule_class; row order is the ranking (best first);
molecule_class one of protein | nanobody | scfv | fab_kappa | fab_lambda; a Fab is one
string 'VH:VL'; single-chain length 10-250; designs must be unique.  The task you are
given on the day overrides all of this: pass its limits as flags.

Exit code 1 when there are errors, 0 otherwise (warnings do not fail the check).
Standard library only.  If vhh_qc.py from antibody-sequence-bioinformatics is installed
next to this skill, nanobody rows are also checked for VH/VHH shape.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys

STANDARD = set("ACDEFGHIKLMNPQRSTVWY")
CLASSES = ("protein", "nanobody", "scfv", "fab_kappa", "fab_lambda")
NEAR_DUP_MAX_ROWS = 100
TEXT_COLUMNS = {"notes", "note", "rationale", "description", "method", "methods", "comment", "comments", "summary", "reasoning", "why"}
# A lint for text that talks to the selector instead of describing the design.
ADDRESSING = [
    r"\b(ignore|disregard|override|forget)\b.{0,40}\b(instruction|prompt|rule|criteri|previous)",
    r"\b(you are|as an? (ai|assistant|language model)|system prompt|claude|chatgpt|llm)\b",
    r"\b(please|must|should|always)\b.{0,30}\b(select|accept|choose|pick|prioriti[sz]e|rank|include)\b",
    r"\b(select|pick|choose|prioriti[sz]e)\b.{0,25}\b(this|these|my|our)\b.{0,25}\b(design|sequence|submission|candidate)s?\b",
    r"\b(reviewer|selector|grader|judge)s?\b.{0,30}\b(should|must|will|please)\b",
]


def edit_distance(a, b):
    if a == b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def load_vhh_qc():
    here = os.path.dirname(os.path.abspath(__file__))
    for rel in ("../../antibody-sequence-bioinformatics/scripts", "../antibody-sequence-bioinformatics/scripts"):
        path = os.path.normpath(os.path.join(here, rel))
        if os.path.isfile(os.path.join(path, "vhh_qc.py")):
            sys.path.insert(0, path)
            try:
                import vhh_qc  # noqa: WPS433
                return vhh_qc
            except Exception:  # pragma: no cover - optional dependency
                return None
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--max-designs", type=int, default=10, help="most rows allowed (default 10, the participant guide's figure; use the task's number)")
    ap.add_argument("--min-len", type=int, default=10)
    ap.add_argument("--max-len", type=int, default=250)
    ap.add_argument("--near-dup", type=float, default=0.10, help="warn when two designs are closer than this normalised edit distance (default 0.10; 0 disables; skipped above 100 rows)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    errors, warnings = [], []
    try:
        fh = open(args.csv, newline="", encoding="utf-8-sig")
    except OSError as e:
        sys.exit("cannot open %s: %s" % (args.csv, e))
    with fh:
        head = fh.read(4096)
        fh.seek(0)
        delim = "\t" if head.count("\t") > head.count(",") else ","
        reader = csv.DictReader(fh, delimiter=delim)
        cols = reader.fieldnames or []
        rows = list(reader)
    need = ["name", "sequence", "molecule_class"]
    missing = [c for c in need if c not in cols]
    if missing:
        errors.append("missing required column(s): %s (found: %s)" % (", ".join(missing), ", ".join(cols) or "none"))
    if not rows:
        errors.append("no data rows")
    if len(rows) > args.max_designs:
        errors.append("%d designs, the limit is %d: cut the list, do not rely on the selector to trim it" % (len(rows), args.max_designs))

    vq = load_vhh_qc()
    if vq is None:
        warnings.append("vhh_qc.py not found next to this skill: nanobody rows are not checked for VH/VHH shape")

    names, seqs = {}, {}
    for n, row in enumerate(rows, 1):
        tag = "row %d (%s)" % (n, (row.get("name") or "").strip() or "no name")
        name = (row.get("name") or "").strip()
        raw = row.get("sequence") or ""
        cls = (row.get("molecule_class") or "").strip()
        if not name:
            errors.append("%s: empty name" % tag)
        elif name in names:
            errors.append("%s: name already used in row %d" % (tag, names[name]))
        names.setdefault(name, n)
        if cls not in CLASSES:
            errors.append("%s: molecule_class %r is not one of %s" % (tag, cls, ", ".join(CLASSES)))
        if raw != raw.strip() or re.search(r"\s", raw.strip()):
            errors.append("%s: whitespace inside or around the sequence" % tag)
        seq = raw.strip()
        if seq != seq.upper():
            errors.append("%s: lower-case residues; use upper-case one-letter codes" % tag)
        parts = seq.upper().split(":")
        if cls.startswith("fab"):
            if len(parts) != 2 or not all(parts):
                errors.append("%s: a Fab is one string 'VH:VL' (exactly one colon, both chains non-empty)" % tag)
        elif len(parts) > 1:
            errors.append("%s: ':' only belongs in Fab rows (molecule_class fab_kappa / fab_lambda)" % tag)
        bad = sorted({c for p in parts for c in p if c not in STANDARD})
        if bad:
            errors.append("%s: residues outside the 20 standard amino acids: %s" % (tag, "".join(bad)))
        if cls in ("protein", "nanobody", "scfv"):
            L = len(seq.replace(":", ""))
            if L < args.min_len or L > args.max_len:
                (warnings if cls == "scfv" and L > args.max_len else errors).append("%s: length %d outside %d-%d" % (tag, L, args.min_len, args.max_len))
        if cls == "nanobody" and vq and not bad and len(parts) == 1:
            labels, info = vq.segment_vh(seq.upper())
            if labels is None:
                warnings.append("%s: labelled nanobody but not recognised as a VH/VHH domain (%s); a design only counts as a nanobody if a numbering tool annotates it as one" % (tag, info.get("reason", "")[:80]))
        if cls.startswith("fab") and vq and len(parts) == 2 and not bad:
            if vq.segment_vh(parts[0])[0] is None:
                warnings.append("%s: the VH half is not recognised as a heavy-chain variable domain" % tag)
        key = seq.upper()
        if key in seqs:
            errors.append("%s: identical to row %d; designs must be unique" % (tag, seqs[key]))
        seqs.setdefault(key, n)
        for c in cols:
            if c.lower() in TEXT_COLUMNS and row.get(c):
                for pat in ADDRESSING:
                    m = re.search(pat, row[c], re.I | re.S)
                    if m:
                        warnings.append("%s, column %s: text reads as addressed to the selector (%r). Describe the design, not what the reader should do" % (tag, c, m.group(0)[:50]))
                        break
    keys = list(seqs)
    if args.near_dup > 0 and len(keys) > NEAR_DUP_MAX_ROWS:
        warnings.append("near-duplicate scan skipped for more than %d rows (it compares every pair); use rank_designs.py --min-distance for large tables" % NEAR_DUP_MAX_ROWS)
        keys = []
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            a, b = keys[i], keys[j]
            if abs(len(a) - len(b)) / max(len(a), len(b), 1) < args.near_dup and edit_distance(a, b) / max(len(a), len(b), 1) < args.near_dup:
                warnings.append("rows %d and %d differ by under %.0f%%: they may count as one design" % (seqs[a], seqs[b], args.near_dup * 100))

    result = {"file": os.path.basename(args.csv), "rows": len(rows), "limit": args.max_designs, "errors": errors, "warnings": warnings,
              "by_class": {c: sum(1 for r in rows if (r.get("molecule_class") or "").strip() == c) for c in CLASSES}}
    if args.json:
        json.dump(result, sys.stdout, indent=1)
        print()
    else:
        print("%s: %d rows (limit %d); by class %s" % (result["file"], len(rows), args.max_designs, {k: v for k, v in result["by_class"].items() if v}))
        print("ranking = row order; row 1 is your first choice: %s" % (", ".join((r.get("name") or "?") for r in rows[:5]) + (" ..." if len(rows) > 5 else "")))
        for e in errors:
            print("ERROR   " + e)
        for w in warnings:
            print("WARNING " + w)
        print("\n%s" % ("FAIL: %d error(s), %d warning(s)" % (len(errors), len(warnings)) if errors else "PASS (%d warning(s))" % len(warnings)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
