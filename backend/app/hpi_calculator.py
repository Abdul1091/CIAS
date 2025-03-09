def calculate_hpi(metals_data):
    """
    Calculates the Heavy Metal Pollution Index (HPI).

    :param metals_data: List of dictionaries with keys 'metal', 'measured', 'ideal', 'permissible'
    :return: Computed HPI value
    """
    numerator = 0
    denominator = 0

    for metal in metals_data:
        Mi = metal.get("measured")
        Ii = metal.get("ideal")
        Si = metal.get("permissible")

        # Ensure values are valid numbers
        if None in (Mi, Ii, Si) or Si == 0:
            continue  # Skip invalid entries

        # Avoid division by zero
        if Si == Ii:
            continue

        Qi = ((Mi - Ii) / (Si - Ii)) * 100  # Sub-index
        Wi = 1 / Si  # Weight is inversely proportional

        numerator += Qi * Wi
        denominator += Wi

    return round(numerator / denominator, 2) if denominator != 0 else 0  # Avoid division by zero