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

### Code for the evidence of error 5:

```python
import eu_report as r

eu = r.eu_members(r.load())
period = eu[eu["year"] > 1990].sort_values("year")
print(period["year"].min())
print(period.groupby("country")["year"].min().value_counts())
lux = eu[(eu["country"] == "Luxembourg") & (eu["year"].isin([1990, 1991]))]
print(lux[["year", "co2_per_capita"]])
```