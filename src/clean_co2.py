import pandas as pd
import os

# The 27 EU member states, spelled exactly as in the Our World in Data file
EU27_COUNTRIES = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia",
    "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
    "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg",
    "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia",
    "Slovenia", "Spain", "Sweden",
]

# Columns we need from the raw data
REQUIRED_COLUMNS = ["country", "iso_code", "year", "population", "co2", "co2_per_capita"]

# Input and output paths
RAW_DATA_PATH = "data/raw/owid-co2-data.csv"
PROCESSED_DATA_PATH = "data/processed/co2_eu.csv"

print(f"Reading raw data from: {RAW_DATA_PATH}")
df = pd.read_csv(RAW_DATA_PATH, usecols=REQUIRED_COLUMNS)
print(f"Total rows in raw data: {len(df)}")

# Filter to EU27 countries
print("\nFiltering to EU27 countries...")
eu27_df = df[df["country"].isin(EU27_COUNTRIES)].copy()
print(f"Rows after country filter: {len(eu27_df)}")

# Find missing countries
missing_countries = set(EU27_COUNTRIES) - set(eu27_df["country"])
if missing_countries:
    print(f"WARNING: The following EU27 countries are missing from the data: {sorted(missing_countries)}")
else:
    print("All EU27 countries are present in the data")

# Filter to years 2000-2024
print("\nFiltering to years 2000-2024...")
eu27_df = eu27_df[(eu27_df["year"] >= 2000) & (eu27_df["year"] <= 2024)]
print(f"Rows after year filter: {len(eu27_df)}")

# Check for missing values in required columns
print("\nChecking for missing values...")
missing_population = eu27_df["population"].isna().sum()
missing_co2 = eu27_df["co2"].isna().sum()
missing_co2_per_capita = eu27_df["co2_per_capita"].isna().sum()

if missing_population > 0:
    print(f"WARNING: {missing_population} rows have missing population values")
if missing_co2 > 0:
    print(f"WARNING: {missing_co2} rows have missing CO2 values")
if missing_co2_per_capita > 0:
    print(f"WARNING: {missing_co2_per_capita} rows have missing CO2 per capita values")

# Create output directory if it doesn't exist
os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)

# Write the processed data
print(f"\nWriting processed data to: {PROCESSED_DATA_PATH}")
eu27_df.to_csv(PROCESSED_DATA_PATH, index=False)
print(f"Successfully wrote {len(eu27_df)} rows to {PROCESSED_DATA_PATH}")