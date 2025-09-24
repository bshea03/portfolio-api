import pytest

@pytest.fixture
def project_payload():
    return {
        "title": "Portfolio Platform",
        "description": "A full-stack platform for showcasing developer portfolios.",
        "image": "./images/projects/portfolio.png",
        "alt": "Screenshot of portfolio platform",
        "docs": "https://docs.example.com",
        "code": "https://github.com/brady/portfolio",
        "tech": ["FastAPI", "PostgreSQL", "React", "Docker"],
        "details": {
            "intro": "This project helps developers showcase their work.",
            "features": [
                {
                    "title": "Dynamic Resume",
                    "description": "Auto-generates resume from structured data."
                },
                {
                    "title": "Project Showcase",
                    "description": "Displays projects with rich media and tech stack."
                }
            ],
            "conclusion": "Used by over 100 developers to host personal sites."
        }
    }

@pytest.fixture
def created_project(client, project_payload):
    response = client.post("/api/projects/", json=project_payload)
    assert response.status_code == 201
    return response.json()

def test_create_project(client, project_payload):
    response = client.post("/api/projects/", json=project_payload)
    assert response.status_code == 201
    project = response.json()
    assert project["title"] == project_payload["title"]
    assert project["tech"] == project_payload["tech"]
    assert project["details"]["intro"] == project_payload["details"]["intro"]

def test_get_all_projects(client, created_project):
    response = client.get("/api/projects/")
    assert response.status_code == 200
    projects = response.json()
    assert isinstance(projects, list)
    assert any(p["id"] == created_project["id"] for p in projects)

def test_get_single_project(client, created_project):
    project_id = created_project["id"]
    response = client.get(f"/api/projects/{project_id}")
    assert response.status_code == 200
    project = response.json()
    assert project["title"] == created_project["title"]

def test_update_project(client, created_project):
    project_id = created_project["id"]
    update_payload = {
        "title": "Updated Portfolio Platform",
        "description": "Updated description for the platform."
    }
    response = client.patch(f"/api/projects/{project_id}", json=update_payload)
    assert response.status_code == 200
    updated = response.json()
    assert updated["title"] == "Updated Portfolio Platform"
    assert updated["description"] == "Updated description for the platform."

def test_delete_project(client, created_project):
    project_id = created_project["id"]
    response = client.delete(f"/api/projects/{project_id}")
    assert response.status_code == 204

    # Confirm deletion
    response = client.get(f"/api/projects/{project_id}")
    assert response.status_code == 404
