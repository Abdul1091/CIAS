import pytest
from app.services.indices.cf import calculate_cf


def test_calculate_cf_basic(monkeypatch):

    reference = {
        "Pb": {"background": 0.02},
        "Cd": {"background": 0.005}
    }

    def mock_load():
        return reference

    monkeypatch.setattr(
        "app.services.indices.cf.load_reference_data",
        mock_load
    )

    metals = [
        {"metal": "Pb", "measured": 0.04},
        {"metal": "Cd", "measured": 0.01}
    ]

    cf = calculate_cf(metals)

    assert cf["Pb"] == 2.0
    assert cf["Cd"] == 2.0


def test_calculate_cf_empty(monkeypatch):

    def mock_load():
        return {"Pb": {"background": 0.02}}

    monkeypatch.setattr(
        "app.services.indices.cf.load_reference_data",
        mock_load
    )

    assert calculate_cf([]) is None


def test_calculate_cf_unknown_metal(monkeypatch):

    def mock_load():
        return {"Pb": {"background": 0.02}}

    monkeypatch.setattr(
        "app.services.indices.cf.load_reference_data",
        mock_load
    )

    metals = [{"metal": "Zn", "measured": 0.2}]

    assert calculate_cf(metals) is None


def test_calculate_cf_background_zero(monkeypatch):

    reference = {
        "Pb": {"background": 0}
    }

    def mock_load():
        return reference

    monkeypatch.setattr(
        "app.services.indices.cf.load_reference_data",
        mock_load
    )

    metals = [{"metal": "Pb", "measured": 0.05}]

    assert calculate_cf(metals) is None


def test_calculate_cf_negative_values(monkeypatch):

    reference = {
        "Pb": {"background": 0.02}
    }

    def mock_load():
        return reference

    monkeypatch.setattr(
        "app.services.indices.cf.load_reference_data",
        mock_load
    )

    metals = [{"metal": "Pb", "measured": -0.02}]

    cf = calculate_cf(metals)

    assert cf["Pb"] == -1.0


def test_calculate_cf_missing_background(monkeypatch):

    reference = {
        "Pb": {}
    }

    def mock_load():
        return reference

    monkeypatch.setattr(
        "app.services.indices.cf.load_reference_data",
        mock_load
    )

    metals = [{"metal": "Pb", "measured": 0.02}]

    assert calculate_cf(metals) is None


def test_calculate_cf_multiple_metals(monkeypatch):

    reference = {
        "Pb": {"background": 0.02},
        "Cd": {"background": 0.005}
    }

    def mock_load():
        return reference

    monkeypatch.setattr(
        "app.services.indices.cf.load_reference_data",
        mock_load
    )

    metals = [
        {"metal": "Pb", "measured": 0.04},
        {"metal": "Cd", "measured": 0.01}
    ]

    cf = calculate_cf(metals)

    assert cf["Pb"] == 2.0
    assert cf["Cd"] == 2.0


def test_calculate_cf_rounding(monkeypatch):

    reference = {
        "Pb": {"background": 0.03}
    }

    def mock_load():
        return reference

    monkeypatch.setattr(
        "app.services.indices.cf.load_reference_data",
        mock_load
    )

    metals = [{"metal": "Pb", "measured": 0.1}]

    cf = calculate_cf(metals)

    assert cf["Pb"] == round(0.1 / 0.03, 3)