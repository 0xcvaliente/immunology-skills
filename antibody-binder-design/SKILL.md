---
name: antibody-binder-design
description: Computational design of antibody-format binders (VHH/nanobody, scFv, Fab) against a given target, from the task text to a ranked, defensible submission - epitope choice, objectives such as cross-species or pH-selective binding turned into design levers, calibration on controls, two or more generation routes, co-folding and scoring (ipTM, ipSAE, pLDDT), filters, a diverse top-N with a decision log, submission CSV and methods. Use when asked to design, rank, filter or select nanobodies or antibody binders, to choose between design models (RFdiffusion, BoltzGen, RFantibody, Germinal, ProteinMPNN, Boltz, Chai, OpenFold, Protenix), to interpret confidence scores, to build a reproducible design pipeline or skill, or to prepare designs for wet-lab testing (Adaptyv, Proteinbase). Orchestrates the tool skills and MCP servers already connected; models screen, they do not measure binding. Use antibody-sequence-bioinformatics for numbering, CDRs, liabilities and contigs, antibody-literature-search for the target dossier, oslo-antibodies-hackathon for that event's rules, antibody-engineering to improve an antibody you already have.
---

# Antibody binder design

Take a task and a target to a ranked set of antibody-format designs and the evidence for choosing them. Nothing here predicts binding with confidence, so the product is **decisions with evidence**: the sequences, and the log that says why each was chosen and how it could be wrong.

## Working rules

- **Task text wins.** What the task says about the target construct, objectives, limits, format and novelty rule overrides every default below. Quote it in `task.md` before anything else.
- **Funnel.** Start wide, cut in order of cost, and record what each stage drops.
- **Tracer bullet.** Before scaling any one step, push about twenty designs through every step to a written `selection.csv`. A crude end-to-end run exposes the broken hand-off while there is still time to fix it.
- **Screen, not verdict.** Every in-silico metric is a filter. Agreement between independent methods is evidence; one model's high score is not; disagreement is information, so keep it visible.
- **Calibrate.** Cut-offs come from controls run through your own pipeline, not from papers about other targets or models.
- **Two routes.** At least two generation routes that fail differently and at least two independent scorers. Hit rate depends strongly on the target, so no single method can be trusted in advance.
- **Decision log.** Every choice (epitope, method, threshold, selection) is a dated line with its reason in `decision-log.md`. The log is a deliverable.
- **Unseen target.** A judge may run the pipeline on a target you have not seen. Target, epitope, objectives and limits are inputs; nothing about one target is written into the code.
- **Scope.** Therapeutic, diagnostic and research binders. Every design sent for synthesis is biosecurity-screened. A request for a binder that would enhance a pathogen's or toxin's harm, or help it evade a deployed countermeasure, is out of scope: say so and stop.

## Steps

Each step ends when its *done* line is true.

