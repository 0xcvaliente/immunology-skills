# AIRR data

## Why AIRR

The AIRR Community Rearrangement schema is the interchange format for annotated receptor sequences: a tab-delimited file with a required header, one row per rearrangement, and defined field names. IgBLAST, MiXCR, Change-O, scirpy and immunarch all read or write it, so normalising to AIRR early means downstream code faces one schema instead of five.

The authoritative field list lives at `https://docs.airr-community.org` — read the version matching the data rather than caching the list, since fields are added between releases. The current release is **AIRR Standards v2.0.0** (with v1.6.1 as the previous stable line); the schema moved on from v1.x with reorganised single-cell, clone and packaging structures, so a file written for one major version is not silently interchangeable with the other. Pin the schema version in the project and record it with the data.

## Fields that carry the data

The commonly required core: `sequence_id`, `sequence`, `rev_comp`, `productive`, `v_call`, `d_call`, `j_call`, `sequence_alignment`, `germline_alignment`, `junction`, `junction_aa`, and the `v_cigar`, `d_cigar`, `j_cigar` alignment strings. Widely used additions: `locus`, `cdr3`, `cdr3_aa`, `np1`, `np2`, `v_germline_start`/`v_germline_end` and the matching sequence-coordinate pairs, `clone_id`, `cell_id`, `consensus_count`, `duplicate_count`.

Traps in this schema specifically:

- **Coordinates are 1-based closed intervals.** Python slicing is 0-based half-open. Every `_start`/`_end` pair needs `start-1` on entry to a slice, and that conversion is the single most common bug in AIRR-handling code. Write one helper and use it everywhere.
- **`junction_aa` is not `cdr3_aa`.** The junction includes the conserved flanking Cys and Trp/Phe; CDR3 excludes them. Pick one and keep it; never mix them in a length distribution or a clonotype key.
- **`v_call` can hold several comma-separated alleles** when the assignment is ambiguous. Code that assumes one value silently takes the whole string as a gene name. Decide explicitly whether to keep ties, take the first, or collapse to gene level, and record the choice.
- **Gene, allele and family are three levels.** `IGHV3-23*01` is an allele, `IGHV3-23` a gene, `IGHV3` a family. Comparisons across datasets usually have to drop to gene level because allele calling depends on the reference set.
- **`productive` is the tool's verdict**, computed under its own rules. Check frame and stop codons independently when the conclusion depends on it.
- **`rev_comp`** tells you the stored `sequence` orientation relative to the original read; ignoring it misorients coordinates.

## Germline references

Record the reference set and its version with every annotated dataset: **IMGT/GENE-DB** is the conventional source, **OGRDB** (AIRR Community) publishes curated and inferred germline sets with citable versions, and species beyond human and mouse often need a set built for that organism. Assignments from different reference sets are not comparable, and a mutation-frequency number is only meaningful relative to its reference.

## Where the data lives

Annotated repertoire data is exchanged through the AIRR Data Commons rather than as loose files. **iReceptor** (`https://gateway.ireceptor.org`) federates the member repositories and queries them through the ADC API; **OAS** (`https://opig.stats.ox.ac.uk/webapps/oas/`) serves bulk background repertoires; **VDJbase** (`https://vdjbase.org`) curates gene and allele variation across individuals; **VDJServer** (`https://vdjserver.org`) is an AIRR-aware analysis and deposition service. Raw reads go to the **NCBI SRA** or **ENA** with MiAIRR-compliant metadata, and every accession cited should resolve.

## QC checklist

Run before any analysis, and report the counts dropped at each step:

1. **Record count** and the per-step attrition, kept as a table. An unexplained drop is a bug.
2. **Chain type consistency** — `locus` agrees with the actual sequence, and heavy and light are not mixed in a file that is treated as one chain.
3. **Frame and stops** — translate independently and count stop codons; compare with `productive`.
4. **Junction sanity** — junction starts with the conserved Cys, ends with Trp (heavy) or Phe (light), length divisible by three in nucleotide form.
5. **Length distributions** — plot CDR3 length; a bimodal or implausibly long tail points at frame or trimming problems.
6. **Duplicates** — decide what a duplicate is (identical `sequence`, identical junction plus V and J, identical UMI) and apply it consistently. Collapse before diversity statistics, since PCR duplicates inflate every one of them.
7. **Paired data** — count cells with exactly one heavy and one light chain, and decide explicitly how to treat orphans and multiplets rather than letting a merge drop them.
8. **Round-trip** — write the file, read it back, and compare record counts and a hash of the key columns. This catches quoting, delimiter and type-coercion damage, which is why AIRR forbids `@`, `#` and quote characters in values.
9. **Contamination check** — unexpected species in germline assignments, or index-hopping signatures between samples sequenced together.

## Scale

Repertoire files are large. Stream them, filter early, keep intermediate artefacts on disk with their provenance, and never compare diversity metrics computed at different sequencing depths without rarefaction.
