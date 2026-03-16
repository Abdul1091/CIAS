import pandas as pd
from app.services.datasets.dataset_analyzer import analyze_dataset
from app.services.indices.hpi import calculate_hpi


def analyze_hpi_dataset(file):
    return analyze_dataset(file, calculate_hpi, "HPI")