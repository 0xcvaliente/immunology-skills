# Formats

## Anatomy

A full IgG is two heavy chains and two light chains: ~150 kDa, Y-shaped, two identical binding arms.

- **Variable domains** VH and VL pair to form the **Fv**, the binding unit. Each carries three **CDRs** (complementarity-determining regions) on a scaffold of four framework regions. CDR-H3 is the most diverse and usually contributes most of the binding energy.
- **Fab** = VH + CH1 + VL + CL, one binding arm. **F(ab')2** = both arms, hinge intact, no Fc. **Fc** = CH2 + CH3, the half that talks to the immune system and to FcRn.
- The **hinge** sets arm flexibility and is the main proteolysis and fragmentation site.
- A conserved N-glycan at heavy-chain **N297** (EU numbering) governs Fcγ-receptor engagement. Its composition, especially core fucose, moves effector potency.
- **Paratope** is the antibody's binding surface; **epitope** is the patch on the antigen. Conformational epitopes vanish when the antigen is denatured — the reason a reagent validated for ELISA may fail on a Western blot.

## IgG subclasses

Human therapeutics are nearly always IgG. The subclass is a deliberate choice about effector function.

| Subclass | Effector function | Typical use | Notes |
|---|---|---|---|
| IgG1 | Strong ADCC, ADCP and CDC | Default for depleting antibodies | Best characterised, longest manufacturing track record |
| IgG2 | Weak ADCC, weak CDC | Blocking without effector killing | Disulfide isoform heterogeneity complicates analytics |
| IgG3 | Strongest CDC, long hinge | Rare in therapeutics | Shorter half-life, allotype variability, awkward purification |
| IgG4 | Weak effector recruitment | Blockade where killing is unwanted | Fab-arm exchange is suppressed with the S228P hinge mutation |

Half-life for an unengineered human IgG1 in humans is roughly three weeks, set by pH-dependent FcRn recycling. Fragments lacking Fc clear in hours to days.

## Fragments and small formats

| Format | Size | Why choose it | Cost |
|---|---|---|---|
| Fab, Fab' | ~50 kDa | Monovalent, no effector function, better tissue and tumour penetration | Short half-life, no FcRn recycling |
| F(ab')2 | ~100 kDa | Bivalent, effector-silent | Hinge fragility |
| scFv | ~25 kDa | Modular building block for bispecifics and CAR binders | Aggregation and diabody formation; linker length (typically 15–25 residues) tunes this |
| sdAb / VHH / nanobody | ~15 kDa | Camelid single domain; reaches cryptic and concave epitopes, very stable, cheap to express | Needs fusion or albumin binding for useful exposure |
| scFv-Fc, minibody | 80–110 kDa | Restores FcRn recycling and bivalency at lower mass | Non-natural architecture, developability work needed |

Smaller means faster tumour penetration and faster clearance at once; the two trade against each other, and the choice follows the intended dose interval and route.

## Bispecifics and multispecifics

A bispecific binds two different epitopes. The architecture decides geometry, valency and manufacturability.

- **Heterodimerisation of full IgG** — knob-into-hole, electrostatic steering, CrossMab for correct light-chain pairing. Keeps IgG-like PK; the engineering problem is pairing purity.
- **Appended IgG** — DVD-Ig, 2+1 and 1+1 formats with an extra scFv or Fab. Gains valency control; adds mass and liabilities.
- **Fragment-only** — tandem scFv (the BiTE architecture), DART, diabody. Small, potent, no Fc, so exposure is short and infusion is often continuous.
- **Mechanism classes** — T-cell engagers (one arm CD3, one arm a tumour antigen); checkpoint co-targeting; receptor cross-linking or clustering; protein bridging, where emicizumab's two arms substitute for factor VIII by holding factor IXa and factor X together; dual-pathway blockade.

Potency in T-cell engagers is driven by affinity balance, not by maximising both arms: a too-strong CD3 arm concentrates the drug in T cells and widens toxicity rather than efficacy.

## Antibody-drug conjugates

Four components, each a design decision.

1. **Antibody** — needs a target that internalises and whose expression is high on tumour and low on essential tissue.
2. **Linker** — cleavable (valine-citrulline dipeptide, GGFG tetrapeptide, hydrazone, disulfide) releases payload in the lysosome or tumour microenvironment and permits bystander killing of neighbouring antigen-negative cells; non-cleavable (SMCC thioether) requires full antibody catabolism and gives no bystander effect but better plasma stability.
3. **Payload** — auristatins (MMAE, MMAF; tubulin), maytansinoids (DM1, DM4; tubulin), camptothecins (DXd, SN-38; topoisomerase I), calicheamicin and PBD dimers (DNA). Potency sits in the sub-nanomolar range, so free payload in circulation drives much of the toxicity.
4. **Conjugation** — stochastic lysine or interchain cysteine chemistry gives a distribution; site-specific conjugation gives a homogeneous product. **DAR** (drug-to-antibody ratio) is the average payload count: too low loses potency, too high accelerates clearance and aggregation.

Class toxicities reported across ADC programmes include neutropenia, peripheral neuropathy (tubulin payloads), interstitial lung disease, ocular surface toxicity and thrombocytopenia; which ones apply is payload- and linker-specific, so check the label rather than generalising.

## Fc engineering

| Goal | Common approach |
|---|---|
| More ADCC | Afucosylation (glyco-engineered cell lines), or mutations such as S239D/I332E |
| Silenced effector function | LALA (L234A/L235A) and LALA-PG, N297A or N297G aglycosylation, IgG4 backbone |
| Longer half-life | FcRn-affinity mutations YTE (M252Y/S254T/T256E) or LS (M428L/N434S) |
| Shorter half-life / FcRn blockade | Engineered high-affinity Fc that saturates FcRn and accelerates clearance of endogenous IgG |
| Less immune-complex trouble | Hinge and CH2 changes that reduce Fc–Fc clustering |

Mutation positions follow EU numbering; the same residue carries different indices in other schemes, so quote the scheme (see antibody-sequence-bioinformatics).

## Adjacent modalities

Radioimmunoconjugates, immunocytokines, antibody-oligonucleotide conjugates, Fc-fusion proteins (named with the `-cept` stem, e.g. receptor traps), peptide-Fc fusions, and CAR constructs whose binder is an scFv lifted from a monoclonal. They share the discovery and CMC machinery but differ in regulatory classification.

## Decoding a drug name

A name encodes format (the stem) and, in older names, the source species (an infix). Both schemes are governed by the WHO INN Programme, and the definitions are the ones to quote rather than a remembered summary.

- **Source infix (legacy).** `-o-` mouse, `-xi-` chimeric, `-zu-` humanised, `-u-` fully human. WHO dropped the source infix at its 64th consultation in April 2017, so an infix that is present dates the molecule to before 2017; a name assigned since carries no source information at all.
- **Stem (from late 2021).** At its 73rd consultation in October 2021 the WHO INN Expert Group discontinued `-mab` for new antibodies — 879 INNs already carried the stem, which made new names hard to distinguish (Koch et al., *mAbs* 2022) — and split it into four stems encoding format ([WHO, 2021](https://www.who.int/publications/m/item/inn-21-531); revised [May 2022](https://www.who.int/publications/m/item/inn-22-542)):

| Stem | Meaning |
|---|---|
| `-tug` | Monospecific full-length immunoglobulin with unmodified constant regions (an "unmodified immunoglobulin"); covers natural, chimeric and humanized full-length antibodies of any class |
| `-bart` | Monospecific full-length immunoglobulin with any engineered change in the constant regions (an "artificial immunoglobulin") — a hinge mutation, a new glycan site, altered FcRn or FcγR binding |
| `-ment` | Monospecific immunoglobulin fragment of any kind not covered by `-tug` or `-bart`, including an scFv-Fc, provided at least one variable domain contributes to binding |
| `-mig` | Bispecific or multispecific immunoglobulin, any format — full-length, fragment, engineered or not |

- `-mig` takes precedence: a bispecific with an engineered Fc is a `-mig`, not a `-bart`. Cross-reactivity from a single set of CDRs (for example bimekizumab) stays on the monospecific stem.
- **Fusion proteins** fall outside the antibody stems and take the `-fusp` stem, with an infix recording the partner (`-a-` for an antibody part): tebentafusp (a TCR fused to an anti-CD3 scFv), valanafusp alfa, onfekafusp alfa. A construct made only of antibody domains stays on the antibody scheme, not `-fusp`.
- **Target/action infixes** are still used and no longer imply the format: `-ta-` tumour, `-pru-` immunosuppressive, `-sto-` immunostimulatory (includes checkpoint inhibitors), `-ler-` allergen, `-ki-` cytokine and cytokine receptor, `-ci-` cardiovascular, `-ne-` neural, `-vi-` viral, `-ba-` bacterial, `-toxa-` toxin.
- Existing `-mab` names were kept, so the stem alone does not date a molecule reliably — only names assigned from late 2021 follow the new rules.
- The INN is the generic name; the brand name is separate and market-specific. In the US a biological product carries a four-letter suffix after the INN to distinguish related products (for example `-dkst`, `-abda`).
- Decoding stops at format. Target, indication and ownership come from a lookup, not from the name.
