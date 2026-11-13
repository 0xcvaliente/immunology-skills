# Before the day

The guide asks for "a couple of evenings". Everything below is something that costs minutes now and an hour at 10:30 on the day. Tick it off, and write down what failed.

## 1. Rules and the repository

- [ ] Read the site FAQ on pre-existing work. Decide what is prepared knowledge and tooling (these skills, scripts, notes) and what must be created on the day (the submission repository and everything in it).
- [ ] At registration or the opening, tell an organiser which prepared tooling you plan to use, and ask whether that is allowed. Note the answer and who gave it.
- [ ] Do not create the submission repository tonight. Have a GitHub account ready and know the three commands to start a repository.
- [ ] Note the prize condition: the Apheris version of OpenFold must be in the pipeline to qualify for the monetary prize.

## 2. Accounts and access

- [ ] JapanFold login (`https://japanfold.aiand.com/`) and a test structure prediction.
- [ ] Nebius access, the model catalogue (`https://forge.nebius.cloud/models/`), and how GPU time is granted.
- [ ] Apheris Foundry access: what is promised ("access is planned") and what is live.
- [ ] AMASS onboarding (`https://amass.tech/onboarding/oslo-ai-antibodies-hackathon`) and one literature search.
- [ ] Claude Max credits redeemed, and Claude Code working on the laptop.
- [ ] Agent integrations for JapanFold, Nebius and Apheris: find what each vendor actually offers, and read it before installing anything. Adaptyv's open `protein-design-skills` pack (MIT) covers tool execution on Modal; read what it installs before adding it.

## 3. Laptop

- [ ] Python 3.9 or newer; `uv` or a virtual environment.
- [ ] `biotite` (the guide's recommendation for structure files) and `anarcii` (numbering; installs PyTorch, so do it on a good connection).
- [ ] A structure viewer: PyMOL, ChimeraX or py3Dmol.
- [ ] In this repository: `python3 -m unittest discover -s tests` passes (no network, a few seconds).
- [ ] Charger, a second charger or a power bank, headphones.

## 4. The practice run (PDB 1ZVY)

Do the guide's tutorial end to end and compare with the numbers in `event-facts.md`.

- [ ] Download `1ZVY.cif`. From the repository root run `python3 antibody-sequence-bioinformatics/scripts/cdr_contig.py 1ZVY.cif --chain A --target-chain B`. Expect `B1-129, /0, A2-96, 20, A117-125` and "excluded (backbone N/CA/C incomplete): A1".
- [ ] Run `antibody-sequence-bioinformatics/scripts/vhh_qc.py` on the chain A sequence; expect CDR3 `GATRKYVPVRFALDQSSYDY`, hallmarks `FARG`.
- [ ] In JapanFold, run Option A and Option B with RFD4-Proteina. Note run time, output format (is a sequence returned, or a backbone only?), and which caps you hit.
- [ ] Take one output through folding, `interface_contacts.py` (binder, target, a few lysozyme hotspots) and `rank_designs.py` with ten rows. The point is to meet every file format once.

## 5. A dry run on a target you have not designed for

A judge runs the skill on an unseen case, so rehearse that.

- [ ] Pick a closed challenge page from the competition (`https://proteinbase.com/competitions/anthropic-adaptyv-2026`), copy its target sequence and requirements into a `task.md`, and walk antibody-binder-design steps 0 to 9 with a small budget (20 designs).
- [ ] Write down every step where you had to make something up. Those are the gaps to fix before the day, or the questions to ask a mentor.

## 6. Reading, by role (all optional, none is homework)

- Everyone: the guide's front page (basics, workflow, where AI stands, judging).
- Machine learning: the ML topic page; `antibody-binder-design/references/models-and-metrics.md`.
- Biology: the biology topic page and `antibody-sequence-bioinformatics/references/vhh.md`.
- Physics and chemistry: the physics page (KD and ΔG, why affinity is hard, the methods table).
- Medicine and business: the two topic pages and `antibody-therapeutics-landscape/references/value-and-pitch.md`.
- Two longer reads: the Adaptyv EGFR competition lessons preprint and *How to Design Antibodies* (Asimov Press).

## 7. Team

- [ ] Agree who plays which role (see `day-plan.md`), who owns the repository, and who owns the decision log.
- [ ] Agree how you share files and how often you merge. Write it down in one line.
