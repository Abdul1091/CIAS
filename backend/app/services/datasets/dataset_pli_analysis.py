import pandas as pd
from app.services.indices.pli import calculate_pli
from app.services.datasets.dataset_analyzer import analyze_dataset

def analyze_pli_dataset(file):
    return analyze_dataset(file, calculate_pli, "PLI")