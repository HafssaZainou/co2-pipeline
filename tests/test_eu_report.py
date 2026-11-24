import matplotlib

matplotlib.use("Agg")  # draw charts without opening a window
import matplotlib.pyplot as plt

import pandas as pd
import pytest

import eu_report as r


@pytest.fixture(scope="module")
def df():
    return r.load()


@pytest.fixture(scope="module")
def owid_eu(df):
    """Our World in Data's own row for the 27 member states."""
    return df[df["country"] == "European Union (27)"].set_index("year")


def test_report_runs():
    r.main()

def test_all_27_states(df):
    eu = r.eu_members(df)
    assert eu["country"].nunique() == 27

def test_latest_year_is_2024(df):
    eu = r.eu_members(df)
    assert eu["year"].max() == 2024 

def test_missing_consumption_is_not_zero():
    tiny = pd.DataFrame({
        "year": [2024, 2024],
        "co2": [1.0, 2.0],
        "consumption_co2": [float("nan"), float("nan")],
    })
    totals = r.eu_totals(tiny)
    assert pd.isna(totals.loc[2024, "consumption_co2"])

def test_per_person_matches_owid(df, owid_eu):
    pp = r.per_person(r.eu_members(df))
    assert pp[1990] == pytest.approx(owid_eu.loc[1990, "co2_per_capita"], abs=0.01)

def test_biggest_cuts_starts_in_the_base_year():
    toy = pd.DataFrame({"country": ["A", "A", "A"], "year": [1990, 1991, 2024], "co2_per_capita": [10.0, 9.0, 5.0]})
    cuts = r.biggest_cuts(toy)
    assert cuts.loc["A", "tonnes"] == -5.0
    assert cuts.loc["A", "percent"] == -50.0

def test_chart_label_names_the_unit(tmp_path):
    plt.close("all")
    totals = pd.DataFrame({"co2": [3800.0, 2400.0], "consumption_co2": [4000.0, 2600.0]}, index=[1990, 2024])
    r.chart(totals, first=1990, latest=2024, path=tmp_path / "c.png")
    ax = plt.gcf().axes[0]
    assert "Mt" in ax.get_ylabel()

def test_chart_y_axis_starts_at_zero(tmp_path):
    plt.close("all")
    totals = pd.DataFrame({"co2": [3800.0, 2400.0], "consumption_co2": [4000.0, 2600.0]}, index=[1990, 2024])
    r.chart(totals, first=1990, latest=2024, path=tmp_path / "c.png")
    ax = plt.gcf().axes[0]
    assert ax.get_ylim()[0] == 0

def test_world_share_matches_owid(df, owid_eu):
    share = r.world_share(df, r.eu_members (df))
    assert share[1990] == pytest.approx(owid_eu.loc[1990, "share_global_co2"], abs=0.1)