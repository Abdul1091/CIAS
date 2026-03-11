import pytest
from app.services.indices.hei import calculate_hei


def test_calculate_hei_basic(monkeypatch):
    """Test HEI calculation with known values"""

    reference = {
        "Pb": {"permissible": 0.1},
        "Cd": {"permissible": 0.05}
    }

    def mock_load_standards():
        return reference

    monkeypatch.setattr(
        "app.services.indices.hei.load_reference_data",
        mock_load_standards
    )

    metals = [
        {"metal": "Pb", "measured": 0.05},
        {"metal": "Cd", "measured": 0.025}
    ]

    hei = calculate_hei(metals)

    # HEI = (0.05/0.1) + (0.025/0.05)
    #     = 0.5 + 0.5
    #     = 1.0
    assert round(hei, 3) == 1.0


def test_calculate_hei_empty(monkeypatch):
    """Return 0 if metals list empty or no known metals"""

    def mock_load_standards():
        return {"Pb": {"permissible": 0.1}}

    monkeypatch.setattr(
        "app.services.indices.hei.load_reference_data",
        mock_load_standards
    )

    assert calculate_hei([]) is None

    metals = [{"metal": "Zn", "measured": 0.1}]
    assert calculate_hei(metals) is None


def test_calculate_hei_negative_values(monkeypatch):
    """HEI should handle negative measured values"""

    def mock_load_standards():
        return {"Pb": {"permissible": 0.1}}

    monkeypatch.setattr(
        "app.services.indices.hei.load_reference_data",
        mock_load_standards
    )

    metals = [{"metal": "Pb", "measured": -0.05}]
    hei = calculate_hei(metals)

    assert round(hei, 3) == -0.5