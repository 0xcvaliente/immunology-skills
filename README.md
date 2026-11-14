# immunology-skills

Claude Code skills for antibody work — the drug and business side, the literature, the bench reagent, the sequence data, engineering of existing antibodies, and computational design of nanobody and antibody binders — plus a brief for the AI × Antibodies hackathon in Oslo.

## The skills

| Skill | Covers |
|---|---|
| [`antibody-binder-design`](antibody-binder-design/SKILL.md) | Designing VHH, scFv and Fab binders against a target, from reading the task to a ranked, defensible submission: target dossier and epitope choice, objectives (cross-species, pH-selective, selectivity) turned into levers and checks, calibration on controls, two or more generation routes, co-folding and scoring, filters, a diverse top-N with a decision log, submission CSV and methods. Scripts: `rank_designs.py`, `check_submission.py`. |
| [`antibody-engineering`](antibody-engineering/SKILL.md) | Improving an antibody, scFv or VHH you already have: humanisation, affinity maturation, stability and solubility, developability, immunogenicity risk. An eight-step workflow with calibration on known data, plus a tool map by stage (numbering and germline, structure and complex prediction, docking, mutation scoring by physics, inverse folding and language models, generative redesign, developability, T-cell epitope prediction) with every link and paper verified. |
| [`antibody-sequence-bioinformatics`](antibody-sequence-bioinformatics/SKILL.md) | Sequence, VHH and structure data: IMGT/Kabat/Chothia/Martin numbering, CDR boundaries, ANARCII/ANARCI/abnumber/IgBLAST, VHH hallmark residues, AIRR Rearrangement TSV, clonotype definitions, liability motifs and humanness. Scripts: `vhh_qc.py`, `cdr_contig.py`, `interface_contacts.py`. |
| [`antibody-literature-search`](antibody-literature-search/SKILL.md) | Finding and summarising papers and database records: Europe PMC, PubMed, UniProt, PDB, SAbDab(-nano), Thera-SAbDab, IMGT, OGRDB, Proteinbase, trial registries, patent sequences, with every identifier resolved before it is cited; a target-dossier procedure for an unseen target. |
| [`antibody-therapeutics-landscape`](antibody-therapeutics-landscape/SKILL.md) | Antibodies as medicines: IgG subclasses, fragments, VHHs as drugs, bispecifics, ADCs, Fc engineering, INN name decoding, the discovery-to-approval path, regulatory routes (US, EU, Norway), CMC and commercial vocabulary; user fit and path to value for a design tool; biotech employer research and interview prep. |
| [`antibody-reagent-selection`](antibody-reagent-selection/SKILL.md) | Choosing and qualifying a research antibody: writing the spec, reading a datasheet, the five validation pillars, per-application requirements (WB, IHC, IF, flow, ELISA, IP, ChIP, SPR/BLI), control sets and troubleshooting tables. |
| [`oslo-antibodies-hackathon`](oslo-antibodies-hackathon/SKILL.md) | The AI × Antibodies hackathon, Oslo, 14 November 2026: schedule, the four judging criteria, rules that can cost a team, provided tools and prize conditions, the PDB 1ZVY practice tutorial with verified numbers, a preparation checklist, a day plan, the pitch. Perishable: delete it after the event. |

Each skill keeps its steps in `SKILL.md` and pushes the tables and detail into `references/`, loaded only when needed.

## Install

```bash
git clone https://github.com/0xcvaliente/immunology-skills.git
cd immunology-skills
./install.sh          # copies every skill into ~/.claude/skills (re-run after a git pull)
./install.sh --link   # or symlink them, so the clone is the single source
```

The script only touches directories in this repository that contain a `SKILL.md`, and says what it replaced. All seven skills are model-invoked, so Claude reaches them on its own when a prompt matches their description; they can also be invoked by name. A copy installed earlier and then edited elsewhere drifts from the repository, which is why the script exists: install from the repository, edit in the repository.

## Scripts and tests

Standard library only, Python 3.9 or newer, nothing to install; `--help` on each.

