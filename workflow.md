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
