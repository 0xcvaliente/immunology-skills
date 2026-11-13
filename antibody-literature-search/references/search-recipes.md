# Search recipes

## PubMed and Europe PMC syntax

Field tags work in both, with Europe PMC using its own short forms:

```
# PubMed
"CD19"[Title/Abstract] AND "bispecific"[Title/Abstract] AND 2020:2026[dp]
antibodies, monoclonal[MeSH Terms] AND humanization[Title/Abstract]
smith j[Author] AND trastuzumab[Title]

# Europe PMC
TITLE_ABS:"T-cell engager" AND PUB_YEAR:[2022 TO 2026]
AUTH:"Reichert JM" AND SRC:MED
(ABSTRACT:"affinity maturation") AND (OPEN_ACCESS:y)
```

MeSH is the lever for recall in immunology: `Antibodies, Monoclonal`, `Immunoglobulin Variable Region`, `Antibodies, Bispecific`, `Immunoconjugates`, `Single-Domain Antibodies`, `Epitope Mapping`, `Antibody Affinity`. Explode a MeSH term to catch the narrower ones; add free-text synonyms on top because recent papers are not yet indexed.

## Vocabulary expansion, by object

Run the variants in one batch rather than serially.

**A target** — gene symbol (`ERBB2`), protein name (`HER2`), alternative names (`neu`, `CD340`), CD number, species qualifier, and the receptor family. UniProt's "alternative names" field is the cheapest synonym generator.

**A named antibody** — INN (`trastuzumab`), the development code (`RG597`, `MEDI-...`, `ABBV-...`), brand name, originator and current owner, and the clone or construct name in the original paper. Thera-SAbDab maps INN to sequence and sponsor.

**A method** — the full name and the abbreviation (`biolayer interferometry` and `BLI`), plus the dominant instrument name, which is often used as a synonym in methods sections.

## Finding the originator publication for a named mAb

1. Thera-SAbDab for format, target and sequence.
2. Europe PMC for the INN and for the development code; the earliest hits are usually the discovery or first-in-human papers.
3. Patents for the sequence disclosure, which often predates any publication.
4. The label or EPAR for the pivotal trials, then the registry ID, then the trial publication.

Expect the discovery paper, the sequence disclosure and the clinical papers to be three separate sources with three different author lists.

## Structure searches

- Antigen-specific: SAbDab's search by antigen name or UniProt accession returns annotated antibody complexes, which is faster and cleaner than a PDB text search.
- Sequence-similar structures: RCSB's sequence search with an mmseqs2 identity threshold, or BLAST against PDB sequences.
- Check resolution, construct (Fab versus scFv versus full IgG), whether the antigen is full-length or a fragment, and whether crystal contacts could explain the interface before treating a structure as the epitope answer.

## Repertoire and sequence questions

For "has this sequence been seen before", search OAS for near-identical junctions rather than the literature. For "which germline does this come from", run IgBLAST or ANARCI locally (see antibody-sequence-bioinformatics) instead of trusting a paper's stated assignment, since assignments shift with the reference set.

## Trials

```
https://clinicaltrials.gov/api/v2/studies?query.intr=trastuzumab&filter.overallStatus=RECRUITING&format=json
https://clinicaltrials.gov/api/v2/studies?query.term=AREA[InterventionType]BIOLOGICAL AND bispecific&format=json
```

Read the registry record for the pre-specified primary endpoint and compare it against what the publication reports as primary. A changed endpoint is the single most informative thing a trial record can tell you.

## Saturation

Stop expanding when new vocabularies return papers already seen. Record which vocabularies were tried — a search report that lists its queries can be checked and repeated; one that lists only conclusions cannot.
