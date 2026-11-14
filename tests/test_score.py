# test_score.py — Layer 1 test: data + scoring only (no Streamlit, no map)
#
# Run from the martian-map folder:  python3 test_score.py
# It loads data/sites.csv, recomputes every Survival Score with the v2
# formula, and prints PASS/FAIL per site. If this passes, Layer 1 is solid
# and any bug later is in the UI layers, not the data.

import pandas as pd
from pathlib import Path

CSV_PATH = Path(__file__).parent.parent / "data" / "sites.csv"


def survival_score(row):
    """v2 formula (see docs/SURVIVAL_SCORE.md)."""
    return round(
        (
            row["resource_score"] * 0.25
            + row["temp_radiation_score"] * 0.20
            + row["terrain_score"] * 0.20
            + row["hazard_safety_score"] * 0.15
            + row["pressure_score"] * 0.10
            + row["air_score"] * 0.10
        )
        * 20
    )


def main():
    sites = pd.read_csv(CSV_PATH)
    print(f"Loaded {len(sites)} sites from {CSV_PATH}")
    all_ok = True
    for _, row in sites.iterrows():
        computed = survival_score(row)
        stored = int(row["survival_score"])
        status = "PASS" if computed == stored else "FAIL"
        if computed != stored:
            all_ok = False
        print(f"  {status}  {row['name']}: computed {computed}, stored {stored}")
    print("ALL SCORES MATCH" if all_ok else "MISMATCH — fix sites.csv before going further")


if __name__ == "__main__":
    main()