0. **Read the task.** Write `task.md`: target as given (accession, PDB and chain, or sequence), the construct the assay presents, each objective as a measurable condition, allowed molecule classes, length limits, number of designs, novelty rule (de novo only, or a starting binder allowed), submission format and deadline, how winners are decided, how binding is measured, any tag or construct restriction. *Done:* every field is filled from the task text or marked "not stated, assumed X because Y", and open questions are listed for the human.
1. **Survey the toolbox.** List connected MCP servers, installed skills (Adaptyv's `protein-design-skills`, the event's JapanFold, Nebius and Apheris integrations, anything local), GPUs and keys. Smoke-test each planned tool on a known complex. *Done:* `tools.md` has one row per stage (generator, co-folder, second co-folder, rescoring, developability) with tool, version, where it runs, limits and the smoke-test result. Tool parameters live in each tool's own skill or documentation; roles and caveats are in [references/models-and-metrics.md](references/models-and-metrics.md).
2. **Build the target dossier** with antibody-literature-search (`references/target-dossier.md` there). *Done:* it holds the exact construct and numbering, the best structures with their gaps and glycans, known binders with their epitopes, orthologs and isoforms that matter to the objectives, conformational states, and candidate epitopes.
3. **Choose epitopes and hotspots.** At least two distinct epitopes unless the task fixes one; each exposed in the assay construct (not buried, glycan-shielded, membrane-proximal or absent in the assay's conformation). *Done:* each epitope has residues in the structure file's numbering, a reason and a named risk.
4. **Turn each objective into a lever and a check** ([references/objectives.md](references/objectives.md)). *Done:* every objective has its measurable condition, design lever, computational proxy, and what would show the proxy is wrong.
5. **Calibrate.** Positive controls are known binders of this target or a close homolog (SAbDab-nano, the PDB, Proteinbase); negative controls are scrambled CDRs, designs for an unrelated target, or published non-binders. Run them through the same co-folding and scoring as the designs, then `scripts/rank_designs.py --controls`. *Done:* a table of metric, AUC and n is saved and the cut-offs are set from it. With no controls, write that in the log and rank without absolute cut-offs.
6. **Generate wide, by two or more routes.** Typical routes: de novo CDR design on a fixed framework with a nanobody-capable tool; framework-templated CDR redesign (`cdr_contig.py` in antibody-sequence-bioinformatics, then inverse folding); whole-binder diffusion. Vary seeds, epitopes, CDR3 lengths and frameworks. If the task requires de novo, zero-shot designs, never seed from a known binder of the target; known binders may still calibrate filters. *Done:* `designs.csv` holds hundreds of designs (size it from the throughput measured in step 1), each with `name, sequence, molecule_class, method, model_version, seed, params, epitope, framework`, and per-route counts are in the log.
7. **Fold and score.** Co-fold each design with the target construct under at least two independent predictors, keep raw outputs in `runs/`, and derive ipTM, ipSAE (the minimum of both directions), pLDDT, interface PAE and self-consistency RMSD; add hotspot coverage and CDR fraction from `interface_contacts.py`. *Done:* each design has every metric from each predictor or `NA` with a reason, the scale in the column name (`plddt_0_100`), and its structure files kept.
8. **Filter, cheapest first.** Validity and class (`scripts/check_submission.py designs.csv --max-designs 100000` for alphabet, length and class; `vhh_qc.py --annotate` for placement as a VH/VHH, canonical Cys pair, no odd Cys, hallmarks intact, no high-severity liability in a CDR), then interface (touches the intended epitope through the CDRs), then calibrated metric cut-offs, then novelty and diversity against known binders where required. *Done:* an attrition table (stage, count) is in the log and every dropped design has its failing rule recorded.
9. **Rank and select.** `scripts/rank_designs.py` with three or more metrics from two or more predictors, control-derived weights, `--diverse-col qc_cdr3` and `--max-per method=N`. Then look at the top picks by hand: the structure, the disagreement flags, the epitope. *Done:* `selection.csv` and its `.rule.json` exist; every selected design has a one-line reason and one named risk in the log; the final order is the submission order.
10. **Test on a case you have not tuned on.** Run steps 2 to 9 unchanged on a second target (a closed competition target works) and record what broke. *Done:* the pipeline ran end to end with only the task inputs changed; fixes go into the pipeline, never into the held-out result.
11. **Package and verify.** `scripts/check_submission.py` exits 0; `methods.md` and `README.md` written ([references/selection-and-submission.md](references/selection-and-submission.md)); a clean clone reproduces `selection.csv`, or a stated subset, with one documented command; versions, seeds and data licences recorded; no text addressed to the selector. *Done:* the clean-clone run matches.

## Guard rails

- Re-score after every sequence edit: a change that removes a liability can break the interface.
- Keep the fold intact: the canonical Cys23-Cys104 pair, the FR2 hallmark positions 42 and 52, and FR4. See antibody-sequence-bioinformatics `references/vhh.md`.
- Repeat across seeds and report the spread; a result seen once may be a lucky seed.
- Confidence is not affinity. pLDDT, ipTM and PAE say how sure a model is about geometry; a confident complex can still bind weakly, and confidence is least reliable at CDR3.
- A short list with reasons beats a long list of numbers.

## Reference

- [references/objectives.md](references/objectives.md) — objective types (cross-species, pH-selective, selectivity, mutation-specific, blocking, agonism), the lever and proxy for each.
- [references/models-and-metrics.md](references/models-and-metrics.md) — models by role, what each score means, thresholds and their provenance, reading a failing campaign.
- [references/selection-and-submission.md](references/selection-and-submission.md) — submission CSV, hard criteria, portfolio logic, decision-log and methods templates, repository layout, rules that can cost a team.
