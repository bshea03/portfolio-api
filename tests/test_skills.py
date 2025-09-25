import pytest
from app.models.skill import SkillCategory

@pytest.fixture
def skill_payload():
    return {
        "name": "FastAPI",
        "icon": "./icons/fastapi.png",
        "category": SkillCategory.backend,
        "rank": 1
    }

@pytest.fixture
def skill_payload_2():
    return {
        "name": "PostgreSQL",
        "icon": "./icons/postgres.png",
        "category": SkillCategory.backend,
        "rank": 2
    }

@pytest.fixture
def skill_payload_3():
    return {
        "name": "Docker",
        "icon": "./icons/docker.png",
        "category": SkillCategory.backend,
        "rank": 3
    }

@pytest.fixture
def created_skill(client, skill_payload):
    response = client.post("/v1/skills/", json=skill_payload)
    assert response.status_code == 201
    return response.json()

def test_create_skill_with_rank(client, skill_payload):
    response = client.post("/v1/skills/", json=skill_payload)
    assert response.status_code == 201
    skill = response.json()
    assert skill["name"] == skill_payload["name"]
    assert skill["rank"] == skill_payload["rank"]

def test_create_skill_without_rank(client):
    payload = {
        "name": "Docker",
        "icon": "./icons/docker.png",
        "category": SkillCategory.backend
    }
    response = client.post("/v1/skills/", json=payload)
    assert response.status_code == 201
    skill = response.json()
    assert skill["name"] == "Docker"
    assert isinstance(skill["rank"], int)

def test_get_all_skills_grouped(client, created_skill):
    response = client.get("/v1/skills/")
    assert response.status_code == 200
    grouped = response.json()
    assert SkillCategory.backend.value in grouped
    assert any(s["name"] == created_skill["name"] for s in grouped[SkillCategory.backend.value])

def test_get_skills_by_category(client, created_skill):
    category = created_skill["category"]
    response = client.get(f"/v1/skills/{category}")
    assert response.status_code == 200
    skills = response.json()
    assert isinstance(skills, list)
    assert any(s["id"] == created_skill["id"] for s in skills)

def test_update_skill_rank_and_name(client, created_skill):
    skill_id = created_skill["id"]
    update_payload = {
        "name": "FastAPI Pro",
        "rank": created_skill["rank"] + 1
    }
    response = client.patch(f"/v1/skills/{skill_id}", json=update_payload)
    assert response.status_code == 200
    updated = response.json()
    assert updated["name"] == "FastAPI Pro"
    assert updated["rank"] == created_skill["rank"] + 1

def test_delete_skill(client, created_skill):
    skill_id = created_skill["id"]
    response = client.delete(f"/v1/skills/{skill_id}")
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]

def test_normalize_skills(client):
    response = client.post("/v1/skills/normalize")
    assert response.status_code == 200
    assert "Ranks normalized" in response.json()["message"]

def test_rank_collision_on_insert(client, skill_payload, skill_payload_2, skill_payload_3):
    # Insert three skills with ranks 1, 2, 3
    client.post("/v1/skills/", json=skill_payload)
    client.post("/v1/skills/", json=skill_payload_2)
    client.post("/v1/skills/", json=skill_payload_3)

    # Insert a new skill at rank 2 — should push s2 and s3 down
    collision_payload = {
        "name": "Golang",
        "icon": "./icons/go.png",
        "category": SkillCategory.backend,
        "rank": 2
    }
    inserted = client.post("/v1/skills/", json=collision_payload).json()
    assert inserted["rank"] == 2

    # Fetch all backend skills and verify ranks
    response = client.get(f"/v1/skills/{SkillCategory.backend.value}")
    skills = response.json()
    ranks = {s["name"]: s["rank"] for s in skills}

    assert ranks["FastAPI"] == 1
    assert ranks["Golang"] == 2
    assert ranks["PostgreSQL"] == 3
    assert ranks["Docker"] == 4

def test_rank_shift_on_deletion(client):
    # Insert three skills
    s1 = client.post("/v1/skills/", json={
        "name": "React",
        "icon": "./icons/react.png",
        "category": SkillCategory.frontend,
        "rank": 1
    }).json()

    s2 = client.post("/v1/skills/", json={
        "name": "TailwindCSS",
        "icon": "./icons/tailwind.png",
        "category": SkillCategory.frontend,
        "rank": 2
    }).json()

    s3 = client.post("/v1/skills/", json={
        "name": "TanStack Query",
        "icon": "./icons/query.png",
        "category": SkillCategory.frontend,
        "rank": 3
    }).json()

    # Delete rank 2 (TailwindCSS)
    response = client.delete(f"/v1/skills/{s2['id']}")
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]

    # Fetch remaining frontend skills and verify ranks
    response = client.get(f"/v1/skills/{SkillCategory.frontend.value}")
    skills = response.json()
    ranks = {s["name"]: s["rank"] for s in skills}

    assert ranks["React"] == 1
    assert ranks["TanStack Query"] == 2  # shifted up from 3
