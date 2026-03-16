import pandas as pd


def row_to_metals(row):
    """
    Convert a dataframe row into metals list format
    required by index functions.
    """
    metals = []

    for metal, value in row.items():
        metals.append({
            "metal": metal,
            "measured": value
        })

    return metals


def analyze_dataset(file, index_function, index_name):
    """
    Generic dataset analyzer for any pollution index.
    """

    # Support CSV and Excel
    if file.filename.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    results = []

    for _, row in df.iterrows():
        metals = row_to_metals(row)
        value = index_function(metals)
        results.append(value)

    df[index_name] = results

    return df