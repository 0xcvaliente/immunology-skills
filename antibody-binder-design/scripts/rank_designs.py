#!/usr/bin/env python3
"""Filter, rank and shortlist designs from a metrics table, and record the rule used.

    rank_designs.py designs.csv \\
        --metric ipsae_min:max --metric iptm:max --metric pae_interaction:min:0.5 \\
        --hard "plddt>=80" --hard "qc_liab_high==0" \\
        --top 10 --max-per method=4 -o selection.csv

Why this and not a single composite score: individual in-silico metrics are weak
predictors of binding, so the table is ranked on several at once.  Each metric is turned
into a rank (1 = best), ranks are averaged (optionally weighted), and the spread between a
design's best and worst rank is reported, so a design that one model loves and another
rejects is visible instead of averaged away.  The shortlist is then built greedily from
the top while enforcing diversity (edit distance on a chosen column) and per-group caps,
and every design that is left out gets a reason.

Metrics measured on different scales (pLDDT 0-1 versus 0-100) are fine here because only
ranks are used, but hard filters compare raw values: check the scale first.

Controls (--controls) are designs with a known outcome: rows with control_type 'pos' (known
binders) or 'neg' (scrambles, non-binders), scored by the same pipeline.  They show which
metrics actually separate them in your setup (AUC), and --weights-from-controls weights the
ranking by that separation.  With fewer than ~10 controls per class the AUC is noisy.
"""
from __future__ import annotations

import argparse
import csv
import datetime
import hashlib
import json
import math
import os
import re
import sys

SCRIPT_VERSION = 1
OPS = [(">=", lambda a, b: a >= b), ("<=", lambda a, b: a <= b), ("==", lambda a, b: a == b),
       ("!=", lambda a, b: a != b), (">", lambda a, b: a > b), ("<", lambda a, b: a < b)]


def num(x):
    try:
        v = float(str(x).strip())
        return None if math.isnan(v) else v
    except (TypeError, ValueError):
        return None


def parse_hard(expr):
    for sym, fn in OPS:
        if sym in expr:
            col, val = [p.strip() for p in expr.split(sym, 1)]
            return col, sym, fn, val
    sys.exit("bad --hard expression %r (use e.g. 'plddt>=80')" % expr)


def passes(row, hard):
    col, sym, fn, val = hard
    cell = row.get(col)
    if cell is None or str(cell).strip() == "":
        return False, "%s missing" % col
    a, b = num(cell), num(val)
    ok = fn(a, b) if a is not None and b is not None else (fn(str(cell).strip(), val) if sym in ("==", "!=") else False)
    return ok, "%s%s%s (value %s)" % (col, sym, val, str(cell).strip())


def average_ranks(values, higher_is_better):
    """1 = best; ties share the mean rank; None sorts last."""
    order = sorted(range(len(values)), key=lambda i: (values[i] is None, -values[i] if (values[i] is not None and higher_is_better) else (values[i] if values[i] is not None else 0)))
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return ranks


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


def norm_distance(a, b):
    return edit_distance(a, b) / max(len(a), len(b), 1)


def auc(pos, neg, higher_is_better):
    if not pos or not neg:
        return None
    wins = 0.0
    for p in pos:
        for n in neg:
            if p == n:
                wins += 0.5
            elif (p > n) == higher_is_better:
                wins += 1.0
    return wins / (len(pos) * len(neg))


