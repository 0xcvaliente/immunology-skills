---
name: antibody-reagent-selection
description: Choose and qualify a commercial research antibody - writing the spec, reading a datasheet, judging validation evidence against the five pillars, picking monoclonal or polyclonal, host and isotype, conjugates and secondary antibodies, planning controls, troubleshooting a failed Western blot, IHC, IF, ELISA, flow cytometry, IP or ChIP experiment, and reading SPR or BLI binding data (what a KD rests on, orientation, controls). Use when asked which antibody to buy or whether one is any good, when a datasheet or vendor claim needs assessment, or when an immunoassay gives no signal, extra bands, high background or an unexpected molecular weight. Validation is application-specific, so an antibody is only validated for the application, species and sample type it was tested in. Use antibody-literature-search to find published use of a clone, antibody-therapeutics-landscape for formats and vocabulary, antibody-binder-design when the antibody is to be designed rather than bought.
---

# Antibody reagent selection

Picking a research antibody and knowing what its datasheet does and does not promise. Selection narrows the field; the bench decides, so this skill ends at a shortlist plus a control plan, never at a guarantee.

## Validation is application-specific

"Validated" on a datasheet means tested in some application, in some species, on some sample type — frequently not yours. The claim that matters is the conjunction:

> this clone, in this application, on this sample type, from this species, at this expression level.

Every link must hold. An antibody that gives a beautiful overexpression blot can be useless at endogenous levels; one validated for ELISA may fail on a denatured target; a "human, mouse, rat" reactivity list is often sequence-homology prediction rather than data. Treat a reactivity claim without a figure as untested.

## Steps

### 1. Write the spec before shopping

Fix these before looking at any catalogue, because every later filter depends on them:

- **Target** — gene and protein name, species, and which isoform or domain. If the epitope must be extracellular (live-cell flow, cell-surface staining), say so now.
- **Application** — Western blot, IHC on FFPE or frozen, IF, flow, ELISA, IP, ChIP, multiplex.
- **Sample** — species, tissue or cell type, lysate or fixed section, expected expression level.
- **Format needs** — host species, clonality, isotype, conjugate (unconjugated, HRP, biotin, fluorophore), carrier-free if conjugating in-house.
- **Constraints** — multiplexing (no two primaries from the same host unless directly conjugated), secondary antibody availability, species-on-species staining, published-method compatibility, volume and budget.

### 2. Build a candidate list

Prefer clones with independent published use over clones with only vendor figures. Search the clone ID and the catalogue number in the literature (antibody-literature-search), look the clone up in the Antibody Registry for its RRID, and check whether multiple vendors resell the same clone — they frequently do, which makes vendor-specific claims less meaningful than clone-specific evidence.

### 3. Judge the evidence with the five pillars

The International Working Group for Antibody Validation's framework (Uhlén et al., *Nature Methods* 2016), to be applied per application:

1. **Genetic** — signal disappears in knockout or knockdown material.
2. **Orthogonal** — antibody-independent measurement (mass spectrometry, RNA-seq, qPCR) agrees.
3. **Independent antibodies** — a second antibody to a different epitope gives the same molecular weight and localisation.
4. **Tagged protein** — a tagged construct detected by both the antibody and a tag antibody.
5. **Biological** — a defined stimulus or treatment that changes target expression moves the signal as expected.

A knockout-validated figure in your application is worth more than every other claim on the page. Details of how to read the figures, and what a weak one looks like: [references/validation.md](references/validation.md).

### 4. Plan the controls before ordering

The controls are part of the selection decision, because an antibody whose specificity cannot be controlled in your system is the wrong choice. Control sets per application: [references/controls-and-troubleshooting.md](references/controls-and-troubleshooting.md).

### 5. Record what was used

Clone ID, vendor, catalogue number, **lot number**, RRID, dilution and incubation conditions. Lot matters most for polyclonals, where a new lot is a new reagent and can simply stop working. This record is what makes the experiment repeatable and a troubleshooting session tractable.

## Monoclonal, polyclonal, recombinant

| | Strength | Weakness |
|---|---|---|
| **Monoclonal** (hybridoma) | Single epitope, consistent between lots, defined | Can fail if the epitope is masked, fixed or mutated; one epitope means one point of failure |
| **Polyclonal** (serum) | Multiple epitopes, robust to fixation and denaturation, good for IP and low abundance | Lot-to-lot variation, finite supply, higher background, specificity hard to pin down |
| **Recombinant monoclonal** | Sequence-defined, renewable, animal-free, reproducible indefinitely | Price; still a single epitope |

Where a choice exists, a recombinant monoclonal with knockout validation in the target application is the default; reproducibility arguments in the field have moved firmly this way.

## Reference

- [references/applications.md](references/applications.md) — what each application demands of an antibody, and the gotchas particular to it, including SPR and BLI binding kinetics.
- [references/validation.md](references/validation.md) — reading a datasheet, the five pillars in practice, RRIDs, what good and bad validation figures look like.
- [references/controls-and-troubleshooting.md](references/controls-and-troubleshooting.md) — control sets, and symptom-to-cause tables for failed experiments.
