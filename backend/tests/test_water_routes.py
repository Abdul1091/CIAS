import io
import json
from app.models.water_quality_report import WaterQualityReport
from app import db
import pytest

def test_compute_hpi(client):
    # Test POST /api/water/hpi
    payload = {
        "location": "Test River",
        "metals": [
            {"metal": "Pb", "measured": 0.05},
            {"metal": "Cd", "measured": 0.01}
        ]
    }
    response = client.post("/api/water/hpi", json=payload)
    assert response.status_code == 200

    data = response.get_json()
    assert "HPI" in data
    assert "status" in data
    assert "report_id" in data
    assert isinstance(data["HPI"], float)
    assert data["status"] in ["Safe", "Polluted"]

def test_compute_hpi_no_metals(client):
    # Should return 400 if metals missing
    payload = {"location": "Empty River"}
    response = client.post("/api/water/hpi", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_dataset_hpi(client):
    # Test POST /api/water/hpi/dataset with a small CSV
    csv_content = "Pb,Cd\n0.05,0.01\n0.1,0.02"
    data = {
        "file": (io.BytesIO(csv_content.encode()), "test.csv")
    }
    response = client.post("/api/water/hpi/dataset", content_type="multipart/form-data", data=data)
    assert response.status_code == 200

    # Convert JSON string to Python list
    json_data = json.loads(response.data)
    assert len(json_data) == 2  # Two rows

    # Each row should contain expected keys
    for row in json_data:
        assert "HPI" in row
        assert "Pb" in row
        assert "Cd" in row

@pytest.fixture
def add_sample_reports(app):
    """Add some sample HPI reports to the test DB."""
    with app.app_context():
        db.create_all()
        report1 = WaterQualityReport(
            location="River Niger",
            hpi_value=50.0,
            hei_value=5.0,
            status="Safe",
            metals_data=[{"metal": "Pb", "measured": 0.05}]
        )
        report2 = WaterQualityReport(
            location="River Kaduna",
            hpi_value=120.0,
            hei_value=15.0,
            status="Polluted",
            metals_data=[{"metal": "Cd", "measured": 0.06}]
        )
        db.session.add_all([report1, report2])
        db.session.commit()
        yield
        db.drop_all()


def test_get_all_reports(client, add_sample_reports):
    """Test GET /api/water/hpi"""
    response = client.get("/api/water/hpi")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["location"] == "River Niger"
    assert data[1]["status"] == "Polluted"


def test_get_single_report(client, add_sample_reports):
    """Test GET /api/water/hpi/<report_id>"""
    response = client.get("/api/water/hpi/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["id"] == 1
    assert data["location"] == "River Niger"

    # Test 404 for non-existent report
    response = client.get("/api/water/hpi/999")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data


def test_dataset_hei(client):
    """Test POST /api/water/hei/dataset with CSV"""

    csv_content = "Pb,Cd\n0.05,0.01\n0.1,0.02"

    data = {
        "file": (io.BytesIO(csv_content.encode()), "test.csv")
    }

    response = client.post(
        "/api/water/hei/dataset",
        content_type="multipart/form-data",
        data=data
    )

    assert response.status_code == 200

    json_data = json.loads(response.data)

    assert len(json_data) == 2

    for row in json_data:
        assert "HEI" in row
        assert "Pb" in row
        assert "Cd" in row


def test_compute_hei(client):
    """Test POST /api/water/hei"""

    payload = {
        "metals": [
            {"metal": "Pb", "measured": 0.05},
            {"metal": "Cd", "measured": 0.01}
        ]
    }

    response = client.post("/api/water/hei", json=payload)

    assert response.status_code == 200

    data = response.get_json()

    assert "HEI" in data
    assert "status" in data
    assert isinstance(data["HEI"], float)


def test_compute_hei_no_metals(client):
    """Should return 400 if metals missing"""

    response = client.post("/api/water/hei", json={})

    assert response.status_code == 400

    data = response.get_json()

    assert "error" in data