---
name: antibody-literature-search
description: Find and summarise antibody and immunology literature and public database records - papers on a target, antibody or method, the originator publication for a named mAb, UniProt entries, PDB and SAbDab structures, Thera-SAbDab therapeutic sequences, IMGT germlines, clinical trials, patent sequences. Use when asked what is known or published about an antigen, antibody, epitope or assay, to look up an accession, PDB ID, PMID or DOI, to summarise a paper, or to assemble evidence on an antibody target. Every identifier is resolved against the source before it is written. Use antibody-therapeutics-landscape for industry and format context, antibody-reagent-selection to choose a commercial antibody, antibody-sequence-bioinformatics to work with the sequences retrieved.
---

# Antibody literature and database search

Getting from a question to sourced evidence, with every citation verified.

## Resolve before writing

An identifier that has not been fetched in this session does not get written down. This applies to PMIDs, DOIs, accessions, PDB IDs, clone names, catalogue numbers and trial IDs alike.

The discipline, in order:

1. **Search**, do not recall. Antibody and immunology citations are the easiest thing in this field to generate plausibly and wrongly: the right-looking author, journal and year attached to a paper that does not exist.
2. **Fetch the record** for every identifier that will appear in the output.
3. **Match the record to the claim.** A resolving PMID proves the paper exists, not that it says what the answer attributes to it. Read the abstract at minimum; read the methods when the claim is about how something was measured.
4. **Carry provenance into the output** — identifier, title, year, and what that source actually supports.

If a source cannot be resolved, write the claim as unsourced or drop it. Stating "I could not find a reference for this" is a correct answer.

Database records carry provenance too. A record is cited with its accession plus, where the resource versions its data, the release or version and the date it was retrieved — `UniProt P04626 (retrieved 2026-11-13)`, `PDB 1N8Z`, `Thera-SAbDab trastuzumab`, `IEDB epitope ID 12345`. Database content changes between releases, so a bare accession with no version is not reproducible. Prefer the primary source (the deposited record) over a secondary summary of it.

## Pick the resource from the question

| Question | Go to |
|---|---|
| What is published about this target, antibody or method? | Europe PMC or PubMed |
| What is this protein, its domains, isoforms, PTMs, sequence? | UniProt |
| Which epitopes are known or mapped for this antigen? | IEDB |
| Is there a structure of this complex? | RCSB PDB, then SAbDab for antibody-specific annotation |
| What is the sequence and format of a named therapeutic antibody? | Thera-SAbDab, IMGT/mAb-DB |
| Has this antibody sequence been published or patented before? | PLAbDab |
| Which germline genes and alleles exist? | IMGT/GENE-DB, OGRDB |
| Has this repertoire or clonotype been seen in a study? | OAS, iReceptor, VDJbase |
| Which trials exist and what phase? | ClinicalTrials.gov, EU CTIS, WHO ICTRP |
| Which antibodies are approved or under review? | The Antibody Society's table, YAbS |
| Has this sequence been claimed in a patent? | Google Patents, Lens.org, patent sequence databases |
| Which commercial antibodies target this protein, and are they validated? | antibody-reagent-selection |

Details, URLs and API notes: [references/resources.md](references/resources.md). Query syntax and worked recipes: [references/search-recipes.md](references/search-recipes.md).

## Search breadth

A single query answers almost nothing in this field. For any question beyond a direct lookup, run several searches in one batch and vary the vocabulary, because the same object has many names:

- the target: gene symbol, protein name, CD number, former names, species.
- the antibody: INN, code name (often `ABC-123`), brand name, clone ID, originator company.
- the concept: the method name plus its common abbreviation.

Stop when the same papers keep returning from different vocabularies. That saturation is the completion criterion, not a fixed number of searches.

## Summarise with the evidence attached

For each paper that earns a place in the answer, extract the fields in [references/reading-a-paper.md](references/reading-a-paper.md) — target, antibody and format, what was measured and how, model system, controls, effect size, limitations — and distinguish throughout:

- what was **measured** versus what was **concluded**,
- **in vitro**, animal, and human evidence,
- **peer-reviewed** versus preprint versus conference abstract versus company press release.

Rank claims by that hierarchy rather than by how recent or emphatic they are. A press release reporting a positive phase 2 is weaker evidence than the published trial, and both should be labelled as what they are.

## Fetching politely

Public APIs here are free and rate-limited. Batch requests, obey the documented limits, and cache results in the scratchpad rather than re-fetching.

NCBI's E-utilities ask callers to identify themselves with `tool` and `email` parameters. Send a generic client name, and ask the user before putting their own email address in a request to any external service.
