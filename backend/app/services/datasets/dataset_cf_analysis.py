import pandas as pd
from app.services.indices.cf import calculate_cf


def analyze_dataset(file):
    df = pd.read_csv(file)
    results = []

    for _, row in df.iterrows():
        metals = []

        for metal in df.columns:
            metals.append({
                "metal": metal,
                "measured": row[metal]
            })

        cf_values = calculate_cf(metals)
        results.append(cf_values)

    df["CF"] = results

    return df