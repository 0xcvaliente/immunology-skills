# Applications

Each application asks a different question of the same molecule. An antibody is a different reagent in each row below.

## Western blot

- **Epitope state** — denatured and reduced, so linear epitopes survive and conformational ones do not. An antibody raised against a folded ectodomain often fails here.
- **What good validation looks like** — a full-lane image, a single band at the predicted mass, and a knockout or knockdown lane.
- **Gotchas** — glycosylation, phosphorylation and proteolytic processing shift apparent mass; SDS-sensitive epitopes; reducing agents destroying disulfide-dependent epitopes; transfer efficiency falling off above ~150 kDa; membrane choice (PVDF versus nitrocellulose) and blocking agent (milk contains phospho-proteins and biotin, so use BSA for phospho-targets and for biotin-streptavidin detection).
- **Must record** — lysis buffer, reducing conditions, load per lane, dilution, blocking agent.

## Immunohistochemistry (FFPE and frozen)

- **Epitope state** — formalin cross-links and masks epitopes, so FFPE needs retrieval (heat-induced in citrate pH 6 or EDTA/Tris pH 9, or enzymatic). Retrieval conditions are part of the antibody's validation, not a detail.
- **What good validation looks like** — positive and negative tissue chosen on known expression, matched retrieval conditions, and a localisation pattern consistent with the protein's biology.
- **Gotchas** — frozen and FFPE validation do not transfer; endogenous peroxidase and biotin need quenching; edge artefacts and fixation gradients in large sections; nuclear staining from an antibody to a membrane protein is a red flag, not a discovery.
- **Must record** — fixation time, retrieval method and pH, detection system, counterstain.

## Immunofluorescence and confocal

- **Epitope state** — depends on fixation: paraformaldehyde preserves structure but masks some epitopes; methanol or acetone precipitates and permeabilises, destroying others. Test both.
- **Gotchas** — autofluorescence (lipofuscin, elastin, aldehyde-induced); bleed-through between channels; spectral overlap with the counterstain; permeabilisation required for intracellular targets, which rules out live-cell work.
- **Multiplex rule** — two unconjugated primaries from the same host cannot be distinguished by secondaries. Use different host species, directly conjugated primaries, or sequential staining with blocking.

## Flow cytometry

- **Epitope state** — native and usually on live cells, so the epitope must be extracellular and the antibody must work without fixation. Intracellular or phospho-targets need fix-and-perm kits whose conditions are antibody-specific.
- **What good validation looks like** — a histogram with a clearly separated negative population, isotype or better a knockout control, and titration data.
- **Gotchas** — Fc receptors on myeloid cells capturing antibody non-specifically (block with Fc receptor blocking reagent); dead cells binding everything (viability dye required); fluorophore brightness matched to antigen density, with the brightest dyes reserved for the dimmest markers; tandem dye degradation on light and freeze-thaw exposure; compensation needed for spectral overlap; enzymatic dissociation cleaving surface epitopes.
- **Must record** — fluorophore, clone, titration-determined dilution, blocking, viability dye, instrument configuration.

## ELISA and immunoassay

- **Format** — sandwich ELISA needs a **matched pair** binding non-overlapping epitopes, one for capture and one for detection; a single antibody cannot do both jobs on the same epitope.
- **Gotchas** — hook effect at high analyte; matrix effects from serum or plasma; the standard's identity (recombinant protein is not necessarily the native analyte); cross-reactivity with related family members, which must be tested explicitly for an assay claiming specificity.
- **Must record** — capture and detection pair with epitope regions, standard source, diluent, matrix.

## Immunoprecipitation and co-IP

- **Epitope state** — native, in lysate, and the epitope must remain accessible when the protein is in its complexes.
- **Choice** — polyclonals often outperform monoclonals here because multiple epitopes raise capture efficiency; for co-IP an antibody against a region inside the interaction interface will disrupt the complex it is meant to pull down.
- **Gotchas** — antibody heavy and light chains appearing at ~50 and ~25 kDa on the subsequent blot and masking targets there (use a different host for the blot, or conjugated beads and elution strategies); bead-only background; stringency trading yield against specificity.

## ChIP

- **Requirement** — the antibody must work on cross-linked chromatin, which is a distinct and demanding validation. "ChIP-grade" without a figure means nothing.
- **Controls** — IgG control, input, a known positive locus, and ideally knockout material.

## Multiplex and high-parameter (CyTOF, imaging mass cytometry, multiplex IF)

- Every antibody must be validated in the panel, not alone: steric interference, metal or fluorophore conjugation altering binding, and sequential-stripping damage all appear only in the full panel.
- Conjugation of a carrier-free antibody is its own optimisation; conjugation can and does kill binding.
