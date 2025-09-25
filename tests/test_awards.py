import pytest

@pytest.fixture
def award_payload():
    return {
        "title": "Top Engineer Award",
        "description": "Recognized for outstanding contributions to backend infrastructure and team mentorship.",
        "icon": "./images/awards/top-engineer.png",
        "date": "June 2025"
    }

@pytest.fixture
def created_award(client, award_payload):
    response = client.post("/v1/awards/", json=award_payload)
    assert response.status_code == 201
    return response.json()

def test_create_award(client, award_payload):
    response = client.post("/v1/awards/", json=award_payload)
    assert response.status_code == 201
    award = response.json()
    assert award["title"] == award_payload["title"]
    assert award["description"] == award_payload["description"]
    assert award["icon"] == award_payload["icon"]
    assert award["date"] == award_payload["date"]

def test_get_all_awards(client, created_award):
    response = client.get("/v1/awards/")
    assert response.status_code == 200
    awards = response.json()
    assert isinstance(awards, list)
    assert any(a["id"] == created_award["id"] for a in awards)

def test_get_single_award(client, created_award):
    award_id = created_award["id"]
    response = client.get(f"/v1/awards/{award_id}")
    assert response.status_code == 200
    award = response.json()
    assert award["title"] == created_award["title"]

def test_update_award(client, created_award):
    award_id = created_award["id"]
    update_payload = {
        "title": "Updated Engineer Award",
        "description": "Updated description for the award."
    }
    response = client.patch(f"/v1/awards/{award_id}", json=update_payload)
    assert response.status_code == 200
    updated = response.json()
    assert updated["title"] == "Updated Engineer Award"
    assert updated["description"] == "Updated description for the award."

def test_delete_award(client, created_award):
    award_id = created_award["id"]
    response = client.delete(f"/v1/awards/{award_id}")
    assert response.status_code == 204

    # Confirm deletion
    response = client.get(f"/v1/awards/{award_id}")
    assert response.status_code == 404
