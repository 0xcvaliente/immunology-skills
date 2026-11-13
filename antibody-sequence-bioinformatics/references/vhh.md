# VHH sequences

A VHH (single-domain antibody, nanobody) is the variable domain of a camelid heavy-chain-only antibody: one domain of about 120 residues and 15 kDa, three CDRs, no light chain. It is numbered like a heavy-chain variable domain: IMGT numbering, framework and CDR boundaries as in [numbering.md](numbering.md). "Nanobody" is a trademark of Ablynx (Sanofi); "VHH" and "single-domain antibody" are the generic terms.

## What differs from a conventional VH

**Hallmark residues.** Four framework-2 positions that face the light chain in a conventional antibody are replaced in a classical VHH, so the domain stays soluble alone. IMGT positions 42, 49, 50 and 52 (the VHH criterion in the [IMGT Lexique](https://imgt.org/IMGTeducation/IMGTlexique/O/Only-heavy-chainantibodies.html)); in Kabat numbering the same positions are 37, 44, 45 and 47.

| IMGT position | Conventional VH | Classical VHH |
|---|---|---|
| 42 | Val | Phe or Tyr |
| 49 | Gly | Glu (also Gln) |
| 50 | Leu | Arg |
| 52 | Trp | Phe, Leu or Gly |

- `vhh_qc.py` prints the four residues and a class: **VHH-type** (at most one conventional residue), **VH-type** (all four conventional, as in `VGLW`) or **mixed**. A VH-type framework is not an error: non-classical VHHs exist, and many engineered or humanised nanobodies are partly VH-like. It is a prompt to check solubility and aggregation, because the former light-chain interface is then exposed.
- Positions 42 and 52 are the ones reported to matter most for stability and binding, and reverting them toward the conventional residue is discouraged in humanisation; 49 and 50 are reported as more tolerant. Treat the first pair as a "do not mutate without evidence" set when editing a VHH framework.
- Position 118 (first residue of FR4) is usually Trp but not always: Arg and His occur in natural VHHs, and synthetic libraries (sybodies) carry Phe, Tyr, Ile, Leu. A scan that insists on `WGQG` will reject real nanobodies.

**Cysteines.** The canonical pair is Cys23 (FR1) and Cys104 (end of FR3). Some camelid VHHs carry a second, extra disulfide that links CDR3 to CDR1 or to the framework (FR2). So: two Cys is the standard case; four, with the extra pair accounted for, is plausible; **an odd number means a free thiol**, which is a developability problem. `vhh_qc.py` reports the count and where the extra ones sit.

**CDR3.** Usually the longest and most variable loop and, with no light chain to share the work, the main binder. In a VHH it often folds back over the framework, which makes its shape hard to predict and is why confidence scores are least reliable there.

**Developability.** TNP (Therapeutic Nanobody Profiler, [web](https://tnp.opig.stats.ox.ac.uk/), [code](https://github.com/oxpig/TNP)) compares a nanobody with clinical-stage therapeutics and flags properties such as CDR length, CDR3 compactness and surface charge or hydrophobic patches; paper: Gordon et al., bioRxiv 2025, [doi:10.1101/2025.08.11.669635](https://doi.org/10.1101/2025.08.11.669635). Its thresholds are updated with the tool, so read them from the live tool, not from a note. Motif-level checks are in [liabilities.md](liabilities.md).

## vhh_qc.py: what it was checked against

`scripts/vhh_qc.py` segments a VH/VHH domain without a numbering model, so its placement was measured against ANARCII 2.0.8 (IMGT) on real PDB chains, on 2026-11-13: four sets of nanobody and conventional heavy-chain sequences found by free-text search of the PDB, plus kappa/lambda light chains and shark VNARs as negatives. The first three sets were used while the rules were developed. The fourth was disjoint on its first run (right-hand column); one rule, for a double Cys at the end of FR3, was added after reading its two mismatches, so the left-hand column includes that fix.

| Result | All four sets, final script | Fourth set, first run |
|---|---|---|
| Heavy-chain domains placed | 417 of 419 | 97 of 97 |
| Light chains or VNARs wrongly accepted | 0 of 59 | 0 of 26 |
| CDR1 / CDR2 / CDR3 identical to ANARCII | 99.8 / 99.3 / 100 % | 99.0 / 100 / 97.9 % |
| FR2 / FR3 / FR4 identical | 99.5 / 99.8 / 100 % | 100 / 97.9 / 100 % |
| Hallmark tetrad identical | 99.5 % | 100 % |

Known limits, all of which are reported rather than guessed:

- **Cys23 mutated** (cysteine-free engineered nanobodies) is returned as unplaced; two such sequences were the only misses.
- A **2-residue deletion in FR1** or an **insertion in FR2/FR3** shifts a boundary by one or two residues (about 1 sequence in 100). Where the exact CDR2 or FR3 boundary decides something, use `--numbering anarcii`.
- One domain only. Tandem constructs and long inputs are flagged; split them first.
- It cannot name the chain type reliably in unusual cases (an engineered light chain carrying a VH-style FR4 is caught by its `R-F-S-G-S` FR3 signature, but other chimeras may not be). ANARCII reports H/K/L and a confidence score; across the four sets every heavy-chain domain scored 26.2 or more, with a median near 30, and the two shark VNARs forced through the antibody model scored 17.9 and 19.5. `--numbering anarcii` therefore treats a score below 25 as unplaced (`--min-anarcii-score` changes it); the floor is empirical, from two VNARs, so look at the score when a sequence is unusual. Unlike the heuristic, the ANARCII path places Cys23-mutated nanobodies.
- Ground truth is itself a model. Treat ANARCII as the reference, not as an experiment.

The regression panel is in `tests/fixtures/vhh_panel.json`; `python3 -m unittest discover -s tests` re-runs it.

## Using ANARCII

Install notes and the Python snippet are in [tools.md](tools.md). `vhh_qc.py --numbering anarcii` wraps it, so a sequence list can be placed exactly without writing code.
