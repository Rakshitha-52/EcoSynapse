import pandas as pd
from pathlib import Path


# ============================================================
# ECOSYNAPSE - DATASET AUDIT
# File: 01_dataset_audit.py
#
# Purpose:
#   Inspect all master datasets before cleaning and feature
#   engineering.
#
# IMPORTANT:
#   This script DOES NOT modify any dataset.
# ============================================================


# ============================================================
# 1. CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data" / "master"


DATASETS = [
    "agricultural_land.csv",
    "biodiversity_indicators.csv",
    "biodiversity_observations.csv",
    "climatewatch_ghg.csv",
    "environmental_indicators.csv",
    "forest_area.csv",
    "pesticide_use.csv",
]


# World Bank CSV files usually contain several metadata rows
# before the actual column header.
WORLD_BANK_DATASETS = {
    "agricultural_land.csv",
    "forest_area.csv",
}


# ============================================================
# 2. LOAD DATASET
# ============================================================

def load_dataset(file_path):
    """
    Load a CSV safely.

    World Bank datasets require skiprows=4 because their
    downloaded CSV contains metadata before the actual table.
    """

    if file_path.name in WORLD_BANK_DATASETS:

        df = pd.read_csv(
            file_path,
            skiprows=4,
            low_memory=False
        )

    else:

        df = pd.read_csv(
            file_path,
            low_memory=False
        )

    return df


# ============================================================
# 3. BASIC INFORMATION
# ============================================================

def print_basic_information(df):

    print("\n" + "-" * 80)
    print("BASIC INFORMATION")
    print("-" * 80)

    print(f"Rows       : {len(df):,}")
    print(f"Columns    : {len(df.columns)}")
    print(f"Memory use : {df.memory_usage(deep=True).sum() / (1024 ** 2):.2f} MB")


# ============================================================
# 4. COLUMN INFORMATION
# ============================================================

def print_columns(df):

    print("\n" + "-" * 80)
    print("COLUMN NAMES")
    print("-" * 80)

    for i, column in enumerate(df.columns, start=1):

        print(f"{i:>3}. {column}")


# ============================================================
# 5. DATA TYPES
# ============================================================

def print_data_types(df):

    print("\n" + "-" * 80)
    print("DATA TYPES")
    print("-" * 80)

    for column in df.columns:

        print(
            f"{column:<40} {str(df[column].dtype)}"
        )


# ============================================================
# 6. MISSING VALUES
# ============================================================

def print_missing_values(df):

    print("\n" + "-" * 80)
    print("MISSING VALUES")
    print("-" * 80)

    missing = df.isnull().sum()

    missing = missing[missing > 0]

    if len(missing) == 0:

        print("No missing values.")

        return

    for column, count in missing.sort_values(
        ascending=False
    ).items():

        percentage = (
            count / len(df)
        ) * 100

        print(
            f"{column:<40} "
            f"{count:>10,} "
            f"({percentage:>6.2f}%)"
        )


# ============================================================
# 7. DUPLICATES
# ============================================================

def print_duplicates(df):

    print("\n" + "-" * 80)
    print("DUPLICATE ROWS")
    print("-" * 80)

    duplicates = df.duplicated().sum()

    print(f"Duplicate rows: {duplicates:,}")

    if duplicates > 0:

        percentage = (
            duplicates / len(df)
        ) * 100

        print(
            f"Duplicate percentage: {percentage:.2f}%"
        )


# ============================================================
# 8. FIRST ROWS
# ============================================================

def print_sample(df):

    print("\n" + "-" * 80)
    print("FIRST 3 ROWS")
    print("-" * 80)

    print(
        df.head(3).to_string(index=False)
    )


# ============================================================
# 9. UNIQUE VALUES
# ============================================================

def print_low_cardinality_columns(df):

    print("\n" + "-" * 80)
    print("LOW-CARDINALITY COLUMNS")
    print("(Columns having <= 20 unique values)")
    print("-" * 80)

    found = False

    for column in df.columns:

        unique_count = df[column].nunique(
            dropna=True
        )

        if unique_count <= 20:

            found = True

            print(
                f"\n{column} "
                f"({unique_count} unique values):"
            )

            values = (
                df[column]
                .dropna()
                .unique()
            )

            for value in values[:20]:

                print(f"  - {value}")

    if not found:

        print("No low-cardinality columns found.")


# ============================================================
# 10. YEAR / TIME INFORMATION
# ============================================================

def print_time_information(df):

    print("\n" + "-" * 80)
    print("TIME INFORMATION")
    print("-" * 80)

    time_columns = []

    for column in df.columns:

        column_lower = column.lower()

        if any(
            keyword in column_lower
            for keyword in [
                "year",
                "date",
                "time",
                "period"
            ]
        ):

            time_columns.append(column)

    if not time_columns:

        print("No obvious time/date columns found.")

        return

    for column in time_columns:

        print(f"\nColumn: {column}")

        values = df[column].dropna()

        if len(values) == 0:

            print("  No values.")

            continue

        # Try numeric year
        numeric_values = pd.to_numeric(
            values,
            errors="coerce"
        ).dropna()

        if len(numeric_values) > 0:

            print(
                f"  Minimum: {numeric_values.min()}"
            )

            print(
                f"  Maximum: {numeric_values.max()}"
            )

        else:

            print(
                "  Sample values:"
            )

            print(
                values.astype(str)
                .head(10)
                .tolist()
            )


# ============================================================
# 11. GEOGRAPHIC INFORMATION
# ============================================================

