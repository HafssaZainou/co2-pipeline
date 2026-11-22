import math
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "data" / "processed" / "co2_eu.csv"
FIGURES_DIR = ROOT_DIR / "figures"
CHART_PATH = FIGURES_DIR / "co2_per_capita_reduction_2000_2024.png"
REQUIRED_COLUMNS = {"country", "year", "co2_per_capita"}
START_YEAR = 2000
END_YEAR = 2024
EXPECTED_COUNTRY_COUNT = 27
DATASET_SOURCE = (
    "Our World in Data, CO2 and Greenhouse Gas Emissions; "
    "pinned commit 382ee6c662b0ece26e111f263b44c029afad7787"
)


def load_comparison() -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH)
    missing_columns = REQUIRED_COLUMNS - set(data.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    print(f"Input rows: {len(data)}")
    endpoints = data.loc[
        data["year"].isin([START_YEAR, END_YEAR]),
        ["country", "year", "co2_per_capita"],
    ].copy()
    print(f"Rows after selecting {START_YEAR} and {END_YEAR}: {len(endpoints)}")

    if endpoints["country"].isna().any():
        raise ValueError("Endpoint data contains rows with a missing country.")
    if endpoints["co2_per_capita"].isna().any():
        missing = endpoints.loc[
            endpoints["co2_per_capita"].isna(), ["country", "year"]
        ]
        raise ValueError(f"Missing endpoint emissions values:\n{missing.to_string(index=False)}")

    endpoints["co2_per_capita"] = pd.to_numeric(
        endpoints["co2_per_capita"], errors="raise"
    )
    if not endpoints["co2_per_capita"].map(math.isfinite).all():
        raise ValueError("Endpoint emissions values must be finite numbers.")
    if endpoints.duplicated(["country", "year"]).any():
        duplicates = endpoints.loc[
            endpoints.duplicated(["country", "year"], keep=False),
            ["country", "year"],
        ]
        raise ValueError(f"Duplicate country/year endpoint rows:\n{duplicates.to_string(index=False)}")

    years_by_country = endpoints.groupby("country")["year"].agg(list)
    invalid_countries = years_by_country[
        years_by_country.map(lambda years: sorted(years) != [START_YEAR, END_YEAR])
    ]
    if len(years_by_country) != EXPECTED_COUNTRY_COUNT or not invalid_countries.empty:
        raise ValueError(
            "Expected 27 countries with exactly one row for each endpoint year; "
            f"found {len(years_by_country)} countries. Invalid coverage: "
            f"{invalid_countries.to_dict()}"
        )

    comparison = endpoints.pivot(
        index="country", columns="year", values="co2_per_capita"
    ).sort_index()
    nonpositive_baselines = comparison.index[comparison[START_YEAR] <= 0].tolist()
    if nonpositive_baselines:
        raise ValueError(
            f"Cannot calculate percentage cuts with nonpositive 2000 values: "
            f"{nonpositive_baselines}"
        )

    comparison["cut_tonnes_per_person"] = (
        comparison[START_YEAR] - comparison[END_YEAR]
    )
    comparison["cut_percent"] = (
        comparison["cut_tonnes_per_person"] / comparison[START_YEAR] * 100
    )
    return comparison


def print_rankings(comparison: pd.DataFrame) -> None:
    tonnes_ranking = comparison.sort_values(
        "cut_tonnes_per_person", ascending=False, kind="mergesort"
    ).head(3)
    percent_ranking = comparison.sort_values(
        "cut_percent", ascending=False, kind="mergesort"
    ).head(3)

    print("\nLargest cuts in tonnes per person:")
    for rank, (country, row) in enumerate(tonnes_ranking.iterrows(), start=1):
        print(
            f"{rank}. {country}: "
            f"{START_YEAR} = {row[START_YEAR]:.2f} tonnes per person; "
            f"{END_YEAR} = {row[END_YEAR]:.2f} tonnes per person; "
            f"cut = {row['cut_tonnes_per_person']:.2f} tonnes per person "
            f"({row['cut_percent']:.2f}%)."
        )

    print("\nLargest cuts in percent of 2000 emissions per person:")
    for rank, (country, row) in enumerate(percent_ranking.iterrows(), start=1):
        print(
            f"{rank}. {country}: "
            f"{START_YEAR} = {row[START_YEAR]:.2f} tonnes per person; "
            f"{END_YEAR} = {row[END_YEAR]:.2f} tonnes per person; "
            f"cut = {row['cut_percent']:.2f}% "
            f"({row['cut_tonnes_per_person']:.2f} tonnes per person)."
        )


def save_chart(comparison: pd.DataFrame) -> None:
    chart_data = comparison.sort_values(
        "cut_tonnes_per_person", ascending=True, kind="mergesort"
    )
    cuts = chart_data["cut_tonnes_per_person"]
    colors = ["#c44e52" if cut < 0 else "#4c956c" for cut in cuts]

    fig, ax = plt.subplots(figsize=(13, 7))
    ax.bar(chart_data.index, cuts, color=colors)
    ax.axhline(0, color="black", linewidth=0.9)
    ax.set_xlabel("EU country")
    ax.set_ylabel("Cut in CO2 emissions per person (tonnes per person)")
    ax.set_title(
        "Cut in CO2 emissions per person, 2000 to 2024 "
        "(above zero: lower in 2024)"
    )
    ax.tick_params(axis="x", labelrotation=55)
    ax.margins(y=0.12)
    fig.tight_layout()

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(CHART_PATH, dpi=150, metadata={"Description": f"Source: {DATASET_SOURCE}"})
    plt.close(fig)
    print(f"\nChart saved to {CHART_PATH.relative_to(ROOT_DIR)}")


def main() -> None:
    comparison = load_comparison()
    print_rankings(comparison)
    save_chart(comparison)


if __name__ == "__main__":
    main()
