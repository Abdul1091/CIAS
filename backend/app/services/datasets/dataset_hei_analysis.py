import pandas as pd
from app.services.datasets.dataset_analyzer import analyze_dataset
from app.services.indices.hei import calculate_hei


def analyze_hei_dataset(file):
    return analyze_dataset(file, calculate_hei, "HEI")