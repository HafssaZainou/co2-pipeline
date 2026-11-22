import pandas as pd
import pytest
import hashlib


# The 27 member states, spelled as in the Our World in Data file
EU27 = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia",
    "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
    "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg",
    "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia",
    "Slovenia", "Spain", "Sweden",
]


@pytest.fixture(scope="module")
def df():
    return pd.read_csv("data/processed/co2_eu.csv")


def test_only_eu27_countries(df):
    assert set(df["country"]) == set(EU27)  # no World, no UK


def test_one_row_per_country_and_year(df):
    assert not df.duplicated(subset=["country", "year"]).any() # no duplicate combinations of country and year
    assert set(df["year"]) == set(range(2000, 2025)) # years are exactly 2000 to 2024 (range(2000, 2025))
    assert len(df) == len(EU27) * 25 # there are 27 countries times 25 years, means 675 rows


def test_no_missing_values_in_population_co2_and_co2_per_capita(df):
    columns = ["population", "co2", "co2_per_capita"]
    assert df[columns].isna().sum().sum() == 0  # no missing values in these three columns


def test_units_fit_together(df):
    calculated = df["co2"]*1_000_000/df["population"]
    assert calculated.to_numpy() == pytest.approx(df["co2_per_capita"].to_numpy(), rel=0.001)


def test_raw_data_checksum():
    with open("data/raw/owid-co2-data.csv", "rb") as f:
        checksum = hashlib.sha256(f.read()).hexdigest()
    assert checksum == "7f78e2b218ce4bb8c538bbec04fdc9a7982e8d40bff972e650df603899edd5f6"