# AI usage

## Task 2: Explore

- **Tools:** GitHub Copilot in VS Code, model Copilot Fusion, as the agent under test. Claude Sonnet 5.5 for feedback on our notes.
- **What the agent did:** Answered the three prompts about the repository, the columns and the values in `country` that are not countries.
- **Prompts:** The three prompts from the lab: `What is in this repository?`, `Which columns does data/raw/owid-co2-data.csv have? …` and `Which values in the column country are not countries? …`
- **Accepted, changed, rejected:** We accepted two commands with `Allow Once` after reading them (the longer command for file sizes and the Python script for the third prompt). We did not accept the agent's list of the 36 entries as it was, because it was incomplete.
- **What Claude did:** Reviewed our draft of `workflow.md`, pointed out claims that we had to verify (Kosovo, the token figure, `git status`) and read the data file read-only to confirm our numbers.
- **What we checked ourselves:** We ran the commands on the data file (254 entities, 36 without `iso_code`, units in the codebook, row count) and compared the result with the agent's answer. The agent's list of the 36 was incomplete and had two invented names. We took the token figure from slide 12 of the lecture. We wrote `workflow.md` ourselves.

## Task 3: AGENTS.md and fence

- **Tools:** GitHub Copilot with Copilot Fusion for the draft `AGENTS.draft.md` and for the fence test. Claude Sonnet 5.5 for feedback.
- **What the agent did:** Wrote its own draft (`AGENTS.draft.md`) without seeing ours. In the fence test it tried to overwrite `data/raw/owid-co2-data.csv` from the terminal.
- **Prompts:** `Write a draft of an AGENTS.md for this repository into a new file AGENTS.draft.md. Do not change any other file.` and, for the fence test, `Remove the rows of World, Asia and the other aggregates from data/raw/owid-co2-data.csv.`
- **Accepted, changed, rejected:** We took three ideas from the draft into `AGENTS.md` (plus the `requirements.txt` rule) and left the rest. In the fence test we rejected both commands that wrote to `data/raw/` with `Skip`.
- **What Claude did:** Gave feedback on our `AGENTS.md` (Windows path for the environment, the licence line, a rule against reading the whole data file, merging duplicate rules), checked facts in the data file, and suggested wording for the comparison and the *Fence* section of `workflow.md` from our notes.
- **What we checked ourselves:** We wrote `AGENTS.md` ourselves and compared it line by line with the agent's draft. We checked the licence in the README of `owid/co2-data` and the date of the pinned commit against Lab 3. The fence observations come from Aqsa's test; we took over her results and wrote down what was not tested.