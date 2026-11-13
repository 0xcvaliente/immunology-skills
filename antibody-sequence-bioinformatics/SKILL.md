---
name: antibody-sequence-bioinformatics
description: Work with antibody, nanobody (VHH) and BCR sequence data - numbering schemes (IMGT, Kabat, Chothia, Martin, AHo), CDR and framework boundaries, VHH hallmark residues and cysteine checks, germline assignment with ANARCII, ANARCI, abnumber or IgBLAST, mapping CDRs onto a structure's residue numbers for loop-redesign contigs, interface contacts and hotspot coverage of a predicted complex, repertoire pipelines, the AIRR Rearrangement TSV format, clonotype grouping, humanness, and sequence liability motifs. Use when parsing, numbering, annotating, QC-ing or filtering antibody, VHH or designed binder sequences, when a CDR definition or region coordinate is in question, when a contig needs PDB residue numbers, or when writing code against AIRR, IgBLAST, ANARCI or OAS data. Every region coordinate carries the name of its numbering scheme. Use antibody-binder-design for the design workflow, antibody-literature-search to find sequences and structures, antibody-therapeutics-landscape for formats and engineering vocabulary.
---

# Antibody sequence bioinformatics

Code and conventions for antibody sequence data: numbering, annotation, interchange and quality control.

Scope: research, therapeutic, diagnostic and educational work. A request to engineer a pathogen toward greater transmissibility, or to design escape from a deployed countermeasure, falls outside it — say so and stop.

## Name the scheme

A residue index without its numbering scheme is meaningless. `H52` is a different residue under Kabat than under IMGT, and `CDR-H1` spans different residues under every scheme in use. So:

- State the scheme in prose, in column names (`cdr1_aa_imgt`), in file names, and in docstrings.
- When data arrives without a stated scheme, re-number it rather than inferring; a mislabelled scheme corrupts every downstream comparison silently.
- Convert by re-numbering the sequence, never by arithmetic on indices. Insertion codes (`52A`, `100A`–`100K`) make index arithmetic wrong.
- Boundaries belong to a scheme too: quote CDR definitions as "IMGT CDR-H3" rather than "CDR3".
- A structure file has its own residue numbers. IMGT positions are not PDB numbers, and a contig or hotspot list must use the file's numbering (`cdr_contig.py` below does the mapping).

Scheme table and boundary definitions: [references/numbering.md](references/numbering.md).

## Steps

1. **Establish the input** — chain type (heavy, kappa, lambda, or a mixed file), amino acid or nucleotide, paired or unpaired, and whether sequences are full-length V(D)J or variable-domain only. Check a handful of records by eye before writing a pipeline over the file.
2. **Number and annotate** with a tool, not by hand: ANARCII (language-model numbering, the OPIG successor to ANARCI) or ANARCI/abnumber for numbering and region extraction, IgBLAST for germline assignment from nucleotide data. Tool choices and snippets: [references/tools.md](references/tools.md).
3. **Normalise to AIRR Rearrangement TSV** as the interchange format, so downstream code reads one schema. Field conventions and coordinate traps: [references/airr-data.md](references/airr-data.md).
4. **QC before analysis.** Run the checklist in `airr-data.md`: productive flags, frame, stop codons, chain-type consistency, duplicate handling, orphan chains in paired data, and a round-trip check that writing then re-reading the file reproduces the records.
5. **Report flags as flags.** Liability motifs, humanness scores and clonotype groupings are hypotheses with thresholds, and the threshold must travel with the number: [references/liabilities.md](references/liabilities.md).

## VHH, designed binders and structures

Three standard-library scripts in `scripts/` (Python 3.9+, nothing to install; `--help` on each). Run them from this skill's directory or by full path.

| Question | Command |
|---|---|
| What are this VHH's CDRs, hallmarks, cysteines, liabilities, charge? | `python3 scripts/vhh_qc.py seqs.fasta` or `python3 scripts/vhh_qc.py designs.csv --annotate -o designs.qc.csv` |
| Which residue numbers hold the CDRs in this structure, and what contig redesigns them? | `python3 scripts/cdr_contig.py 1ZVY.cif --chain A --target-chain B --design CDR3 --length CDR3=16-24` |
| Does this predicted complex touch the intended epitope, through the CDRs? | `python3 scripts/interface_contacts.py design.cif --binder H --target A --hotspots A45,A67` |

Rules that keep their output trustworthy:

- `vhh_qc.py` places regions by anchoring on Cys23, Trp41, Cys104 and the FR4 tail. It reads one VH/VHH domain and **reports a sequence it cannot place as unplaced instead of guessing**. For an exact IMGT numbering, or when chain type matters, add `--numbering anarcii`. Agreement with ANARCII, the cases it declines, and the limits: [references/vhh.md](references/vhh.md).
- Positions in its output are raw 1-based indices plus a region name, never IMGT numbers.
- `cdr_contig.py` drops residues whose backbone N, CA or C is missing, because a contig naming an unresolved residue fails inside the design tool. Run it on the exact file you will upload.
- Contig syntax and residue-numbering convention belong to the design tool; confirm both in that tool's documentation before pasting.
- `interface_contacts.py` reports geometry only. It is a filter on *where* a design binds, not an estimate of how well.

## Clonotype definitions are a choice, not a fact

Any statement about clonal diversity depends on a definition that must be stated: identical junction nucleotides; identical CDR3 amino acids plus same V and J gene; CDR3 amino acid identity above a threshold with the same V and J; or a hierarchical-clustering definition with a distance cutoff. These give answers that differ several-fold on the same data. Report the definition alongside every diversity number, and keep one definition across any comparison.

## Reference

- [references/numbering.md](references/numbering.md) — schemes, CDR and framework boundaries, insertion codes, conversion, IMGT versus PDB numbering.
- [references/vhh.md](references/vhh.md) — VHH sequence features, hallmark residues, cysteines, what `vhh_qc.py` was validated against.
- [references/tools.md](references/tools.md) — tool-to-job map, install notes, Python and CLI snippets.
- [references/airr-data.md](references/airr-data.md) — AIRR Rearrangement essentials, germline references, QC checklist.
- [references/liabilities.md](references/liabilities.md) — sequence liability motifs, humanness, and what sequence alone cannot decide.
