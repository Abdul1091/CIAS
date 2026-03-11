from app.services.indices.cf import calculate_cf
from typing import List, Dict

def calculate_pli(metals: List[Dict[str, float]]) -> float:
    """
    Calculate Pollution Load Index (PLI) from a list of metals.

    PLI = (CF1 * CF2 * ... * CFn)^(1/n)
    where CF = Contamination Factor for each metal

    Args:
        metals: List of dicts with keys:
            - metal: str
            - measured: float

    Returns:
        float: PLI value rounded to 3 decimals or None if CF cannot be calculated
    """
    cf_dict = calculate_cf(metals)
    if not cf_dict:
        return None  # Defensive: no valid CFs

    cf_values = [v for v in cf_dict.values() if v is not None]

    if not cf_values:
        return None

    n = len(cf_values)
    product = 1.0
    for cf in cf_values:
        product *= cf

    pli = product ** (1/n)
    return round(pli, 3)