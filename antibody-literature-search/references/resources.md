# Resources

Stable entry points. Endpoints drift, so when a call fails, fetch the resource's own API documentation rather than guessing at a parameter.

## Literature

**Europe PMC** — `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=<q>&format=json&pageSize=25`. The first choice: no key needed, covers PubMed plus preprints, patents and agricola, and returns open-access full text where available (`.../<PMCID>/fullTextXML`). Supports `&cursorMark=` for paging and `resultType=core` for abstracts and identifiers.

**PubMed / NCBI E-utilities** — `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=<q>&retmode=json`, then `efetch.fcgi` or `esummary.fcgi` with the returned UIDs. Best for MeSH-controlled searching. Identify the client with a generic `tool` name; ask the user before sending their email address.

**bioRxiv / medRxiv** — `https://api.biorxiv.org/details/biorxiv/<DOI>`. Preprints, label them as such.

**OpenAlex** — `https://api.openalex.org/works/https://doi.org/<DOI>`. Open metadata and citation graph, no key, useful for resolving a DOI to a title, venue and year and for finding what cites a paper. **Crossref** (`https://api.crossref.org/works/<DOI>`) is the registration authority for DOIs and the place to confirm a DOI actually resolves before citing it.

**Google Scholar** has no API and should not be scraped; use it by hand through the browser when citation counts matter.

## Target biology

**UniProt** — `https://rest.uniprot.org/uniprotkb/<accession>.json` for an entry, `.fasta` for sequence, `https://rest.uniprot.org/uniprotkb/search?query=<q>&format=json` to search. The authority on isoforms, domain boundaries, signal peptides, glycosylation sites and cross-references. Isoform and domain coordinates matter for epitope questions: an antibody raised against a cytoplasmic tail cannot stain intact cells.

**Human Protein Atlas** — `https://www.proteinatlas.org/<ENSG>-<gene>`; tissue and cell-line expression, plus antibody staining images with their own reliability scores.

**AlphaFold DB** — `https://alphafold.ebi.ac.uk/entry/<accession>` for predicted structure where no experimental one exists; a prediction, not evidence of conformation.

## Epitopes and immune-receptor data

**IEDB (Immune Epitope Database)** — `https://www.iedb.org`. NIAID-funded catalogue of experimentally characterised B-cell and T-cell epitopes across infectious disease, allergy, autoimmunity and transplantation, with the assay and the reference behind each entry. The place to check whether an epitope has been mapped before, and how, rather than inferring it from a structure.

**IMGT/mAb-DB** — `https://www.imgt.org/mAb-DB/`. Curated therapeutic and diagnostic monoclonal antibodies and fusion proteins, with their sequences, targets and clinical stage, cross-linked into IMGT's gene and structure data. Complements Thera-SAbDab when the question is a fusion protein or the IMGT gene context.

**PLAbDab (Patent and Literature Antibody Database)** — `https://opig.stats.ox.ac.uk/webapps/plabdab/`. Over 150,000 paired antibody sequences mined from patents and papers, each linked to its source, searchable by sequence or CDR structure. The tool for "has this antibody sequence appeared before", which neither the literature nor the PDB answers directly.

## Structures

**RCSB PDB** — entry data `https://data.rcsb.org/rest/v1/core/entry/<ID>`, coordinates `https://files.rcsb.org/download/<ID>.cif` (or `.pdb`), sequences of every chain `https://www.rcsb.org/fasta/entry/<ID>`. Search is a POST of a JSON query to `https://search.rcsb.org/rcsbsearch/v2/query`; paging goes under `request_options.paginate` (not `paging`, which fails schema validation):

```bash
curl -s -X POST https://search.rcsb.org/rcsbsearch/v2/query -H 'Content-Type: application/json' \
  -d '{"query":{"type":"terminal","service":"full_text","parameters":{"value":"nanobody"}},"return_type":"entry","request_options":{"paginate":{"start":0,"rows":25}}}'
```

**PDBe** at EBI mirrors the archive with its own API.

**SAbDab** — `https://opig.stats.ox.ac.uk/webapps/sabdab-sabpred/sabdab`. Every antibody structure in the PDB, re-annotated consistently: chain assignment, numbering, CDR definitions, antigen, species, affinity where reported. Downloadable as a summary table, CC-BY 4.0. Use this instead of filtering the PDB by hand. Its nanobody subset, **SAbDab-nano**, is the source of VHH–antigen complexes for controls and calibration.

**Thera-SAbDab** — `https://opig.stats.ox.ac.uk/webapps/sabdab-sabpred/therasabdab`. Therapeutic antibodies with their sequences, format, target and development stage, linked to structures where they exist. The route from a drug name to its actual sequence.

OPIG publishes successor tools and occasionally reorganises these webapps; if a path 404s, start at `https://opig.stats.ox.ac.uk/webapps` and take the current link.

## Measured designs and binding data

What the field has actually measured, which is what a calibration set should be made of.

**Proteinbase** — `https://proteinbase.com` (also served at `https://design.adaptyvbio.com`). Adaptyv's open database of protein designs with wet-lab results, organised by protein, collection, design method, target and competition. Each design method page shows how many designs were generated and how many tested; the Anthropic × Adaptyv competition results are published here, negative results included, under ODC-BY. Use it to find measured positives and negatives for a target or a method, and to see how a method has performed in practice rather than in its paper. Reference paper for an earlier crowdsourced round: Crowdsourced Protein Design: Lessons From the Adaptyv EGFR Binder Competition, bioRxiv 2025, [doi:10.1101/2025.04.17.648362](https://doi.org/10.1101/2025.04.17.648362).

