# Event facts

Retrieved 2026-11-13 from: the [participant guide](https://oslo-ai-antibodies-hackathon.vercel.app/participant_guide) (**guide**), the [event site](https://oslo-ai-antibodies-hackathon.vercel.app/) (**site**), and the [Anthropic × Adaptyv competition terms](https://proteinbase.com/competitions/anthropic-adaptyv-2026/terms) (**terms**) that the site points to. These pages change: run `python3 scripts/read_guide.py --diff` and trust the live pages over this file. The guide says its scoring weights are provisional and that model access and versions "will be confirmed before the event". It also says: *"This is a preparation guide, not the task: the task is released at 09:30 on the day."*

## Logistics

| | |
|---|---|
| Date | Saturday 14 November 2026 |
| Venue | BI Startup Village, BI Norwegian Business School, Nydalsveien 37, 0484 Oslo; doors 08:30, breakfast included |
| Team | up to 5; alone is fine and organisers help form teams (site) |
| Bring | laptop and charger; meals, refreshments and compute are provided; no accommodation (site) |
| Organisers | Nucleate Norway (main), with Girls Who ML, Yogutide and Tekna Biotek; Oslo Cancer Cluster supports logistics (site) |

Schedule, marked preliminary on the site:

| Time | |
|---|---|
| 09:00 | Registration, light breakfast, team adjustments |
| 09:30 | Opening: welcome, **task** and mentor intro |
| 10:00 | Focused work starts |
| 12:00 | Lunch |
| 17:00 | Pitch and presentation prep |
| 18:00 | **Pitch submission deadline**, snacks, tech set-up |
| 18:05 | Presentations begin |
| 19:00 | Presentations end; jury deliberates |
| 19:30 | Award ceremony, mingling |

## What is submitted and what is judged

- **Submit** a pitch or presentation and a **GitHub repository link** with the materials created during the hackathon; a working prototype strengthens it (site FAQ).
- **How projects are judged:** "A judge runs your skill on a case your team hasn't seen" (site FAQ). Two scientific and two product criteria:

| Criterion | Weight | Definition (guide) |
|---|---|---|
| Judgment | 40% | Clear reasoning behind the molecules you chose |
| Execution | 20% | A reproducible pipeline in a GitHub repo |
| User fit | 20% | What your design is for, and who needs it |
| Path to value | 20% | A credible route to real use, for the molecule or the method |

  The guide: "Judgment carries the most weight: we want to know why you made each choice, not only what you built. These weights are provisional and will be confirmed in the final hackathon instructions. Each group needs to provide score tables and report where each score came from."
- **Designs:** the funnel ends with **up to 10 designs** to present. Adaptyv, not the team, tests them; the guide says "We can probably test five designs per team", and says VHHs, Fabs and scFvs are tested, not whole antibodies. Record inputs, model versions and the reasons for selecting each candidate.

## Prizes

- **Site:** 3,000 USD prize money for the winning team(s); lab validation of winning sequences (expressed and tested in vitro by a partner lab, with a full report; valued at 20K USD); the possibility of a scientific publication; a pitch to venture capitalists; partner media.
- **Guide:** Apheris and OpenFold are the monetary prize sponsors, and **to qualify for that prize a pipeline must include Apheris' version of OpenFold**. AMASS awards 100 USD in credits to the team with the most creative use of AMASS.
- The two pages describe the prizes in different words; ask at the opening which applies.

## Rules that can cost a team

- **Pre-existing work** (site FAQ): "All project outputs and repositories must be created during the hackathon. Prior ideas, research or papers may inspire you, but if your project builds on a pre-existing startup or business idea, you must disclose it to the organizers." Treat prepared tooling, skills and scripts as something to disclose and to ask about, and create the submission repository on the day.
- **Ownership and publication** (site FAQ and terms §6): designs sent for validation are tested by Adaptyv and the results are published on Proteinbase under ODC-BY, with the sequence, predicted structure, design method, measurements and the participant's name and team name. By submitting, participants give Anthropic and Adaptyv permission to use and publish the design; they do not become its owners. The terms put the responsibility for patent filings before submission on the participant.
- **Biosecurity** (terms §5.5): every design sent for synthesis is screened and may be rejected without explanation.
- **Embedded instructions** (competition FAQ): text in a submission addressed to the selecting model can be grounds for disqualification.
- **Original work** (terms §3.3): the submission must be the participant's original work or one they hold rights to.

## Tools and sponsors

Provided: **JapanFold** (structure prediction and binder-design workbench), **Nebius** (model catalogue and NVIDIA GPUs), **Apheris Foundry** (access planned; includes models further optimised on pharma proprietary data), **AMASS** (literature search and verification), Anthropic **Claude Max credits**, JapanFold credits from Tenstorrent × ai&. "These tools have agent integrations", so agents can run them while people decide.

JapanFold's public workbench is a free demo on shared compute with caps: **1,024 residues per structure, 10 structures per run, 10 binders per design**. A VHH–antigen complex with a large antigen can exceed that: crop the antigen to the region around the epitope, or use the API (guide).

Models listed on JapanFold in the guide (availability to be confirmed on the day):

| Model | What it does | Heads-up from the guide |
|---|---|---|
| OpenFold3 | Open AlphaFold3-class complex prediction | Fully open; the organisers also provide it directly |
| RoseTTAFold3 | AlphaFold3-class complex prediction | |
| Boltz-2 | Structure plus binding affinity | The affinity head is trained on protein–small-molecule data, not VHH–antigen affinity |
| OpenDDE | Protein and antibody–antigen complexes | Has an antibody–antigen-tuned checkpoint; gains are self-reported, so test whether they include nanobodies |
| Protenix-v2 | All-atom complex prediction | An independent co-folder, useful for consensus |
| OpenBind-0 | Protein–ligand, co-folded | Small-molecule oriented |
| ESMFold-2 | Fast single-sequence folding | Quick first look, no MSA |
| AF2-IG | Re-scores a binder you already designed | AlphaFold2 initial-guess |
| BoltzGen, RFdiffusion3, PXDesign | De novo binder and backbone design | Generate candidates; you still have to filter them |
| ESMC, SaProt | Sequence and structure-aware embeddings | Features for your own models |

AMASS pages from the guide: `https://amass.tech/oslo-ai-antibodies-hackathon` (example use cases and antibody data to start from), `https://amass.tech/onboarding/oslo-ai-antibodies-hackathon` (set-up walkthrough), `https://amass.tech/how-to-do-scientific-work-in-claude`, `https://amass.tech/how-to-use-amass`.

## The practice tutorial (guide), with checks

Practice with PDB **1ZVY**: a dromedary VHH (chain A) bound to hen egg-white lysozyme (chain B). Download the mmCIF, inspect chains and residue identifiers, open JapanFold, choose Drug Design, then RFD4-Proteina, paste the structure, and choose a contig:

- **Option A, new binder to chain B:** `B1-129, /0, 110-130`. `B1-129` is the target, `/0` separates chains, `110-130` asks for a new segment of 110 to 130 residues. The result is not necessarily a VHH.
- **Option B, redesign a VHH loop:** `B1-129, /0, A2-96, 20, A117-125`. It keeps the target, keeps VHH segments A2–96 and A117–125, and asks for a new 20-residue segment between them.

Checked against the real file on 2026-11-13: chain B is residues 1–129 (lysozyme); chain A has coordinates for residues 1–125 and residues 126–136 are missing; the IMGT CDR3 of chain A is `GATRKYVPVRFALDQSSYDY`, residues A97–A116 (20 residues), between Cys96 and Trp117; **residue A1 has only C-alpha, C and O atoms, no backbone N**, which is why the example starts at A2; FR4 is resolved only to A125, which is why the example stops there. `python3 antibody-sequence-bioinformatics/scripts/cdr_contig.py 1ZVY.cif --chain A --target-chain B` (from the repository root) prints exactly `B1-129, /0, A2-96, 20, A117-125`. The guide adds that a backbone-only generator may need a later sequence-design step, so inspect outputs before assuming they are complete VHH sequences, and that IMGT positions are not interchangeable with PDB residue numbers.

## What the guide covers

Start here and basics (proteins, UniProt and PDB, what an antibody and a VHH are, epitope and affinity, vocabulary); how computational design works (the generate, score, filter funnel; the fourth step, lab testing, is Adaptyv's); where machine learning helps (a map from problems to model families); what developability is and what to check; the tools; the tutorial; AMASS; a "Rosetta stone" of plain-word primers for five fields (machine learning, biology, physics and chemistry, medicine, business); five optional topic pages; what AI can and cannot do today (folding one nanobody is largely solved apart from CDR3; predicting complexes is improving but poor on novel epitopes; predicting developability is partial; ranking mutations by affinity is weak); scoring; further reading; a glossary; and a Toolbox with a KD ⇄ ΔG calculator, a histidine-switch demo and a liability-motif scanner. Further reading named by the guide: the Adaptyv EGFR competition lessons preprint and the Asimov Press guide *How to Design Antibodies*.
