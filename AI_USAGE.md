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

## Task 4: Plan, then build in small steps

- **Tools:** Step 1 (`download.py`): GitHub Copilot with Copilot Fusion (Aqsa). Step 2 (`clean_co2.py`): KI:connect Mistral Small 4 in VS Code (Hafssa). Step 3 (`analyse.py`): Copilot Fusion, Aqsa. Claude Sonnet 5.5 for feedback and for drafts of two prompts.
- **What the agent did:** Wrote `src/download.py` (downloads only missing files, never overwrites, prints size and SHA-256), and `src/clean_co2.py` (27 EU member states, 2000 to 2024, writes `data/processed/co2_eu.csv`). `src/analyse.py` prints the three countries with the biggest cut in tonnes per person and in percent (2000 to 2024) and saves a chart of all 27 countries.
- **Prompts:** Step 1: the prompt from the lab, word for word. Step 2: our own prompt in the five parts (goal, context, constraints, done when, first). Claude drafted it; we read it and adapted it. Step 3: our own prompt in the five parts; Claude drafted it, we changed *six lines* to *two lists of three countries* and added *Do not install packages*.
- **Accepted, changed, rejected:** Step 1: we changed the plan (`SOURCES.txt` only after a real download, never change permissions, use only `AGENTS.md`, name the exact URLs) and accepted every command after reading it. Step 2: we added three things to the plan (names in the script, check for 27 countries, do not touch the tests). We rejected the agent's command to run the script in its own terminal, because `python` there is not our environment, and stopped the agent when it kept asking. Step 3: we changed the plan: countries with rising emissions have a negative cut and must be shown below zero. The draft prompt from Claude said to start the y-axis at zero, which would have hidden them. We accepted every command after reading it.
- **What Claude did:** Reviewed our tests (the test function name must start with `test_`), drafted the prompts for `clean_co2.py` and `analyse.py`, and gave feedback on the agents' plans.
- **What we checked ourselves:** Hafssa wrote `tests/test_clean.py` before the cleaning script and committed it (4 errors, 1 passed). After `clean_co2.py` we ran the script and the tests ourselves (675 rows, 5 passed) and checked with `git status` and `git diff --stat` that the tests were unchanged. `python src/download.py` printed the expected checksum `7f78e2b2…d5f6`. Step 3: the result has 54 rows after the filter (27 countries, 2 years). Claude recomputed the top three in both readings from the raw file and the numbers agree; we do our own hand check in Task 5.