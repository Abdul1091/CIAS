from app.services.reference_loader import get_reference_data

def calculate_hei(metals_data):
    reference = get_reference_data()
    hei = 0

    for metal in metals_data:
        name = metal["metal"]
        measured = metal["measured"]

        if name not in reference:
            continue

        permissible = reference[name]["permissible"]

        if permissible == 0:
            continue

        hei += measured / permissible

    return round(hei, 3) if hei != 0 else None