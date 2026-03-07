import json
from pathlib import Path


REFERENCE_FILE = Path(__file__).resolve().parents[2] / "reference_data" / "water_standards.json"

def load_reference_data():
    with open(REFERENCE_FILE) as f:
        return json.load(f)


def calculate_hpi(metals_data):
    reference = load_reference_data()
    numerator = 0
    denominator = 0

    for metal in metals_data:
        name = metal["metal"]
        measured = metal["measured"]

        if name not in reference:
            continue

        ideal = reference[name]["ideal"]
        permissible = reference[name]["permissible"]

        if permissible == ideal:
            continue

        qi = ((measured - ideal) / (permissible - ideal)) * 100
        wi = 1 / permissible

        numerator += qi * wi
        denominator += wi

    if denominator == 0:
        return None

    return round(numerator / denominator, 3)