import pandas as pd
from app.services.index_classifier import classify_cf
from app.services.indices.cf import calculate_cf
from app.services.pollution_source import get_dominant_metal


def row_to_metals(row):
    """Convert a dataframe row into metals list format for index functions."""
    return [{"metal": metal, "measured": value} for metal, value in row.items()]


def build_row_reasoning(index_results):
    """Build overall reasoning list for a single row."""
    reasoning = []
    for index, data in index_results.items():
        if index == "pollution_source":
            continue
        classification = data.get("classification")
        if isinstance(classification, dict):
            for metal, meta in classification.items():
                reason = meta.get("reason")
                if reason:
                    reasoning.append(f"{index} {metal}: {reason}")
        elif classification:
            # For scalar indices
            reason = classification.get("reason") if isinstance(classification, dict) else classification
            reasoning.append(f"{index}: {reason}")
    return reasoning


def analyze_dataset(file, index_function, index_name):
    """
    Generic dataset analyzer for any pollution index with row_id, overall_reasoning,
    and flattened CF handling.
    """

    # Read CSV or Excel
    if file.filename.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    results_list = []

    for i, row in df.iterrows():
        metals = row_to_metals(row)
        value = index_function(metals)

        # Wrap scalar values in dict
        if isinstance(value, (int, float)):
            index_result = {index_name: {"value": value, "classification": None}}
        else:
            index_result = {index_name: {"value": value, "classification": classify_cf(value)}}

        # Add pollution source for the row
        dominant = get_dominant_metal(value if index_name == "CF" else calculate_cf(metals))
        index_result["pollution_source"] = dominant

        # Compute overall reasoning
        index_result["overall_reasoning"] = build_row_reasoning(index_result)

        # Add row_id
        index_result["row_id"] = i + 1

        results_list.append(index_result)

    # Flatten results into dataframe
    flat_rows = []
    for res in results_list:
        flat = {
            "row_id": res["row_id"],
            "overall_reasoning": res["overall_reasoning"],
            "pollution_source": res["pollution_source"]
        }

        for k, v in res.items():
            if k in ["row_id", "overall_reasoning", "pollution_source"]:
                continue

            if isinstance(v.get("value"), dict):
                for metal, val in v["value"].items():
                    flat[f"{k}_{metal}"] = val
                    flat[f"{k}_{metal}_classification"] = v["classification"].get(metal)
            else:
                flat[f"{k}_value"] = v.get("value")
                flat[f"{k}_classification"] = v.get("classification")

        flat_rows.append(flat)

    return pd.DataFrame(flat_rows)