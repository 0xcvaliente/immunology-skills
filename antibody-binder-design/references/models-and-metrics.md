# Models and metrics

Roles first, then what each score does and does not mean. Availability changes by event and by day: confirm in step 1 of the workflow what is actually connected before planning around a model. Sources: the AI × Antibodies participant guide (retrieved 2026-11-13), Adaptyv's open `protein-design-skills` pack (MIT, `github.com/adaptyvbio/protein-design-skills`, retrieved the same day), and the papers named below. Read a tool's own skill or documentation for parameters; this file does not copy them.

## Models by role

| Role | Models named by the guide or the Adaptyv pack | Notes |
|---|---|---|
| Co-folding: structure of the complex | OpenFold3, RoseTTAFold3, Boltz-2, Protenix(-v2), Chai-1, AlphaFold2/3, OpenDDE | Use at least two from different families for consensus. OpenDDE has an antibody–antigen-tuned checkpoint; its authors' gains over AlphaFold3 are self-reported, so test whether they include nanobodies before trusting it. Boltz-2's affinity head was trained on protein–small-molecule data and is not a VHH–antigen affinity predictor. |
| Structure of the binder alone | NanoBodyBuilder2, ABodyBuilder3, ESMFold(-2) | Fast first look; ESMFold needs no alignment. A single VHH folds well apart from CDR3. |
| Design: generate binders or CDRs | RFdiffusion(3), RFantibody, BoltzGen, PXDesign, IgDiff, Germinal, mBER, RFD4-Proteina | Germinal designs nanobody and scFv CDRs on a fixed framework (hallucination plus AbMPNN plus co-folding); Adaptyv's pack calls it the antibody-format option, not a default, and notes it can be finicky. RFD4-Proteina is the JapanFold diffusion tool in the guide's tutorial, driven by a contig. |
| Sequence for a given backbone | ProteinMPNN, LigandMPNN, SolubleMPNN, AntiFold, ESM-IF | A backbone-only generator still needs this step before a sequence exists. |
| Rescoring an existing design | AF2 initial-guess (AF2-IG), ipSAE | Independent of the generator, which is why it is useful as a second opinion. |
| Embeddings and sequence plausibility | ESM-2, ESMC, SaProt, nanoBERT, IgBERT | One-hot encoding is a fair baseline and sometimes wins. |
| Developability | TNP (nanobodies), TAP, SoluProt, NetSolP, Aggrescan3D, ThermoMPNN, `vhh_qc.py` motifs | Predictions, not measurements; see antibody-sequence-bioinformatics. |
| Physics | FoldX, Rosetta, MM/GBSA, FEP/TI | Seconds for the empirical scores, hours to days per variant for FEP; fitted on compact globular proteins, so a long CDR3 is a poor fit. Rank-only at best. |

No model in these tables predicts affinity for a new VHH–antigen pair. The guide places "rank mutations by affinity" at the weak end of what AI does today, with classical scoring functions around Pearson 0.3–0.5 on antibody ΔΔG benchmarks built mainly on conventional antibodies.

## What the scores mean

