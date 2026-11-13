# Template for the team's own skill

The site says a judge runs "your skill" on a case your team has not seen. This is a skeleton for that deliverable. **Create the real file in the submission repository on the day**, written for what your team actually built; copy only this structure, and only after checking with an organiser that prepared material is allowed (see the rules in `references/event-facts.md`). Replace every `<...>`; delete this paragraph.

Put the finished file at `skills/<team-skill-name>/SKILL.md` in the repository, with scripts beside it.

---

```markdown
---
name: <team-skill-name>
description: <One paragraph. What it designs (VHH / scFv / Fab binders), what it takes as input (target as UniProt accession, PDB id and chain, or sequence; objectives; limits), what it returns (ranked submission CSV, decision log, methods), and when to use it. Name the tools it needs.>
---

# <Team skill name>

## Inputs
Nothing about any one target is built in. The caller supplies:
- target: <accession | PDB id + chain | sequence>
- construct used by the assay: <residue range, tags removed>
- objectives: <each as a measurable condition>
- limits: <molecule classes, length range, number of designs, novelty rule>

## What it returns
- `submission.csv` (name, sequence, molecule_class; best first), `selection.csv` with metrics and reasons, `decision-log.md`, `methods.md`.

## Steps
1. <Intake: write task.md from the inputs. Done when ...>
2. <Dossier: ...>
3. <Generate: routes, counts, seeds. Done when ...>
4. <Score: predictors and metrics, with scales. Done when ...>
5. <Filter: rules in order, attrition table. Done when ...>
6. <Select: rule, diversity, per-design reason and risk. Done when ...>
7. <Verify: submission check passes. Done when ...>

## Requirements
Tools and versions, GPU or hosted service, credentials needed, expected runtime for a default run.

## Reproduce
One command, expected output, and where randomness enters (seeds).

## Limits
What it cannot do or predict, which objective types have no computational check, and what the held-out run showed.

## Evidence it generalises
The unseen-target run: which target, what changed in the inputs (only the inputs), what broke, what was fixed in the pipeline.
```
