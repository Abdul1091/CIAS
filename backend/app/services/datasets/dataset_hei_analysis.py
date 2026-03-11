import pandas as pd
from app.services.indices.hei import calculate_hei


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

        hei = calculate_hei(metals)
        results.append(hei)

    df["HEI"] = results

    return df