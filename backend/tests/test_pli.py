import pytest
from app.services.indices.pli import calculate_pli

def test_calculate_pli_basic(monkeypatch):
    reference = {
        "Pb": {"background": 0.02},
        "Cd": {"background": 0.005}
    }

    def mock_cf(metals):
        return {"Pb": 2.0, "Cd": 2.0}

    monkeypatch.setattr("app.services.indices.pli.calculate_cf", mock_cf)

    metals = [{"metal": "Pb", "measured": 0.04}, {"metal": "Cd", "measured": 0.01}]
    pli = calculate_pli(metals)
    assert pli == 2.0

def test_calculate_pli_empty(monkeypatch):
    def mock_cf(metals):
        return {}
    monkeypatch.setattr("app.services.indices.pli.calculate_cf", mock_cf)
    assert calculate_pli([]) is None

def test_calculate_pli_none_cf(monkeypatch):
    def mock_cf(metals):
        return None
    monkeypatch.setattr("app.services.indices.pli.calculate_cf", mock_cf)
    metals = [{"metal": "Pb", "measured": 0.05}]
    assert calculate_pli(metals) is None

def test_calculate_pli_rounding(monkeypatch):
    def mock_cf(metals):
        return {"Pb": 2.3333, "Cd": 1.6666}
    monkeypatch.setattr("app.services.indices.pli.calculate_cf", mock_cf)
    metals = [{"metal": "Pb", "measured": 0.0467}, {"metal": "Cd", "measured": 0.0083}]
    pli = calculate_pli(metals)
    # geometric mean: (2.3333*1.6666)^0.5 ≈ 1.975
    assert pli == round((2.3333*1.6666)**0.5, 3)