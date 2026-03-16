from app.services.reference_loader import get_reference_data


def calculate_hpi(metals_data):
    reference = get_reference_data()
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