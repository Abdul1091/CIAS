import pytest
from app.services.indices.hpi import calculate_hpi

# Sample reference data (should match your water_standards.json for tests)
# You can mock it if needed, but here we test realistic scenarios.

def test_calculate_hpi_basic(monkeypatch):
    """Test HPI calculation for known metal values"""

    # Mock reference data
    reference = {
        "Pb": {"ideal": 0.0, "permissible": 0.1},
        "Cd": {"ideal": 0.0, "permissible": 0.05}
    }

    def mock_load_reference_data():
        return reference

    # Patch the load_reference_data function
    monkeypatch.setattr("app.services.indices.hpi.load_reference_data", mock_load_reference_data)

    metals_data = [
        {"metal": "Pb", "measured": 0.05},
        {"metal": "Cd", "measured": 0.025}
    ]

    hpi = calculate_hpi(metals_data)
    assert hpi is not None
    # Expected HPI: 
    # Pb: ((0.05-0)/(0.1-0))*100 * (1/0.1) = 50 * 10 = 500
    # Cd: ((0.025-0)/(0.05-0))*100 * (1/0.05) = 50 * 20 = 1000
    # Numerator = 500 + 1000 = 1500
    # Denominator = 1/0.1 + 1/0.05 = 10 + 20 = 30
    # HPI = 1500 / 30 = 50
    assert round(hpi, 3) == 50.0

def test_calculate_hpi_empty(monkeypatch):
    """HPI should return None if metals list is empty or no known metals"""

    def mock_load_reference_data():
        return {"Pb": {"ideal": 0, "permissible": 0.1}}

    monkeypatch.setattr("app.services.indices.hpi.load_reference_data", mock_load_reference_data)

    # Empty metals
    assert calculate_hpi([]) is None

    # Unknown metal
    metals_data = [{"metal": "Zn", "measured": 0.1}]
    assert calculate_hpi(metals_data) is None

def test_calculate_hpi_permissible_equals_ideal(monkeypatch):
    """Should skip metals where permissible == ideal"""

    def mock_load_reference_data():
        return {"Pb": {"ideal": 0.1, "permissible": 0.1}}

    monkeypatch.setattr("app.services.indices.hpi.load_reference_data", mock_load_reference_data)

    metals_data = [{"metal": "Pb", "measured": 0.1}]
    assert calculate_hpi(metals_data) is None

def test_calculate_hpi_negative_values(monkeypatch):
    """Handle measured values below ideal"""

    def mock_load_reference_data():
        return {"Pb": {"ideal": 0.0, "permissible": 0.1}}

    monkeypatch.setattr("app.services.indices.hpi.load_reference_data", mock_load_reference_data)

    metals_data = [{"metal": "Pb", "measured": -0.05}]
    hpi = calculate_hpi(metals_data)
    # Qi will be negative: ((-0.05 - 0)/0.1)*100 = -50, * wi=10 => -500 / 10 = -50
    assert round(hpi, 3) == -50.0