| Metric | Meaning | Scale and traps |
|---|---|---|
| **pLDDT** | Confidence in the local structure | 0–100 in AlphaFold-family output; some pipelines report 0–1. Record the scale in the column name. CDR3 is the low point of a VHH, which is normal. |
| **PAE** | Predicted error in relative position of residue pairs, in Å | Lower is better. The interface block (binder rows against target columns) is the useful part. |
| **ipTM** | Confidence in the relative placement of chains | 0–1. Diluted by disordered or accessory regions, so a large flexible target can depress it. |
| **ipSAE** | Interface score built from the PAE, intended to fix ipTM's dilution (Dunbrack, bioRxiv 2025, [doi:10.1101/2025.02.10.637595](https://doi.org/10.1101/2025.02.10.637595)) | Computed per direction; **ipSAE_min** is the lower of the two. It depends on a PAE cut-off the tool takes as a parameter (its own examples use 10 for AlphaFold3 and Boltz and 15 for AlphaFold2), so record the cut-off with the number. Implementations vary. Compute it with the author's script (`github.com/DunbrackLab/IPSAE`, which Adaptyv's `ipsae` skill wraps), feeding it the predictor's PAE file and structure. |
| **Self-consistency RMSD** | Does the sequence re-fold to the backbone it was designed for | Å; lower is better. A design that does not re-fold to its own backbone was not specified by its sequence. |
| **DockQ** | Accuracy of a predicted complex against a reference | Bands 0.23 acceptable, 0.49 medium, 0.80 high (CAPRI). Needs a reference, so it applies to controls, not to new designs. |
| **Interface contacts, hotspot coverage, CDR fraction** | Where the design touches the target | `interface_contacts.py`. Geometry, not energy. |

**Confidence is not affinity.** A confident complex can still bind weakly, and confidence is least reliable exactly where prediction is hardest, at CDR3 and at novel epitopes (guide, "A word of caution").

## How much the metrics predict

- Adaptyv's `protein-qc` skill summarises single metrics as weak (ipTM and PAE around AUC 0.64–0.66, ESM-2 pseudo-likelihood about 0.72, composites about 0.75) and says metrics work as filters that remove failures, not as predictors that rank successes. This is a secondary summary of unspecified data, so use it as a prior, not a fact.
- A meta-analysis of 3,766 experimentally characterised de novo binders across 15 targets (Overath et al., bioRxiv 2025, [doi:10.1101/2025.08.14.670059](https://doi.org/10.1101/2025.08.14.670059)) is reported, through that same skill, to find AlphaFold3 ipSAE_min the best single in-silico predictor, with 0.61 as a useful threshold. Those binders are mostly not antibodies. Read the preprint before quoting the figure, and calibrate on VHH controls.

## Thresholds, and where they come from

Adaptyv's pack publishes working thresholds for generic de novo binders. They are a reasonable first guess and nothing more: antibody CDR loops are flexible, and the guide warns that models trained on general protein data transfer poorly to them.

| Metric | Standard | Stringent | Note |
|---|---|---|---|
| pLDDT | > 0.85 | > 0.90 | On a 0–1 scale; multiply by 100 for AlphaFold-style output |
| ipTM | > 0.50 | > 0.60 | |
| ipSAE_min | > 0.61 | > 0.70 | AlphaFold3 or Boltz output, PAE cut-off recorded |
| Interface PAE | < 12 Å | < 10 Å | |
| Self-consistency RMSD | < 2.0 Å | < 1.5 Å | |
| Pass rate to expect | 10–15% through a full filter set | | Under 5% or over 50% means a problem: see below |

Values are from the pack's `protein-qc` skill. Its pipeline document lists slightly different numbers for ipTM (0.5 standard, 0.7 stringent) and interface PAE (10 Å and 5 Å), a reminder that these are conventions and not constants.

Replace these with cut-offs taken from your controls (step 5). If you cannot, rank by aggregated rank and say so; a rank carries no threshold to defend.

## Reading a failing campaign

| Symptom | Likely cause | Next step |
|---|---|---|
| Nearly everything fails pLDDT | Backbones strained, or sequences do not specify the fold | Lower diffusion noise, sample more sequences per backbone, check the scale (0–1 versus 0–100) |
| Nearly everything fails ipTM | Hotspots not exposed, or an epitope the models do not recognise | Try other hotspot sets; check the epitope in the assay construct; try a second co-folder |
| High ipTM but the wrong epitope | The predictor found a different contact | Filter on hotspot coverage, not on ipTM alone |
| Everything passes (over 50%) | Cut-offs too lax, monomers being scored, or duplicates | Check that complexes are predicted; deduplicate; use control-derived cut-offs |
| Predictors disagree on the pose | The epitope or CDR3 is hard for these models | Keep as a flagged design only if the objective needs it; do not average the disagreement away |
| Good metrics, no hits afterwards | In-silico metrics do not capture the assay's conditions | Generate more, diversify, and say what the metrics cannot see |

## Consensus between predictors

Two predictors that agree on the epitope are better evidence than one confident score. A cheap measure: run `interface_contacts.py` on each predictor's complex and compare the sets of target residues in contact (Jaccard overlap). Treat the overlap as a heuristic, calibrate it on controls, and report it as "epitope agreement" rather than as a probability.