**SKEMPI 2.0** — `https://life.bsc.es/pid/skempi2`. Experimental changes in binding free energy on mutation, protein–protein complexes.

**AB-Bind** — `https://github.com/sarahsirin/AB-Bind-Database`. Antibody-specific mutational binding data.

**Ginkgo Datapoints** — `https://datapoints.ginkgo.bio/dataset-access`. Developability datasets, including sets measured on VHHs.

**Practical guides.** [How to Design Antibodies](https://www.asimov.press/p/antibody-design) (Asimov Press, 11 March 2026): five stages from target choice to lab testing with open-source tools. Adaptyv's post on [novelty](https://www.adaptyvbio.com/blog/novelty) is the reference the competition FAQ gives for its novelty rule.

## Germline references

**IMGT** — `https://www.imgt.org`, with IMGT/GENE-DB for genes and alleles and IMGT/V-QUEST for web-based annotation (rate-limited, interactive use only). The reference for the IMGT numbering scheme itself.

**OGRDB** — `https://ogrdb.airr-community.org`. AIRR Community germline sets, inferred alleles included; the citable source when a germline reference needs a version.

## Repertoire and sequence repositories

Where annotated repertoire data lives, and where to deposit it. All speak the AIRR Rearrangement schema (see antibody-sequence-bioinformatics).

**OAS (Observed Antibody Space)** — `https://opig.stats.ox.ac.uk/webapps/oas/`. Billions of repertoire sequences from published studies, for background distributions and germline context.

**iReceptor Gateway** — `https://gateway.ireceptor.org`. Federated search across AIRR-seq repositories (billions of annotated sequences) through the AIRR Data Commons API; the fastest way to ask whether a junction has been seen elsewhere.

**VDJbase** — `https://vdjbase.org`. Curated immune-receptor gene and allele variation across individuals, from AIRR-seq and genomic data; the reference for population-level germline questions that a single reference set hides.

**NCBI SRA / ENA** — raw sequencing reads, submitted with MiAIRR-compliant study, subject and sample metadata. VDJServer (`https://vdjserver.org`) is an AIRR-aware alternative for analysis and deposition.

## Clinical and regulatory

**ClinicalTrials.gov API v2** — `https://clinicaltrials.gov/api/v2/studies?query.term=<q>&format=json`. Filter on phase, status and intervention. The registry record is the primary source for what a trial set out to do; compare it against the publication for what was reported.

**EU CTIS** — `https://euclinicaltrials.eu/ctis-public/search`, public register of EU trials under Regulation 536/2014 (CTIS launched 31 January 2022 and is a WHO primary registry). Trials authorised before that date sit in the predecessor EU Clinical Trials Register, `https://www.clinicaltrialsregister.eu`.

**WHO ICTRP** — `https://www.who.int/tools/clinical-trials-registry-platform`. A registry of registries: it aggregates ClinicalTrials.gov, CTIS, ISRCTN, ANZCTR, ChiCTR, CTRI, DRKS, JPRN and others into one search portal. Use it when a trial may be registered only outside the US or EU.

**The Antibody Society** — `https://www.antibodysociety.org/resources/approved-antibodies/`, the maintained table of antibodies approved or in regulatory review in the EU or US. Its searchable companion **YAbS** (`https://db.antibodysociety.org/`) covers approved, in-development and terminated antibody therapeutics.

**Labels** — Drugs@FDA and the FDA label database; EMA's medicine pages for the EPAR and SmPC. The label settles indication, dosing and warnings; secondary sources often lag it.

## Nomenclature

**WHO INN** — `https://www.who.int/teams/health-product-and-policy-standards/inn/stembook`. The stem book defines every INN stem and pre-stem, including the mAb scheme (`-tug`, `-bart`, `-ment`, `-mig`) and the `-fusp` fusion-protein scheme. Quote the WHO definition, not a remembered gloss. The USAN Council (`https://www.ama-assn.org/about/united-states-adopted-names-usan`) publishes the parallel US naming policy.

## Reagents, cell lines and patents

**Antibody Registry** — `https://antibodyregistry.org`, assigns RRIDs to commercial antibodies; the identifier that makes a reagent citation reproducible. The **RRID portal** (`https://rrid.site`, `https://scicrunch.org/resources`) resolves an RRID and also covers cell lines, organisms and software.

**Cellosaurus** — `https://www.cellosaurus.org`. The curated reference for cell lines, and the authority behind cell-line RRIDs (`RRID:CVCL_...`). Check identity, misidentified-line notes and knockout/background status before trusting a line as a control.

**CiteAb** — `https://www.citeab.com`. Reagent and cell-line search ranked by how often each is cited in the literature; useful for finding which clone papers actually used.

**Patent sequences** — Lens.org PatSeq, EPO Espacenet, Google Patents. Many therapeutic antibody sequences appear first in patent filings; a patent is a disclosure, not peer-reviewed evidence, and sequence-to-molecule mapping in filings is frequently ambiguous.
