# immunology-skills

Claude Code skills for antibody work — the drug and business side, the literature, the bench reagent, and the sequence data.

## The skills

| Skill | Covers |
|---|---|
| [`antibody-therapeutics-landscape`](antibody-therapeutics-landscape/SKILL.md) | Antibodies as medicines: IgG subclasses, fragments, bispecifics, ADCs, Fc engineering, INN name decoding, the discovery-to-approval path, regulatory routes (US, EU, Norway), developability, CMC and commercial vocabulary, plus biotech employer research and interview prep. |
| [`antibody-literature-search`](antibody-literature-search/SKILL.md) | Finding and summarising papers and database records: Europe PMC, PubMed, UniProt, PDB, SAbDab, Thera-SAbDab, IMGT, OGRDB, trial registries, patent sequences — with every identifier resolved before it is cited. |
| [`antibody-reagent-selection`](antibody-reagent-selection/SKILL.md) | Choosing and qualifying a research antibody: writing the spec, reading a datasheet, the five validation pillars, per-application requirements (WB, IHC, IF, flow, ELISA, IP, ChIP), control sets and troubleshooting tables. |
| [`antibody-sequence-bioinformatics`](antibody-sequence-bioinformatics/SKILL.md) | Sequence and repertoire data: IMGT/Kabat/Chothia/Martin numbering, CDR boundaries, ANARCI, abnumber, IgBLAST, AIRR Rearrangement TSV, clonotype definitions, QC, liability motifs and humanness. |

Each skill keeps its steps in `SKILL.md` and pushes the tables and detail into `references/`, loaded only when needed.

## Install

Copy or symlink into your personal skills directory:

```bash
git clone https://github.com/0xcvaliente/immunology-skills.git
cd immunology-skills
for s in antibody-*; do ln -s "$PWD/$s" ~/.claude/skills/"$s"; done
```

All four are model-invoked, so Claude reaches them on its own when a prompt matches their description; they can also be invoked by name.

## Conventions

Four rules carry most of the value and are enforced in the skill text itself:

- **Volatile facts get looked up.** Approval counts, pipelines, ownership and company facts are never answered from memory — the skill names the source and asks for a retrieval date.
- **Every identifier resolves.** No PMID, DOI, accession, PDB ID or catalogue number is written without being fetched first.
- **Sources are primary and versioned.** Facts come from the registry, sequence or structure record itself rather than a secondary summary, and a versioned resource is cited with its release and retrieval date — database content changes between releases.
- **Coordinates and validation carry their qualifiers.** A residue number travels with its numbering scheme; a validated antibody is validated for a named application, species and sample type, and nothing beyond it.

Written to the `writing-for-agents` conventions: steps in the main file, reference behind pointers, one source of truth per fact.

## Sources

The skills point at primary, maintained repositories only — Europe PMC and PubMed (NLM), UniProt, RCSB PDB and PDBe, IEDB (NIAID), SAbDab / Thera-SAbDab / OAS / PLAbDab (OPIG, Oxford), IMGT and IMGT/mAb-DB (CNRS), OGRDB and the AIRR Standards (AIRR Community), iReceptor and VDJbase, ClinicalTrials.gov, EU CTIS and WHO ICTRP, the Antibody Society and YAbS, the WHO INN Programme, Cellosaurus, the Antibody Registry (RRID) and CiteAb. The full list, with endpoints, is in [`antibody-literature-search/references/resources.md`](antibody-literature-search/references/resources.md).

## Scope

Research, therapeutic, diagnostic and educational use. Not medical advice, and not a substitute for bench validation — the reagent skill ends at a shortlist and a control plan.
