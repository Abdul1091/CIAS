import io
import json

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