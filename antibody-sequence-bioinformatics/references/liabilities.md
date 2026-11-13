# Sequence liabilities and humanness

## Motifs worth flagging

Sequence-level flags, most consequential in CDRs and at exposed framework positions. A motif is a hypothesis about a risk, not a defect.

| Flag | Motif | Risk |
|---|---|---|
| N-linked glycosylation sequon | `N-X-S/T` where X is not Pro | Unwanted glycan in a CDR; heterogeneity, altered binding |
| Deamidation | `NG` (highest), then `NS`, `NT`, `NN`, `NH` | Charge change and activity loss on storage |
| Isomerisation | `DG` (highest), then `DS`, `DT`, `DD` | Isoaspartate formation, activity loss |
| Acid-catalysed cleavage | `DP` | Fragmentation, notably in the hinge |
| Oxidation | Exposed Met, Trp | Potency loss under light and peroxide stress |
| Free cysteine | Unpaired Cys | Mispairing, dimerisation, aggregation |
| Hydrophobic patch | Clusters of Trp, Phe, Leu, Ile, Val in CDRs | Aggregation, high viscosity, polyreactivity |
| Charge patch and extreme pI | Runs of Arg/Lys or Asp/Glu | Fast clearance, tissue binding, poly-specificity |
| N-terminal heterogeneity | Gln at position 1 | Pyroglutamate formation (usually tolerable) |

Rules for using them:

- Report position **with its numbering scheme**, the motif, and the region (CDR versus framework).
- Solvent exposure decides severity, so a structure or model changes the ranking. A buried `NG` is usually quiet; a `NG` in CDR-H3 rarely is.
- Empirical stress studies (heat, light, pH, oxidation) settle what prediction only suggests.
- Removing a liability costs affinity often enough that the mutation needs re-testing, not assuming.
- Liability panels differ between organisations; state which list was applied instead of implying a standard exists.

## Humanness and germline identity

- **Germline identity** — percentage identity of V region to the nearest human germline, reported per chain with the reference set named.
- **Humanness scores** — T20, OASis and similar metrics score against repertoire distributions; they are relative measures whose thresholds are conventions, so quote the method and the threshold with the number.
- **T-cell epitope prediction** — MHC class II binding predictions flag immunogenicity risk. Predictions are weakly correlated with clinical ADA, so treat them as a triage tool and defer to ex vivo assays and clinical data.
- A high humanness score does not predict low immunogenicity on its own; fully human antibodies raise ADAs too, and aggregation and dosing route often matter more than sequence.

## What sequence alone cannot decide

Be explicit about these limits when reporting a sequence-level analysis:

- **Whether it binds**, or what it binds. Specificity is not readable from sequence, and paratope prediction without structure is speculative.
- **Affinity.** No sequence feature gives a reliable KD.
- **Whether it will aggregate or be viscous.** Sequence flags correlate loosely; measurement decides.
- **Immunogenicity in patients.**
- **Expression titer and manufacturability.**
- **Epitope.** Mapping needs competition, mutagenesis or structure (see antibody-literature-search for the resources).

A sequence report that lists its flags, names its scheme and reference set, and states these limits is useful. One that converts flags into a verdict is not.
