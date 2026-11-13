---
name: antibody-sequence-bioinformatics
description: Work with antibody and BCR sequence data - numbering schemes (IMGT, Kabat, Chothia, Martin, AHo), CDR and framework boundaries, germline assignment with ANARCI, abnumber or IgBLAST, repertoire pipelines, the AIRR Rearrangement TSV format, clonotype grouping, heavy-light pairing, humanness and germline identity, and sequence liability motifs. Use when parsing, numbering, annotating, converting, grouping or QC-ing antibody sequences or repertoire files, when a region coordinate or CDR definition is in question, or when writing code against AIRR, IgBLAST, ANARCI or OAS data. Every region coordinate carries the name of its numbering scheme. Use antibody-literature-search to find sequences and structures, antibody-therapeutics-landscape for formats and engineering vocabulary.
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

Scheme table and boundary definitions: [references/numbering.md](references/numbering.md).

## Steps

1. **Establish the input** — chain type (heavy, kappa, lambda, or a mixed file), amino acid or nucleotide, paired or unpaired, and whether sequences are full-length V(D)J or variable-domain only. Check a handful of records by eye before writing a pipeline over the file.
2. **Number and annotate** with a tool, not by hand: ANARCI or abnumber for numbering and region extraction, IgBLAST for germline assignment from nucleotide data. Tool choices and snippets: [references/tools.md](references/tools.md).
3. **Normalise to AIRR Rearrangement TSV** as the interchange format, so downstream code reads one schema. Field conventions and coordinate traps: [references/airr-data.md](references/airr-data.md).
4. **QC before analysis.** Run the checklist in `airr-data.md`: productive flags, frame, stop codons, chain-type consistency, duplicate handling, orphan chains in paired data, and a round-trip check that writing then re-reading the file reproduces the records.
5. **Report flags as flags.** Liability motifs, humanness scores and clonotype groupings are hypotheses with thresholds, and the threshold must travel with the number: [references/liabilities.md](references/liabilities.md).

## Clonotype definitions are a choice, not a fact

Any statement about clonal diversity depends on a definition that must be stated: identical junction nucleotides; identical CDR3 amino acids plus same V and J gene; CDR3 amino acid identity above a threshold with the same V and J; or a hierarchical-clustering definition with a distance cutoff. These give answers that differ several-fold on the same data. Report the definition alongside every diversity number, and keep one definition across any comparison.

## Reference

- [references/numbering.md](references/numbering.md) — schemes, CDR and framework boundaries, insertion codes, conversion.
- [references/tools.md](references/tools.md) — tool-to-job map, install notes, Python and CLI snippets.
- [references/airr-data.md](references/airr-data.md) — AIRR Rearrangement essentials, germline references, QC checklist.
- [references/liabilities.md](references/liabilities.md) — sequence liability motifs, humanness, and what sequence alone cannot decide.
