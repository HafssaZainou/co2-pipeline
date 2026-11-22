# AGENTS.md

## Project

Which EU country has reduced its CO₂ emissions per person the most since 2000? We answer it in two readings: in tonnes per person and in percent.

## Setup and commands

- Activate the environment first, in every new terminal: `source .venv/Scripts/activate` (Windows, Git Bash) or `source .venv/bin/activate` (macOS/Linux)
- Install packages: `python -m pip install -r requirements.txt`
- Download the data: `python src/download.py`
- Clean the data: `python src/clean_co2.py` (writes `data/processed/co2_eu.csv`)
- Analyse: `python src/analyse.py` (prints the result, saves a chart in `figures/`)
- Run the tests from the top of the repository: `python -m pytest`

## Data

- Source: Our World in Data, CO2 and Greenhouse Gas Emissions, https://github.com/owid/co2-data
- Pinned version: commit `382ee6c662b0ece26e111f263b44c029afad7787` (2 June 2026). Always download this version, never `master`.
- Licence: CC BY 4.0 (Our World in Data); third-party sources follow their own terms, see the codebook.
- Codebook: `data/raw/owid-co2-codebook.csv`, one row per column, with unit and source
- The data file has 50,411 rows and 79 columns, separated by commas, without quoted fields.
- Units: `population` in people, `co2` in million tonnes, `co2_per_capita` in tonnes per person. So approximately `co2 * 1,000,000 / population` gives `co2_per_capita`.
- Not countries: 36 of the 254 values in `country` have no `iso_code`. They are aggregates such as `World`, `Asia`, `European Union (27)`, income groups, `(GCP)` variants, and `International shipping` and `International aviation`.
- Exception: `Kosovo` has no `iso_code`, but Our World in Data treats it as a country.
- Use exact names from the file: e.g. `Czechia`, not `Czech Republic`; `Middle East (GCP)`, not `Middle East`.
- Years: `co2`, `co2_per_capita` and `population` until 2024, `gdp` until 2022.

## Rules

- `data/raw/` is read-only. Never change, move or delete files there, and never change its permissions. If an edit there is blocked, do not work around it. Tell us instead.
- No new packages without asking.
- Never change or delete tests to make them pass. If a test fails, explain why.
- Print row counts after every filter.
- No silent filling of missing values: report them and ask.
- Never invent URLs, column names or numbers; ask instead.
- Show a plan before you write code. One step per session.
- Never read `data/raw/owid-co2-data.csv` in full (about 7.9 million tokens). Use `head`, `cut` or pandas with `usecols`.