| Script | Does |
|---|---|
| `antibody-sequence-bioinformatics/scripts/vhh_qc.py` | IMGT regions, hallmark residues, cysteines, liabilities, charge and size for VH/VHH sequences; `--annotate` adds `qc_*` columns to a design table; `--numbering anarcii` for exact numbering |
| `antibody-sequence-bioinformatics/scripts/cdr_contig.py` | CDRs mapped to a structure's own residue numbers, and a loop-redesign contig |
| `antibody-sequence-bioinformatics/scripts/interface_contacts.py` | Interface contacts, hotspot coverage and CDR contribution for predicted complexes |
| `antibody-binder-design/scripts/rank_designs.py` | Hard filters, multi-metric rank aggregation with a disagreement flag, control-based calibration, a diversity-aware shortlist, and a rule file recording how it was made |
| `antibody-binder-design/scripts/check_submission.py` | Validates a submission CSV (columns, classes, residues, lengths, duplicates, Fab format, text addressed to the selector) |
| `oslo-antibodies-hackathon/scripts/read_guide.py` | Re-reads the live hackathon guide and event site and diffs them against the snapshot the skill was written from |

```bash
python3 -m unittest discover -s tests -v     # no network; a few seconds
```

`vhh_qc.py`'s region placement was measured against ANARCII on four sets of PDB sequences: 417 of 419 heavy-chain domains placed, none of 59 light chains or shark VNARs wrongly accepted, 99.3–100% identical regions. Details and limits: [`vhh.md`](antibody-sequence-bioinformatics/references/vhh.md). The 1ZVY tutorial contig from the hackathon guide is reproduced exactly by `cdr_contig.py` and is part of the tests.

## Hackathon

[`oslo-antibodies-hackathon`](oslo-antibodies-hackathon/SKILL.md) starts with `python3 oslo-antibodies-hackathon/scripts/read_guide.py --diff`, because the organisers say weights and model access may still change and that the task itself is released at 09:30 on the day. The design workflow it points to is [`antibody-binder-design`](antibody-binder-design/SKILL.md).

**For agents.** [`AGENTS.md`](AGENTS.md) covers working in this repository (loaded automatically through `CLAUDE.md`); the [agent runbook](oslo-antibodies-hackathon/references/agent-runbook.md) covers running the day: who decides what, which repository gets what, when to stop and ask, and starter prompts.

**Rules note.** The event's FAQ says: "All project outputs and repositories must be created during the hackathon." These skills are prepared tooling and knowledge, not a submission. Disclose them to the organisers, ask whether they may be used, and create the team's repository, and the team's own skill, on the day. A skeleton for that skill is in `oslo-antibodies-hackathon/assets/team-skill-template.md`.

## Conventions

Four rules carry most of the value and are enforced in the skill text itself:

- **Volatile facts get looked up.** Approval counts, pipelines, ownership and company facts are never answered from memory — the skill names the source and asks for a retrieval date.
- **Every identifier resolves.** No PMID, DOI, accession, PDB ID or catalogue number is written without being fetched first.
- **Sources are primary and versioned.** Facts come from the registry, sequence or structure record itself rather than a secondary summary, and a versioned resource is cited with its release and retrieval date — database content changes between releases.
- **Coordinates and validation carry their qualifiers.** A residue number travels with its numbering scheme; a validated antibody is validated for a named application, species and sample type, and nothing beyond it.

The design skills add a stance: **models screen, they do not measure binding**, so the product is decisions with evidence, thresholds come from controls run through your own pipeline, and every placement the scripts cannot make is reported as unplaced rather than guessed.

Written to the `writing-for-agents` conventions: steps in the main file, reference behind pointers, one source of truth per fact.

## Sources

The skills point at primary, maintained repositories only — Europe PMC and PubMed (NLM), UniProt, RCSB PDB and PDBe, IEDB (NIAID), SAbDab / SAbDab-nano / Thera-SAbDab / OAS / PLAbDab (OPIG, Oxford), IMGT and IMGT/mAb-DB (CNRS), OGRDB and the AIRR Standards (AIRR Community), iReceptor and VDJbase, Proteinbase (Adaptyv), SKEMPI 2.0 and AB-Bind, ClinicalTrials.gov, EU CTIS and WHO ICTRP, the Antibody Society and YAbS, the WHO INN Programme, Cellosaurus, the Antibody Registry (RRID) and CiteAb. The full list, with endpoints, is in [`antibody-literature-search/references/resources.md`](antibody-literature-search/references/resources.md). Event facts come from the organisers' own pages and are dated in [`event-facts.md`](oslo-antibodies-hackathon/references/event-facts.md).

## Scope

Research, therapeutic, diagnostic and educational use. Not medical advice, and not a substitute for bench validation — the reagent skill ends at a shortlist and a control plan, and the design skills end at a ranked list of candidates to test.
