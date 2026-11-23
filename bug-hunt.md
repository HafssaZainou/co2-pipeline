# Bug hunt

Reviewed by Hafssa Zainou and Aqsa Shaikh, without AI (45 minutes). The agent was only allowed to explain what a line does.

## What we found

| # | Function | Row of the checklist | What goes wrong | Evidence (command and number) |
|---|---|---|---|---|
| 1 | `eu_members` (line 24) | Joins and merges (rows lost) | The list MEMBERS says Czech Republic, the data says Czechia. The merge drops the country without an error, so the report says 27 member states but uses only 26. | `eu["country"].nunique()` → 26; `set(r.MEMBERS["country"]) - set(eu["country"])` → `{'Czech Republic'}`; `df[df["country"].str.contains("Czech")]["country"].unique()` → `['Czechia']`. EU total 1990: script 3,706.001 Mt vs. OWID European Union (27) 3,870.253 Mt; the difference, 164.252 Mt, is exactly the CO2 of Czechia in 1990. Imports 1990: script 502.7 Mt vs. OWID 489.9 Mt; the difference, −12.8 Mt, is exactly the imports of Czechia. |
| 2 | `eu_members` (line 45) | Missing values | `dropna(subset=["consumption_co2"])` removes every row without consumption-based data, although only the imports section needs that column. So 2024 is missing from all sections, and the report ends in 2023. | `eu["year"].max()` → 2023; `df[df["country"] == "Germany"]["year"].max()` → 2024; Germany 2024: co2 = 572.319, `consumption_co2` = NaN |
| 3 | `per_person` (line 55) | Aggregation (unweighted mean of ratios) | The function takes the plain mean of the countries' `co2_per_capita`, so Malta counts as much as Germany. The EU value must be total CO2 divided by total population. | Script 1990: 9.87 t, 2023: 5.35 t; OWID European Union (27): 9.215 t and 5.514 t. Total CO2 / total population of the 26 countries in 1990: 9.05 t; with Czechia: 9.215 t, exactly OWID's value. |
| 4 | `chart` (line 81) | Units and scales | The y-axis label says `(t)`, but `co2` is in million tonnes (Mt), so the unit on the chart is wrong. | `grep -E "^co2," data/raw/owid-co2-codebook.csv` → `million tonnes (Mt)`; `python -c "import eu_report as r; t = r.eu_totals(r.eu_members(r.load())); print(t.loc[[1990, 2023], 'co2'])"` → 1990: 3706.001, 2023: 2401.764 |
| 5 | `biggest_cuts` (line 66) | Filters | The report says "since 1990", but the filter `eu["year"] > since` removes the rows of 1990, so the cut is measured from 1991. | `period["year"].min()` → 1991; Luxembourg `co2_per_capita` 1990: 30.938, 1991: 32.109 (see the code below the table) | 
| 6 | `chart` (line 79) | Units and scales (nearest row; the checklist has no row for chart axes) | `ax.set_ylim(2000, None)` starts the y-axis at 2000 instead of 0, so the bars show only the part above 2000. The 2023 bar looks much smaller compared with the 1990 bar than it is. | `python -c "print(2402/3706, (2402-2000)/(3706-2000))"` → 0.648, 0.236: the 2023 bar is 65 % of the 1990 bar in reality, but 24 % of it in the chart |

*Checked, no error of their own: eu_totals and the imports line in main. Their differences from OWID come only from error 1.*

### Code for the evidence of error 5 (as it was at the time of the review):

```python
import eu_report as r

eu = r.eu_members(r.load())
period = eu[eu["year"] > 1990].sort_values("year")
print(period["year"].min())
print(period.groupby("country")["year"].min().value_counts())
lux = eu[(eu["country"] == "Luxembourg") & (eu["year"].isin([1990, 1991]))]
print(lux[["year", "co2_per_capita"]])
```

## Agent review

Mistral Small 4 (KI:connect), new session, Manual permissions. Prompt: the one from the lab.
Files read: Codebook (lines 1–50); data file only through 9 terminal commands (first lines, search for European Union (27)); eu_report.py in the protocol not able to read (a Read in src\eu_report.py failed).  |  Did it read bug-hunt.md? No  |  Numbers in its answer: None