def print_geographic_information(df):

    print("\n" + "-" * 80)
    print("GEOGRAPHIC INFORMATION")
    print("-" * 80)

    geographic_keywords = [
        "country",
        "state",
        "district",
        "latitude",
        "longitude",
        "location",
        "locality",
        "region",
        "area"
    ]

    geographic_columns = []

    for column in df.columns:

        column_lower = column.lower()

        if any(
            keyword in column_lower
            for keyword in geographic_keywords
        ):

            geographic_columns.append(column)

    if not geographic_columns:

        print("No obvious geographic columns found.")

        return

    for column in geographic_columns:

        unique_count = df[column].nunique(
            dropna=True
        )

        print(
            f"{column:<40} "
            f"{unique_count:,} unique values"
        )


# ============================================================
# 12. INDIA INFORMATION
# ============================================================

def print_india_information(df):

    print("\n" + "-" * 80)
    print("INDIA COVERAGE")
    print("-" * 80)

    possible_columns = [
        "REF_AREA",
        "REF_AREA_LABEL",
        "REF_AREA_ID",
        "REF_AREA_NAME",
        "COUNTRY",
        "COUNTRY_NAME",
        "Country",
        "Country Name"
    ]

    found = False

    for column in possible_columns:

        if column not in df.columns:

            continue

        found = True

        values = (
            df[column]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        india_mask = values.isin(
            [
                "ind",
                "india",
                "in"
            ]
        )

        india_count = india_mask.sum()

        print(
            f"{column:<30} "
            f"India records: {india_count:,}"
        )

    if not found:

        # Biodiversity datasets may use locality/state
        # rather than a country field.

        india_count = 0

        for column in df.columns:

            if df[column].dtype == "object":

                values = (
                    df[column]
                    .astype(str)
                    .str.lower()
                )

                india_count += values.str.contains(
                    r"\bindia\b",
                    regex=True,
                    na=False
                ).sum()

        if india_count > 0:

            print(
                f"India mentions found across text columns: "
                f"{india_count:,}"
            )

        else:

            print(
                "No India records/mentions detected "
                "using available checks."
            )


# ============================================================
# 13. INDICATOR INFORMATION
# ============================================================

def print_indicator_information(df):

    print("\n" + "-" * 80)
    print("INDICATOR INFORMATION")
    print("-" * 80)

    indicator_columns = [
        "INDICATOR",
        "INDICATOR_LABEL",
        "INDICATOR_ID",
        "INDICATOR_NAME"
    ]

    found = False

    for column in indicator_columns:

        if column not in df.columns:

            continue

        found = True

        unique_values = (
            df[column]
            .dropna()
            .unique()
        )

        print(
            f"\n{column}: "
            f"{len(unique_values)} unique values"
        )

        for value in unique_values[:30]:

            print(f"  - {value}")

    if not found:

        print("No indicator column found.")


# ============================================================
# 14. NUMERIC COLUMNS
# ============================================================

def print_numeric_columns(df):

    print("\n" + "-" * 80)
    print("NUMERIC COLUMNS")
    print("-" * 80)

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    if len(numeric_columns) == 0:

        print("No numeric columns found.")

        return

    for column in numeric_columns:

        print(f"\n{column}")

        print(
            f"  Min    : {df[column].min()}"
        )

        print(
            f"  Max    : {df[column].max()}"
        )

        print(
            f"  Mean   : {df[column].mean()}"
        )

        print(
            f"  Median : {df[column].median()}"
        )


# ============================================================
# 15. UNIQUE COUNTRY VALUES
# ============================================================

def print_country_values(df):

    print("\n" + "-" * 80)
    print("COUNTRY INFORMATION")
    print("-" * 80)

    possible_columns = [
        "REF_AREA_LABEL",
        "REF_AREA_NAME",
        "COUNTRY",
        "COUNTRY_NAME",
        "Country",
        "Country Name"
    ]

    for column in possible_columns:

        if column not in df.columns:

            continue

        unique_values = (
            df[column]
            .dropna()
            .unique()
        )

        print(
            f"\n{column}: "
            f"{len(unique_values):,} unique countries/areas"
        )

        print(
            list(unique_values[:30])
        )

        return

    print(
        "No standard country column found."
    )


# ============================================================
# 16. DATASET AUDIT
# ============================================================

def audit_dataset(file_path):

    print("\n\n")
    print("#" * 80)
    print(f"DATASET: {file_path.name}")
    print("#" * 80)

    try:

        df = load_dataset(file_path)

    except Exception as error:

        print("\nERROR READING DATASET")
        print("-" * 80)
        print(error)

        return

    # Run all audit sections

    print_basic_information(df)

    print_columns(df)

    print_data_types(df)

    print_missing_values(df)

    print_duplicates(df)

    print_sample(df)

    print_low_cardinality_columns(df)

    print_time_information(df)

    print_geographic_information(df)

    print_india_information(df)

    print_indicator_information(df)

    print_numeric_columns(df)

    print_country_values(df)


# ============================================================
# 17. MAIN
# ============================================================

def main():

    print("\n")
    print("#" * 80)
    print("              ECOSYNAPSE DATASET AUDIT")
    print("#" * 80)

    print(
        f"\nData directory:\n{DATA_DIR}"
    )

    print(
        f"\nDatasets to inspect: {len(DATASETS)}"
    )

    print("\n")

    for dataset_name in DATASETS:

        file_path = DATA_DIR / dataset_name

        if not file_path.exists():

            print("\n" + "=" * 80)
            print(
                f"MISSING DATASET: {dataset_name}"
            )
            print("=" * 80)

            continue

        audit_dataset(file_path)

    print("\n\n")
    print("#" * 80)
    print("                 AUDIT COMPLETE")
    print("#" * 80)
    print("\n")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()