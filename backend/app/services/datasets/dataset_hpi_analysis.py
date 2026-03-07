import pandas as pd
from app.services.indices.hpi import calculate_hpi


def analyze_dataset(file_path):
    df = pd.read_csv(file_path)
    results = []

    for _, row in df.iterrows():
        metals = []
        for metal in df.columns:
            metals.append({
                "metal": metal,
                "measured": row[metal]
            })

        hpi = calculate_hpi(metals)
        results.append(hpi)

    df["HPI"] = results

    return df