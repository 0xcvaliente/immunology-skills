# Working with this repository

Claude Code skills for antibody work, and a perishable brief for the AI × Antibodies hackathon (Oslo, 14 November 2026). `README.md` lists the skills and scripts; each skill's `description` is the router.

## Using it for the hackathon

Read [`oslo-antibodies-hackathon/references/agent-runbook.md`](oslo-antibodies-hackathon/references/agent-runbook.md) first: who decides what, which repository gets what, when to stop and ask, and starter prompts. The design method is `antibody-binder-design`. Event facts live in `oslo-antibodies-hackathon/references/event-facts.md` and are re-checked with `read_guide.py --diff`. This repository is prepared tooling: keep the team's work out of it.

## Changing it

1. **Edit here, install from here.** The repository is the source of truth. `./install.sh` copies the skills into `~/.claude/skills` (`--link` symlinks them). Never edit the installed copies: the next install replaces them, and the old copy goes to `~/.claude/skills-backups/`.
2. **Run the tests before committing:** `python3 -m unittest discover -s tests`. Two tests skip without ANARCII; after touching the ANARCII path, run them with an interpreter that has it (`pip install anarcii` pulls in PyTorch). A behaviour change in a script gets a test. A change to the placement rules in `vhh_qc.py` is re-measured against ANARCII and the numbers in `vhh.md` are updated.
3. **Frontmatter:** `name` equals the directory; `description` is one line under 1,300 characters (it is loaded on every turn) with no `": "` and no `" #"`, which break strict YAML parsers. The tests enforce all three.
4. **Facts carry dates.** Approvals, event details and model availability are looked up and dated, never recalled. Event facts come through `read_guide.py`; after reviewing a diff, `--write-snapshot` records the new state. Put quotation marks only around text that appears verbatim in the source.
5. **Scripts:** standard library only, Python 3.9 or newer.
6. **Public repository:** no personal data, accounts, tokens or absolute home paths.
7. **Git flow:** branch, open a pull request, and merge only when the owner says so: "merge PR #N", or "PR and push main", which means open the PR and merge it. Delete the branch only when asked. End commits with the attribution line your harness specifies. If git reports `index.lock`, another process is touching the repository for a moment: check that no git process is live, wait, and retry; do not delete the lock while one is running.
8. After a merge, run `./install.sh` so the installed skills match `main`.
