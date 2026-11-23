import matplotlib

matplotlib.use("Agg")  # draw charts without opening a window

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