def median(xs):
    xs = sorted(xs)
    return None if not xs else (xs[len(xs) // 2] if len(xs) % 2 else (xs[len(xs) // 2 - 1] + xs[len(xs) // 2]) / 2)


def sha256_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def read_csv(path):
    with open(path, newline="") as fh:
        head = fh.read(4096)
        fh.seek(0)
        delim = "\t" if head.count("\t") > head.count(",") else ","
        rd = csv.DictReader(fh, delimiter=delim)
        return list(rd), rd.fieldnames or []


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("designs", help="CSV/TSV with a name column and metric columns")
    ap.add_argument("--metric", action="append", required=True, help="NAME:max|min[:weight] (repeat; correlated metrics from one model deserve a lower weight)")
    ap.add_argument("--hard", action="append", default=[], help="hard filter, e.g. 'iptm>=0.5' or 'qc_liab_high==0' (missing values fail)")
    ap.add_argument("--name-col", default="name")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--diverse-col", help="column compared for diversity (default: qc_cdr3, cdr3 or sequence, first that exists)")
    ap.add_argument("--min-distance", type=float, default=0.30, help="min normalised edit distance between picks (default 0.30 = at most 70%% identity)")
    ap.add_argument("--max-per", action="append", default=[], help="COL=K: at most K picks per value of COL (e.g. method=4, epitope=3)")
    ap.add_argument("--disagree", type=float, default=0.5, help="flag designs whose rank spread exceeds this fraction (default 0.5)")
    ap.add_argument("--controls", help="CSV of control designs scored with the same metrics")
    ap.add_argument("--control-col", default="control_type", help="column in --controls holding pos|neg (default control_type)")
    ap.add_argument("--weights-from-controls", action="store_true", help="weight metrics by control separation: max(0, 2*(AUC-0.5))")
    ap.add_argument("-o", "--output", default="selection.csv")
    ap.add_argument("--rule-out", help="where to write the selection rule (default: <output>.rule.json)")
    args = ap.parse_args(argv)

    rows, fields = read_csv(args.designs)
    if not rows:
        sys.exit("no rows in %s" % args.designs)
    if args.name_col not in fields:
        sys.exit("no %r column; columns: %s" % (args.name_col, ", ".join(fields)))
    metrics = []
    for spec in args.metric:
        parts = spec.split(":")
        if len(parts) < 2 or parts[1] not in ("max", "min"):
            sys.exit("--metric %r: expected NAME:max|min[:weight]" % spec)
        if parts[0] not in fields:
            sys.exit("--metric %r: no such column" % parts[0])
        metrics.append({"name": parts[0], "hib": parts[1] == "max", "weight": float(parts[2]) if len(parts) > 2 else 1.0})
    div_col = args.diverse_col or next((c for c in ("qc_cdr3", "cdr3", "sequence") if c in fields), None)
    caps = {}
    for item in args.max_per:
        col, _, k = item.partition("=")
        if col not in fields or not k.isdigit():
            sys.exit("--max-per %r: expected COL=K with COL a column" % item)
        caps[col] = int(k)
    hards = [parse_hard(h) for h in args.hard]

    # --- calibration on controls
    calib = []
    if args.controls:
        crows, cfields = read_csv(args.controls)
        if args.control_col not in cfields:
            sys.exit("controls file has no %r column" % args.control_col)
        for m in metrics:
            pos = [num(r.get(m["name"])) for r in crows if r[args.control_col].strip().lower() in ("pos", "positive")]
            neg = [num(r.get(m["name"])) for r in crows if r[args.control_col].strip().lower() in ("neg", "negative")]
            pos, neg = [x for x in pos if x is not None], [x for x in neg if x is not None]
            a = auc(pos, neg, m["hib"])
            calib.append({"metric": m["name"], "n_pos": len(pos), "n_neg": len(neg), "median_pos": median(pos), "median_neg": median(neg), "auc": a})
            if args.weights_from_controls:
                m["weight"] *= 0.0 if a is None else max(0.0, 2 * (a - 0.5))
        if args.weights_from_controls and not any(m["weight"] > 0 for m in metrics):
            sys.exit("no metric separates the controls better than chance; --weights-from-controls would weight everything at 0")

    # --- hard filters
    reasons = {id(r): [] for r in rows}
    attrition = [("input", len(rows))]
    alive = list(rows)
    for h in hards:
        nxt = []
        for r in alive:
            ok, why = passes(r, h)
            if ok:
                nxt.append(r)
            else:
                reasons[id(r)].append("failed hard filter: " + why)
        alive = nxt
        attrition.append(("after %s%s%s" % (h[0], h[1], h[3]), len(alive)))

    # --- ranks
    for m in metrics:
        vals = [num(r.get(m["name"])) for r in alive]
        ranks = average_ranks(vals, m["hib"])
        for r, v, k in zip(alive, vals, ranks):
            r["rank_" + m["name"]] = ("%g" % k) if v is not None else ("%g" % len(alive))
            if v is None:
                r.setdefault("_missing", []).append(m["name"])
    used = [m for m in metrics if m["weight"] > 0]
    wsum = sum(m["weight"] for m in used)
    for r in alive:
        rk = [float(r["rank_" + m["name"]]) for m in used]
        r["agg_rank"] = "%.2f" % (sum(float(r["rank_" + m["name"]]) * m["weight"] for m in used) / wsum)
        r["rank_spread"] = "%.2f" % (((max(rk) - min(rk)) / max(1, len(alive) - 1)) if len(rk) > 1 else 0.0)
        flags = []
        if float(r["rank_spread"]) > args.disagree:
            flags.append("metrics disagree")
        if r.get("_missing"):
            flags.append("missing: " + ",".join(r["_missing"]))
        r["flags"] = "; ".join(flags)

    # --- greedy diverse shortlist
    picked, group_counts = [], {c: {} for c in caps}
    order = sorted(alive, key=lambda r: (float(r["agg_rank"]), float(r["rank_spread"]), r[args.name_col]))
    for r in order:
        why = None
        if len(picked) >= args.top:
            why = "beyond top %d" % args.top
        else:
            if div_col:
                for p in picked:
                    d = norm_distance(r.get(div_col, ""), p.get(div_col, ""))
                    if d < args.min_distance:
                        why = "near-duplicate of %s on %s (distance %.2f < %.2f)" % (p[args.name_col], div_col, d, args.min_distance)
                        break
            if why is None:
                for col, k in caps.items():
                    if group_counts[col].get(r.get(col, ""), 0) >= k:
                        why = "cap reached: %s=%s already has %d picks" % (col, r.get(col, ""), k)
                        break
        if why:
            reasons[id(r)].append(why)
            continue
        picked.append(r)
        for col in caps:
            group_counts[col][r.get(col, "")] = group_counts[col].get(r.get(col, ""), 0) + 1
        r["selection_order"] = str(len(picked))
        reasons[id(r)].append("picked: aggregated rank %s, spread %s" % (r["agg_rank"], r["rank_spread"]))

    # --- write
    extra = ["rank_" + m["name"] for m in metrics] + ["agg_rank", "rank_spread", "flags", "selected", "selection_order", "reason"]
    out_fields = fields + [c for c in extra if c not in fields]
    picked_ids, alive_ids = {id(r) for r in picked}, {id(r) for r in alive}
    ordered = picked + [r for r in order if id(r) not in picked_ids] + [r for r in rows if id(r) not in alive_ids]
    with open(args.output, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=out_fields, extrasaction="ignore")
        w.writeheader()
        for r in ordered:
            r["selected"] = "yes" if id(r) in picked_ids else "no"
            r["reason"] = " | ".join(reasons[id(r)])
            w.writerow(r)
    rule = {"script": "rank_designs.py", "version": SCRIPT_VERSION, "time_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "input": os.path.basename(args.designs), "input_sha256": sha256_file(args.designs),
            "metrics": [{"name": m["name"], "direction": "max" if m["hib"] else "min", "weight": round(m["weight"], 4)} for m in metrics],
            "hard_filters": args.hard, "top": args.top, "diverse_col": div_col, "min_distance": args.min_distance, "max_per": caps,
            "disagree_threshold": args.disagree, "controls": calib or None, "attrition": attrition,
            "n_selected": len(picked)}
    rule_path = args.rule_out or (args.output + ".rule.json")
    with open(rule_path, "w") as fh:
        json.dump(rule, fh, indent=1)

    # --- report
    print("attrition: " + " -> ".join("%s %d" % a for a in attrition))
    if calib:
        print("\ncontrol calibration (AUC: 0.5 = no separation, 1.0 = perfect):")
        for c in calib:
            a = "n/a" if c["auc"] is None else "%.2f" % c["auc"]
            note = "  <- does not separate your controls" if c["auc"] is not None and c["auc"] < 0.7 else ""
            print("  %-22s AUC %-5s (pos %d, neg %d; medians %s vs %s)%s" % (c["metric"], a, c["n_pos"], c["n_neg"], c["median_pos"], c["median_neg"], note))
    print("\nshortlist (%d of %d, diversity on %s, min distance %.2f):" % (len(picked), len(alive), div_col, args.min_distance))
    for r in picked:
        print("  %2s  %-24s agg %-6s spread %-5s %s" % (r["selection_order"], r[args.name_col][:24], r["agg_rank"], r["rank_spread"], r["flags"]))
    for col in caps:
        print("  picks per %s: %s" % (col, json.dumps(group_counts[col])))
    if len(picked) < args.top:
        print("  note: only %d picks; relax --min-distance or --max-per, or generate more designs" % len(picked))
    print("\nwrote %s and %s" % (args.output, rule_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
