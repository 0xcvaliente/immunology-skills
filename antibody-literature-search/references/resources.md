# Resources

Stable entry points. Endpoints drift, so when a call fails, fetch the resource's own API documentation rather than guessing at a parameter.

## Literature

**Europe PMC** — `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=<q>&format=json&pageSize=25`. The first choice: no key needed, covers PubMed plus preprints, patents and agricola, and returns open-access full text where available (`.../<PMCID>/fullTextXML`). Supports `&cursorMark=` for paging and `resultType=core` for abstracts and identifiers.

**PubMed / NCBI E-utilities** — `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=<q>&retmode=json`, then `efetch.fcgi` or `esummary.fcgi` with the returned UIDs. Best for MeSH-controlled searching. Identify the client with a generic `tool` name; ask the user before sending their email address.

**bioRxiv / medRxiv** — `https://api.biorxiv.org/details/biorxiv/<DOI>`. Preprints, label them as such.

**Google Scholar** has no API and should not be scraped; use it by hand through the browser when citation counts matter.

## Target biology

**UniProt** — `https://rest.uniprot.org/uniprotkb/<accession>.json` for an entry, `.fasta` for sequence, `https://rest.uniprot.org/uniprotkb/search?query=<q>&format=json` to search. The authority on isoforms, domain boundaries, signal peptides, glycosylation sites and cross-references. Isoform and domain coordinates matter for epitope questions: an antibody raised against a cytoplasmic tail cannot stain intact cells.

**Human Protein Atlas** — `https://www.proteinatlas.org/<ENSG>-<gene>`; tissue and cell-line expression, plus antibody staining images with their own reliability scores.

**AlphaFold DB** — `https://alphafold.ebi.ac.uk/entry/<accession>` for predicted structure where no experimental one exists; a prediction, not evidence of conformation.

## Structures

**RCSB PDB** — entry data `https://data.rcsb.org/rest/v1/core/entry/<ID>`, search via `https://search.rcsb.org/rcsbsearch/v2/query` (JSON query body), coordinates `https://files.rcsb.org/download/<ID>.cif`. **PDBe** at EBI mirrors the archive with its own API.

**SAbDab** — `https://opig.stats.ox.ac.uk/webapps/sabdab-sabpred/sabdab`. Every antibody structure in the PDB, re-annotated consistently: chain assignment, numbering, CDR definitions, antigen, species, affinity where reported. Downloadable as a summary table, CC-BY 4.0. Use this instead of filtering the PDB by hand.

**Thera-SAbDab** — `https://opig.stats.ox.ac.uk/webapps/sabdab-sabpred/therasabdab`. Therapeutic antibodies with their sequences, format, target and development stage, linked to structures where they exist. The route from a drug name to its actual sequence.

**OAS (Observed Antibody Space)** — `https://opig.stats.ox.ac.uk/webapps/oas/`. Billions of repertoire sequences from published studies, for background distributions and germline context.

OPIG publishes successor tools and occasionally reorganises these webapps; if a path 404s, start at `https://opig.stats.ox.ac.uk/webapps` and take the current link.

## Germline references

**IMGT** — `https://www.imgt.org`, with IMGT/GENE-DB for genes and alleles and IMGT/V-QUEST for web-based annotation (rate-limited, interactive use only). The reference for the IMGT numbering scheme itself.

**OGRDB** — `https://ogrdb.airr-community.org`. AIRR Community germline sets, inferred alleles included; the citable source when a germline reference needs a version.

## Clinical and regulatory

**ClinicalTrials.gov API v2** — `https://clinicaltrials.gov/api/v2/studies?query.term=<q>&format=json`. Filter on phase, status and intervention. The registry record is the primary source for what a trial set out to do; compare it against the publication for what was reported.

**EU CTIS** — `https://euclinicaltrials.eu/ctis-public/search`, public register of EU trials under Regulation 536/2014.

**The Antibody Society** — `https://www.antibodysociety.org/resources/approved-antibodies/`, the maintained table of antibodies approved or in regulatory review in the EU or US.

**Labels** — Drugs@FDA and the FDA label database; EMA's medicine pages for the EPAR and SmPC. The label settles indication, dosing and warnings; secondary sources often lag it.

## Reagents and sequences in patents

**Antibody Registry** — `https://antibodyregistry.org`, assigns RRIDs to commercial antibodies; the identifier that makes a reagent citation reproducible.

**Patent sequences** — Lens.org PatSeq, EPO Espacenet, Google Patents. Many therapeutic antibody sequences appear first in patent filings; a patent is a disclosure, not peer-reviewed evidence, and sequence-to-molecule mapping in filings is frequently ambiguous.
