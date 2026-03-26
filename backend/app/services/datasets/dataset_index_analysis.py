from app.services.datasets.dataset_analyzer import analyze_dataset

from app.services.indices.hpi import calculate_hpi
from app.services.indices.hei import calculate_hei
from app.services.indices.pli import calculate_pli
from app.services.indices.cf import calculate_cf


INDEX_DATASET_FUNCTIONS = {
    "HPI": calculate_hpi,
    "HEI": calculate_hei,
    "PLI": calculate_pli,
    "CF": calculate_cf,
}

def analyze_index_dataset(file, index):
    """
    Entry point to analyze a dataset for a given index.
    """
    
    if index not in INDEX_DATASET_FUNCTIONS:
        raise ValueError("Invalid index")

    return analyze_dataset(file, INDEX_DATASET_FUNCTIONS[index], index)