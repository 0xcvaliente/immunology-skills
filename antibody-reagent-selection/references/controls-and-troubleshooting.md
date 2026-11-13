# Controls and troubleshooting

## Control sets

| Control | What it rules out | Where it applies |
|---|---|---|
| No-primary (secondary only) | Secondary antibody binding directly, or detection-system background | IHC, IF, WB, flow |
| Isotype control, same host, same conjugate, same concentration | Fc-receptor and generic background. Weak evidence for specificity on its own | Flow, IHC, IF |
| Knockout or knockdown sample | Everything else; the strongest control available | all |
| Antigen-negative cell line or tissue | Target-independent signal | WB, IHC, IF, flow |
| Positive control with known expression | Protocol failure versus true negative | all |
| Peptide or antigen block / pre-absorption | Binding through the intended epitope — though it does not prove the signal was the target | IHC, IF, WB |
| Titration series | A dilution chosen by assumption | flow, IHC, IF, ELISA |
| Loading control (housekeeping protein, total protein stain) | Unequal load being read as regulation | WB |
| Input and IgG control | Bead and non-specific capture | IP, ChIP |
| Second antibody to a different epitope | Clone-specific artefacts | all |

A negative result is only interpretable with a positive control in the same run. A specificity claim is only interpretable with genetic or antigen-negative material.

## Western blot

| Symptom | Likely causes | Next step |
|---|---|---|
| No signal | Target not expressed in this sample; epitope destroyed by reduction or SDS; primary too dilute; transfer failed; target above transfer range; detection reagent expired | Run a positive control lysate; stain the membrane for total protein to confirm transfer; raise primary concentration and extend incubation to overnight at 4 °C |
| Band at the wrong mass | Glycosylation, phosphorylation, SUMO or ubiquitin modification; proteolytic processing; isoform; dimer or aggregate; incomplete reduction | Compare with the UniProt entry for predicted modifications and isoforms; deglycosylate; check the knockout lane to see which band is real |
| Multiple bands | Cross-reactivity; degradation; isoforms; splice variants; incompletely denatured sample | Add protease inhibitors and fresh lysis; knockout lane identifies the target band; try a second antibody to another epitope |
| High background | Insufficient blocking; primary or secondary too concentrated; inadequate washing; milk used with a phospho-target or with biotin detection | Switch blocking agent, dilute antibodies, lengthen washes |
| Speckles or blotchy areas | Aggregated antibody; dried membrane; dirty milk powder | Centrifuge or filter the antibody dilution; keep the membrane wet throughout |
| Ladder-like smearing | Overloaded lane; salt in sample | Reduce load; desalt |

## IHC and IF

| Symptom | Likely causes | Next step |
|---|---|---|
| No staining | Retrieval insufficient or wrong pH; epitope masked by fixation; target absent; overfixed tissue | Try both citrate pH 6 and EDTA/Tris pH 9; include a tissue known to be positive; test a frozen section |
| Uniform high background | Blocking inadequate; primary too concentrated; endogenous peroxidase or biotin unquenched; secondary cross-reacting with the tissue's own immunoglobulins | Quench, add serum block from the secondary's host species, titrate |
| Nuclear staining of a membrane protein (or any biologically implausible pattern) | Non-specific binding; retrieval artefact; wrong antibody | Treat as artefact until a knockout or antigen-negative control says otherwise |
| Edge-only or gradient staining | Fixation penetration gradient; section drying | Use thinner sections, keep hydrated |
| Autofluorescence | Aldehyde fixation, lipofuscin, elastin, erythrocytes | Quench with sodium borohydride or a commercial quencher; move the target to a red or far-red channel; acquire an unstained control |

## Flow cytometry

| Symptom | Likely causes | Next step |
|---|---|---|
| No separation from negative | Antigen density too low for the fluorophore; epitope cleaved by dissociation enzyme; wrong dilution | Move the marker to a brighter fluorophore; use gentler dissociation; titrate |
| Everything positive | Fc receptor binding; dead cells; excess antibody; compensation wrong | Fc block, viability dye, titrate, re-run compensation controls |
| Shifting results between runs | Tandem dye degradation; instrument drift; variable incubation | Protect tandems from light, run daily QC beads, fix incubation conditions |

## ELISA

| Symptom | Likely causes | Next step |
|---|---|---|
| Flat standard curve | Capture or detection antibody degraded; pair not matched; coating failed | Verify the pair binds distinct epitopes; re-coat; check plate type |
| High blank | Insufficient washing; detection reagent too concentrated; blocking agent incompatible | Add wash cycles, titrate detection, change blocker |
| Signal falls at high concentration | Hook effect | Dilute the sample series further and re-run |
| Sample values outside the curve in matrix | Matrix interference | Dilute in matrix-matched diluent; run a spike-recovery experiment |

## When troubleshooting stalls

Change one variable at a time and keep the positive control in every run. If three rounds of optimisation fail with controls behaving correctly, the hypothesis to test next is that the antibody does not work in this application — order a second clone from a different epitope region rather than optimising further.