| # | Our error | Found by the agent? | Agent's evidence | Our comment |
|---|-----------|---------------------|------------------|-------------|
| 1 | eu_members, Czechia | Yes | The script uses Czech Republic in the MEMBERS DataFrame, but the data file uses Czechia: `("Czech Republic", 2004),  # Line 28 in eu_report.py` According to the codebook, the correct name in the dataset is Czechia. This will cause the eu_members() function to fail to merge properly, resulting in missing data for Czechia in the EU calculations. | The line that the agent gave, „Line 28“, is not correct (in the file it says line 24). It does not name any commands and no number, for example not „26 instead of 27“. Its sentence „According to the codebook …“ is not proven. We checked it: `grep -c "Czechia" data/raw/owid-co2-codebook.csv` → 0, so the codebook does not say this.|
| 2 | eu_members, dropna | Partly | The eu_members() function drops rows with missing consumption_co2 values: `return eu.dropna(subset=["consumption_co2"])` This could silently exclude valid EU member states if their consumption data is missing for certain years, leading to incorrect totals. | The agent names the correct line and says „could silently exclude valid EU member states“. We had the actual result: The year 2024 is missing, the report ends in 2023. |
| 3 | per_person, mean | No | Nothing found. | / |
| 4 | chart, label (t) | Yes | The chart function uses: `ax.set_ylabel("CO2 emissions (t)")` This is misleading since the data is in million tonnes (Mt), not tonnes. The y-axis should show "Mt" not "t". | It names the issue correctly as Unit and scales (Mt instead of t), but with no evidence. |
| 5 | biggest_cuts, > | No | Nothing found. | / |
| 6 | chart, set_ylim | No | Nothing found. | / |

*3 of 6 of our bugs were found by the agent.*

Reported by the agent, but not one of our six:

| Agent's point | What we checked | Result |
|---------------|-----------------|--------|
| Kosovo missing | `grep -ci "kosovo" data/raw/owid-co2-codebook.csv` → 0; `grep -n "Exception" data/raw/owid-co2-codebook.csv` → no line; `data/raw/owid-co2-data.csv` → 174 lines | Its quote is not in the codebook (0 hits). Kosovo is in the data (174 lines), but it is not one of the 27 member states of the EU, so it does not belong in `MEMBERS`. Not an error. |
| European Union (27) row double-counted | `sorted(eu['country'].unique())` → 26 names | The list of countries in eu has 26 names, all of them single countries. There is no European Union (27) row in it, so nothing is counted twice. Not an error. |
| Year range not validated | `eu.groupby('country')['year'].agg(['min','max'])` → all 1990 to 2023; `python -c "import eu_report as r; eu = r.eu_members(r.load()); print(eu.groupby('country')['year'].count().unique())"` → [34] | All 26 countries start in 1990 and end in 2023. In this data the assumption holds. All 26 countries have 34 rows (1990 to 2023, no gaps). Not an error. |

*Of the agent's 6 points, only 3 match our bugs (Czechia, dropna, y-label). The other 3 are not errors in this data. The agent did not find 3 of our bugs (per_person, >, set_ylim), and it gave no numbers as evidence.*

## What we learned

The line "CO2 per person" changed the most: the unweighted mean (error 3) and the missing Czechia (error 1) made 1990 look like 9.9 t instead of 9.2 t, and the change since 1990 −45.7 % instead of −41.5 % (the first report ends in 2023, the second in 2024, because of error 2). The most convincing wrong number would have been the chart with the y-axis starting at 2000 (error 6): the 2023 bar looked only 24 % as high as the 1990 bar, although it was 65 %, and nobody doubts a picture. The agent was faster: it found the name Czechia, the dropped rows and the unit on the axis in one pass, without a hint. We were better at evidence and at the quiet errors: we gave a number for every error, found the three that the agent missed (unweighted mean, `>` instead of `>=`, y-axis from 2000), and checked its claims, which showed a wrong line number, a quote that is not in the codebook and three points that were no errors.