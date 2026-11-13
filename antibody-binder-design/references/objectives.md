# Objectives

A task rarely says "make a binder". It says what the binder must do under the assay's conditions, and a design is judged on that. Step 4 of the workflow turns each objective into four things; this file is the catalogue of patterns.

| Field | Meaning |
|---|---|
| **Condition** | The measurable statement, in the assay's own terms |
| **Lever** | What in the design can change the outcome |
| **Proxy** | The computation that stands in for the measurement |
| **Falsifier** | What would show the proxy is not tracking the objective |

Evidence labels below: **(page)** comes from a published challenge or guide; **(practice)** is general design practice offered as a starting hypothesis. Both are to be checked against the task in front of you.

## What the assay measures

In the Anthropic × Adaptyv competition the EGFR page states the readout (page, retrieved 2026-11-13): each tested design is measured under each condition with the design immobilised and the target in solution; a design counts as binding in a condition when its sensorgram gives a fittable curve and a KD, or, where the curve cannot be fitted, when the association shift clears 300% over the negative control; otherwise "no detectable binding". The target's purification tags and the design's own capture tag are off limits, so binding to a tag does not count. Read the equivalent section of your task: it fixes what "binds" means, and designs should be judged against that, not against an affinity number.

## Patterns

### Binding a defined epitope
- **Condition:** binds the target construct, ideally at a named functional region (the EGFR page recommends domain III, which cetuximab and panitumumab also target; (page)).
- **Lever:** hotspot residues and epitope choice; CDR3 length; framework.
- **Proxy:** predicted complex whose interface covers the hotspots (`interface_contacts.py` hotspot coverage) with consistent interfaces across two predictors.
- **Falsifier:** high confidence but the interface sits elsewhere; predictors disagree on the pose.

### Cross-species reactivity (for example human and mouse ortholog)
- **Condition:** measurable binding to both orthologs, sometimes ranked by how close the two KDs are (page).
- **Lever:** an epitope conserved between the species; avoid residues that differ.
- **Proxy:** align the orthologs, mark which epitope residues differ, and require the designed interface to avoid them; co-fold against both and require the same pose.
- **Falsifier:** the ortholog differs in a surface loop the interface depends on; the second co-fold changes the pose.

### pH-selective binding (binds at tumour-like pH, not at blood pH)
- **Condition:** a measurable KD at the acidic pH and no detectable binding at the neutral pH (page: EGFR at pH 6.5 versus 7.4, the acidic value standing for the tumour microenvironment).
- **Lever (practice):** histidine at the interface. Histidine's side chain is mostly neutral at pH 7.4 and increasingly protonated and positive toward pH 6, and the local environment at an interface can shift its pKa by a unit or more; the guide's histidine widget makes the same point and adds that a switch between blood and endosome (pH 5.5–6) is sharp while one between blood and a tumour (about 6.7) is much weaker, so tumour-selective designs need more care. Paired charges that change with protonation are the other lever.
- **Proxy:** count interface histidines (`vhh_qc.py` reports His in CDRs and net charge at pH 7.4 and 6.5); an electrostatics or pKa calculation on the predicted interface at both pH values.
- **Falsifier:** **co-folding models do not model protonation or pH**, so their scores are blind to this objective. Do not read a high ipTM as evidence of a pH switch. Without a protonation-aware calculation the honest claim is "designed for a His-mediated switch, not computationally verified".

### Selectivity over a paralog or isoform
- **Condition:** binds the target, does not bind the related protein.
- **Lever:** an epitope on a non-conserved surface.
- **Proxy:** co-fold each design against the target and against the paralog; keep designs that score well on the first and clearly lower on the second; mark conservation on the epitope.
- **Falsifier:** the paralog scores nearly as well; the predictor is overconfident on both.

### Mutation-specific or peptide-specific binding (for example a peptide–MHC neoantigen)
- **Condition:** binds the mutant presentation and not the wild-type one.
- **Lever (practice):** contacts to the mutated residue; avoid a surface shared with the wild type.
- **Proxy:** co-fold with the mutant and wild-type peptide; require a contact to the changed position and a clear score gap.
- **Falsifier:** the model places the same pose for both; the difference rests on a single side chain that the predictor does not resolve. Expect this to be the weakest in-silico proxy.

### Blocking a ligand or partner
- **Condition:** binding that prevents the natural interaction (a competition assay in the lab).
- **Lever:** an epitope overlapping the partner's interface.
- **Proxy:** superpose the known partner complex on the target and test for steric overlap with the designed binder.
- **Falsifier:** the partner binds a different conformation than the structure you used.

### Function, such as agonism
- **Condition:** a cellular or signalling readout, not binding alone.
- **Lever (practice):** orthosteric epitope, valency and geometry (a bivalent or biparatopic format can cluster a receptor).
- **Proxy:** none that is reliable. A structure-based design can reach the right site; whether it activates is not predicted by confidence scores. State plainly that binding is the testable part.

### Conformation-specific binding
- **Condition:** binds one state (open or closed, monomer or oligomer).
- **Lever:** an epitope that exists only in that state.
- **Proxy:** use the structure of the target state in the assay; check the epitope is exposed in it and not in the other.

## Worked reading: the Anthropic × Adaptyv challenge set

The competition page lists five challenges, all closed by 9 November 2026: a conditional EGFR binder, a conditional TNF-α binder, a GLP1R agonist, a conditional TfR1 binder, and a mutation-specific peptide–MHC binder (KRAS G12D). The EGFR page spells out what "conditional" meant there: three objectives (binding human EGFR, mouse cross-reactivity, pH-selective binding), the winner having to clear all three and designs ranked by pH selectivity first, then mouse cross-reactivity, then affinity (page). Each challenge page publishes its target sequence, a structure reference and its ranking rules, so the closed pages are realistic unseen cases for step 10 of the workflow. The other four pages state their own conditions; read them rather than assuming they match EGFR.

## Writing it down

For each objective, one row in `task.md`:

```
| Objective | Condition (assay terms) | Lever | Proxy | Falsifier |
```

An objective with no usable proxy still gets a row: say what the design does about it and that the evidence is by construction, not by computation. Judges reward that clarity more than an unsupported score.
