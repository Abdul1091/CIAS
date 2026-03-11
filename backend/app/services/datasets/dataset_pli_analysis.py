import pandas as pd
from app.services.indices.pli import calculate_pli
from app.services.indices.cf import calculate_cf

def analyze_dataset(file) -> pd.DataFrame:
    """
    Compute PLI for each row in a CSV/Excel dataset.
    Assumes columns are metal names, rows are measured values.
    """
    df = pd.read_csv(file) if file.filename.endswith(".csv") else pd.read_excel(file)
    pli_results = []

    for _, row in df.iterrows():
        metals_list = [{"metal": col, "measured": row[col]} for col in df.columns]
        pli = calculate_pli(metals_list)
        result = metals_list.copy()
        for item in result:
            item["measured"] = round(item["measured"], 3)
        pli_results.append({"PLI": pli, **{col: row[col] for col in df.columns}})

    return pd.DataFrame(pli_results)