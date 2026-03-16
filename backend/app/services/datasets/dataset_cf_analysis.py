import pandas as pd
from app.services.datasets.dataset_analyzer import row_to_metals
from app.services.indices.cf import calculate_cf


def analyze_dataset(file):
    df = pd.read_csv(file) if file.filename.endswith(".csv") else pd.read_excel(file)
    results = []

    for _, row in df.iterrows():
        metals = row_to_metals()
        cf_values = calculate_cf(metals)
        results.append(cf_values)

    df["CF"] = results

    return df