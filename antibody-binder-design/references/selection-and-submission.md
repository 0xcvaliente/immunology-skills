# Selection and submission

Facts here come from the Anthropic × Adaptyv Protein Design Competition pages (challenge FAQ, selection page and official terms) and the AI × Antibodies hackathon site, retrieved 2026-11-13. **The task you are given overrides all of it**: use this as the default shape and pass the task's own limits to the scripts.

## The submission file

A CSV, one design per row, **ordered by how you rank them** (best first), with at least:

| Column | Content |
|---|---|
| `name` | unique identifier |
| `sequence` | the designed protein, upper-case one-letter codes; a Fab is one string `VH:VL` |
| `molecule_class` | `protein`, `nanobody`, `scfv`, `fab_kappa` or `fab_lambda` |

Single-chain proteins are 10–250 residues. A design counts as a nanobody or antibody only if a numbering tool of the ANARCI family annotates it as one; for scFv the organisers may reformat the linker. Everything else is optional but encouraged: metrics (ipTM, ipSAE, self-consistency, physics scores, liability scores), structure models, and method details, either as extra columns or as a link to a repository. Anything submitted may be made public. `scripts/check_submission.py submission.csv --max-designs N` checks all of the above plus unique names and sequences, near-duplicates and residue validity.

**Do not write text addressed to the selector.** In the competition the pooled submissions and their notes are read by a Claude-based selection workflow whose prompt is public, and the FAQ states that embedded instructions or prompt injection may be grounds for disqualification. Describe the design (what it targets, how it was made, what the metrics are); never say what the reader should do with it. `check_submission.py` lints text columns for phrasing that addresses a reader.

## Hard criteria and what the selector weighs

From the FAQ (retrieved 2026-11-13), for the competition's tracks:

- Length and "nanobodyness" as above; every design unique.
- **De novo and zero-shot**: designs may not rely on an initial binder as a starting point, and need adequate sequence and structural diversity (CDR diversity for nanobodies and antibodies) from known proteins. Taking an existing binder and modifying it is not allowed. Using known binders to evaluate and calibrate filters, or to fine-tune models, is allowed, and common framework regions are the recommended starting point for nanobodies. Whether your task applies the same rule is a thing to read, not to assume.
- Beyond that, the public selection prompt weighs predicted design quality, design diversity and method novelty from "a small set of confidence metrics, with no single metric deciding", and takes several designs from each selected submission rather than one or two. It does not rank on one in-silico metric because most metrics do not account for the conditions set (for example pH). The page says: submit the designs you think will do best, in ranked order, and describe the method.

So: rank by your own best judgment, say how you ranked, and show diversity you chose on purpose.

## Choosing N designs

- Fill most of the list from the consensus top of the ranking (high on several independent metrics, interface on the intended epitope).
- Reserve a few places for deliberate exploration: a second epitope, a different CDR3 length class, a different generator. Label them as exploration, not as a mistake.
- Enforce distance on CDR3, not on the whole sequence (frameworks are shared by design): `rank_designs.py --diverse-col qc_cdr3 --min-distance 0.3`, plus `--max-per method=K` so one generator cannot fill the list.
- Look at the top designs by eye. A flagged disagreement between predictors goes in the log whether or not the design is picked.

## Decision log

An append-only `decision-log.md`. One entry per decision that changed what you did.

```markdown
## 2026-11-14 11:42  Epitope: second site on domain II
- Decision: add domain II as epitope E2 alongside the task's domain III.
- Why: dossier shows a published binder at III, so III-only designs risk resembling it (novelty rule); E2 is exposed in the assay construct.
- Evidence: dossier §3 (structure 6XXX, SASA), interface_contacts.py on 3 controls.
- Risk: no positive controls for E2, so calibration there is weaker.
- Reversible: yes (drop E2 designs at step 8).
```

Per selected design, one row in `selection.csv` (written by `rank_designs.py`) plus, in the log or the methods file:

```markdown
| name | route | epitope | key metrics (value, source) | flags | why it is here | named risk |
```

The "named risk" cell is not optional: a design with no stated way to fail has not been thought about.

## methods.md skeleton

1. **Task and constructs**: the task text, the target construct, numbering used.
2. **Tools and versions**: every model with version or commit, where it ran, seeds, parameters (the contents of `tools.md`).
3. **Controls and calibration**: which controls, the AUC table, the cut-offs derived.
4. **Generation**: each route, counts, what varied.
5. **Filters**: the attrition table and the rule that cut each design.
6. **Selection rule**: the contents of `selection.csv.rule.json`, in words.
7. **Limits**: what the metrics cannot see, what was not tested (for example pH behaviour), the held-out run from step 10 and what broke.
8. **Reproduce**: one command, expected runtime, expected outputs.
9. **Licences and attribution**: models, datasets, code reused.

## Repository layout

```
README.md              what it does, the one command, the expected result
task.md                step 0
decision-log.md        the log
tools.md               versions and smoke tests
methods.md
config/                target-specific inputs only (construct, epitopes, objectives)
src/ or scripts/       pipeline; no target-specific constants
runs/                  raw model outputs (or a manifest if too large)
designs.csv  selection.csv  selection.csv.rule.json  submission.csv
```

Pin versions (a lock file or container recipe), fix random seeds, and record the hardware class. Test the claim "a clean clone reproduces this" by doing it once.

## Rules and risks that can cost a team

- **Biosecurity.** Every design submitted for synthesis is screened, and a submission raising concern may be rejected or disqualified without explanation (competition terms, section 5.5).
- **Publication and IP.** Results for tested designs, with the sequence, predicted structure, design method, measurements, and the participant's name and team name, are published openly on Proteinbase under ODC-BY, including negative results; the sponsors receive a perpetual licence to publish, and the participant keeps ownership. Publication may affect patentability, and the terms put the responsibility for patent filings **before** submission on the participant (terms, section 6).
- **No guarantee of testing.** Submitting a design does not guarantee synthesis or a result.
- **Honesty about evidence.** Keep "predicted" and "measured" separate in every table, and say which objectives have no computational proxy.
