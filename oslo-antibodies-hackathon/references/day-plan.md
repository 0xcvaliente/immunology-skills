# The day

Times are from the site's preliminary schedule: task at 09:30, work from 10:00, pitch prep from 17:00, **submission deadline 18:00**. The plan is built around one idea: get a crude end-to-end result early, then improve it, because a pipeline that ran once is worth more than one that is nearly ready. Adjust to the task you are given.

## Timeline

| When | Do | Done when |
|---|---|---|
| 09:30–10:15 | Take in the task. Write `task.md` (antibody-binder-design step 0). Turn each objective into a lever and a proxy. Split roles. Ask the organisers the open questions (what counts as binding, novelty rule, number of designs, prize conditions, whether prepared tooling is allowed). Create the repository. | Every field of `task.md` is filled or marked not stated; questions asked |
| 10:15–11:15 | In parallel: target dossier (one person); toolbox survey and smoke tests (one person); controls (positives and negatives) assembled (one person) | `tools.md`, the dossier and a controls file exist |
| 11:15–12:30 | **Tracer bullet**: about 20 designs, folded, scored, filtered, ranked, `selection.csv` written, `check_submission.py` run. Crude is fine. | An end-to-end result exists in the repository |
| 12:00 | Lunch, in shifts so the run does not stop | |
| 12:30–15:00 | Scale generation by two routes; calibrate on controls; add filters and the diversity rule; keep the decision log current | Hundreds of designs scored; AUC table saved |
| 15:00 | **Freeze generation.** No new designs after this point, only analysis. | |
| 15:00–16:00 | Select: `rank_designs.py`, then read the top designs by eye, in structure. The biologist signs off each design or names the risk. | `selection.csv` final; every pick has a reason and a risk |
| 16:00–17:00 | Held-out run on a second target with the pipeline unchanged; README, `methods.md`, one-command reproduction; `check_submission.py` passes | A clean clone reproduces the result, or the gap is stated |
| 17:00–17:45 | Pitch (see `pitch.md`). Rehearse once with a timer. | Slides done; one person has the repository link ready |
| 17:45 | **Submit**, fifteen minutes before the deadline | Link and files confirmed received |
| 18:00 | Deadline; tech set-up for presentations at 18:05 | |

## Roles

The guide describes five fields and notes that teams are mixed on purpose. With five people, one each; with fewer, merge. Everyone owns something, and one person plays **skeptic**.

| Role | Owns | Asks |
|---|---|---|
| Pipeline (machine learning, code) | generation, folding, scoring, `designs.csv`, the one-command run | Does it run unattended? Are seeds and versions recorded? |
| Biology | target dossier, epitope choice, fold integrity of every pick | Is the patch reachable? Would the fold survive? Would a cell make it? |
| Physics and chemistry | physical sense of predicted complexes, noise versus signal, which score to trust | Does it pack, are there clashes, is this difference bigger than the noise? |
| Medicine | user, patient, what standard of care already gives, safety margin | Who needs this, and what would have to be true for it to be worth making? |
| Business and integration | decision log, repository, README, pitch, submission | What is the next experiment, who pays, what is defensible? |

A person who does not code still has real jobs: reading every design, asking what a number is measured in, writing the log, and turning output into something a judge can follow in five minutes (guide).

## Habits that pay off

- Write the decision log as you go, one line at a time; reconstructing it at 17:00 does not work.
- Commit small and often, with the model version and seed in the message when a run produced the change.
- When two teammates disagree about a design, put both views and the evidence in the log; that is judgment, and it is what is being scored.
- When a tool misbehaves, record the exact command and output before changing anything. A mentor can only help with a failure that can be reproduced.
- Eat, and rotate so someone is always watching the long runs.
