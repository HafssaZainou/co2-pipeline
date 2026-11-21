# Explore

Driver: Aqsa Shaikh. Tool: GitHub Copilot in VS Code, model: Copilot Fusion, agent mode `Interactive` with `Manual permissions`. Navigator: Hafssa Zainou.

## Prompts 1 and 2

**Prompt 1 (What is in this repository?):** Before asking for permission, the agent ran one command (`git status`) and read four files, including `.gitignore`, without asking. It then asked for permission once, for a longer command that measured file sizes (`du -h`), counted rows and columns with a short Python script, and listed all files with `find`. We read the command before approving it: it only reads files and changes nothing, so we chose *Allow Once*. Conclusion: in *Manual permissions* mode, Copilot reads files and runs simple read-only commands on its own, but asks before longer scripts.

**Prompt 2 (columns and units):** The agent searched the codebook for the six columns and ran two read-only commands (`cut … | sed | paste` and a short Python script) to list the 79 column names. It did not open the large data file, as the prompt asked. Units according to the agent: `population` in people, `co2` in million tonnes, `co2_per_capita` in tonnes per person.

## The loop

For the third prompt (*Which values in the column country are not countries?*), the agent asked once for permission to run a short Python script. It read only the columns `country` and `iso_code` of `data/raw/owid-co2-data.csv` with pandas, listed every `country` value without an ISO code, and counted them. We read the script before we approved it: it only reads. The agent then sorted the output into groups (continents, income groups, international categories, historical estimates) and concluded that an empty `iso_code` marks a non-country. This matches the loop of the slide *Anatomy of one task*: gather context (read the codebook and two columns), act (run the script), observe (the printed list), answer.

## Three claims

1. **254 entities, 36 without ISO code.** Confirmed:

   ```bash
   tail -n +2 data/raw/owid-co2-data.csv | cut -d, -f1 | sort -u | wc -l
   # 254
   grep -E "^[^,]*,[0-9]+,," data/raw/owid-co2-data.csv | cut -d, -f1 | sort -u
   # 36 names
   ```

   But the agent’s list is not exact. It leaves out `Africa (GCP)`, `Asia (GCP)`, `Europe (GCP)`, `North America (GCP)`, `Oceania (GCP)` and `South America (GCP)`, and it writes `Central America` and `Middle East`, which do not exist in the file: there, they are called `Central America (GCP)` and `Middle East (GCP)`. A filter built from its list would miss them without an error.
2. **Units.** Confirmed in the codebook: `population` in people, `co2` in million tonnes (Mt), `co2_per_capita` in tonnes per person.

   ```bash
   grep -E "^(co2|co2_per_capita|population)," data/raw/owid-co2-codebook.csv
   ```

3. **Rows.** The agent reported 50,411 rows. `wc -l` gives 50,412 lines: 50,411 rows plus the header. Confirmed.

**Kosovo and International shipping.** The agent mentioned both. Kosovo has no ISO code in this file, but it is a country. *International shipping* and *International aviation* have no ISO code either, because their emissions belong to no country. If we kept only rows with an ISO code, we would drop the aggregates and shipping, which is what we want, but we would also lose Kosovo without noticing.

## The context

Copilot in VS Code showed us no display of how full the context window was; the quota meter showed *Credits 0% used* after the three prompts. The second prompt says do not read the whole data file, because the file has 14 MB, which is about 7.9 million tokens (lecture slides Agentic Coding, slide 12, tokenizer o200k_base; other models count differently). Header and first five rows are only 694 tokens. The context window of the model in my VS Code (KI:connect Mistral Small 4) is 144K tokens. For Copilot Fusion we saw no value. According to the lecture, numbers also split badly into tokens (2024 becomes 202 + 4); this is consistent with the errors in the agent’s list, but we did not test it. The agent read only the small codebook and two columns.  

After all three prompts, `git status` showed no changes: the agent changed nothing.

## AGENTS.md

We wrote `AGENTS.md` ourselves (about 36 lines: Project, Setup and commands, Data, Rules) and then asked Copilot Fusion for its own draft, `AGENTS.draft.md`, without showing it our file.

**What the agent's draft had that ours did not.** The codebook as the authority for column meanings and units; the rule to check factual claims independently; assertions instead of printed-only checks; the smallest complete change; recording the source and version of derived data; updating `requirements.txt` when a package is added.

**What our file had that the draft did not.** The pinned commit, the licence and the project question; the concrete facts we found in Explore (254 entities, 36 without `iso_code`, the `(GCP)` variants, exact names such as `Czechia`, the last year of each column); the pipeline commands; and stricter rules: `data/raw/` is read-only and must not be worked around, tests must not be changed to make them pass, and the agent shows a plan before it writes code. The draft only says not to alter raw data *silently*, which leaves open whether it may do so openly.

**What the agent got wrong or assumed.**
- It assumed macOS or Linux (`python3 -m venv`, `.venv/bin/python`). We work on Windows, where the path is `.venv/Scripts/activate`.
- It wrote that the repository has no source code and no entry point. This is true today, but it will be wrong as soon as `src/` exists.
- It says not to commit generated analysis results. Our pipeline writes `data/processed/co2_eu.csv` and `figures/`; we still have to decide whether to commit them.
- It spends about 20 lines on the repository layout, which the agent can see with `ls`. The draft has more than 60 lines, we asked for about 40.

**A caveat about the draft.** It describes `workflow.md` and mentions Kosovo. The agent did read our own notes in the repository, so its Kosovo remark is not independent knowledge.

**What was missing in our file.** A rule that the agent must not read the whole data file. The lecture gives about 7.9 million tokens for it, and this was the point of Explore. Draft: *Never read `data/raw/owid-co2-data.csv` in full. Use `head`, `cut` or pandas with `usecols`.* We added this line to `AGENTS.md`.