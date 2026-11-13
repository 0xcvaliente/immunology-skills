# Target dossier

A time-boxed profile of one target, built before any design or reagent choice. In under an hour it should tell you where binding is possible, what to avoid, what already exists, and why anyone would care. antibody-binder-design uses it at step 2; the same content feeds "user fit" and "path to value" in a pitch.

Run the lookups in parallel, resolve every identifier before writing it (see the main skill), and stop each step at its *done* line. A dossier with gaps that are named is more useful than a long one with guessed entries.

## Steps

1. **Pin the construct.** Take the exact sequence the assay uses (from the task) and map it to UniProt: accession, isoform, and the offset between the construct's numbering, UniProt's and the structure file's. UniProt's feature table gives signal peptide, domains, transmembrane segments, glycosylation sites and disulfides. *Done:* a small table mapping UniProt residue, construct residue and structure residue for every candidate epitope.
2. **Find structures.** Search the PDB by UniProt accession; use SAbDab or SAbDab-nano to see which entries already hold an antibody or nanobody. Note resolution, construct boundaries, missing residues (REMARK 465 in a PDB file), glycans, ligands and oligomeric state, and which conformational state each shows. With no experimental structure, take the AlphaFold DB model and label it a prediction. *Done:* a ranked list of structures with chain IDs, residue ranges and gaps, and the one chosen for design with the reason.
3. **List known binders and epitopes.** Antibody and nanobody complexes (SAbDab), epitopes recorded in IEDB, therapeutic antibodies against the target (Thera-SAbDab, YAbS, the Antibody Society table), and what the literature says about epitope mapping. *Done:* a table with binder, format, epitope (residues or domain), evidence and source ID. This is the source of positive controls for calibration.
4. **Compare orthologs, isoforms and paralogs** when an objective mentions species or selectivity. Align the sequences and mark which candidate-epitope residues are conserved. *Done:* a conservation track over each candidate epitope, or a statement that no objective needs it.
5. **Assess each candidate epitope's accessibility in the assay construct.** Relative solvent accessibility from the chosen structure, N-glycan sequons (`N-X-S/T`) and known glycosylation near the site, membrane proximity, oligomer interfaces, flexible or disordered stretches. *Done:* each candidate has an exposure statement and its main risk.
6. **Collect context** for the pitch: what the target does, which disease it matters in, expression in healthy tissue (Human Protein Atlas) and so known on-target risk, approved or trial-stage drugs against it (ClinicalTrials.gov, labels), and what standard of care already gives patients. *Done:* five lines, each with a source.

## Output template

```markdown
# Target dossier: <name> (UniProt <accession>, retrieved <date>)

## Construct and numbering
<construct as given; mapping table>

## Structures
<ranked list; chosen structure and why; gaps>

## Known binders and epitopes
| binder | format | epitope | evidence | source |

## Orthologs, isoforms, paralogs
<alignment summary; conserved and variable epitope residues>

## Candidate epitopes (ranked)
| epitope | residues (structure numbering) | exposure | reason | risk |

## Context
<function, disease, expression, existing drugs, standard of care>

## Sources
<every identifier with its retrieval date>
```

## What to keep out

A claim about an epitope that rests only on a predicted structure is labelled as a prediction. A structure of the target bound to a ligand or partner is not evidence that the free target adopts that state in the assay. A published binder's epitope is a hint about what is accessible, not a recommendation to copy it, and where the task requires de novo designs it is a reason to look for a second site.
