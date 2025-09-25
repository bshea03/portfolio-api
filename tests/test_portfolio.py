import pytest
from app.models.skill import SkillCategory

@pytest.fixture
def seed_portfolio_data(client):
    # Create job
    job_payload = {
        "company": "Dispatch Technologies",
        "icon": "./images/jobs/dispatch.png",
        "description": "Senior Software Engineer",
        "dates": "2021–2025",
        "details": [{"text": "Led frontend guild meetings"}],
        "skills": ["React", "TypeScript", "AWS"]
    }
    job = client.post("/v1/jobs/", json=job_payload).json()

    # Create project
    project_payload = {
        "title": "Portfolio Platform",
        "description": "Showcase site for developers",
        "image": "./images/projects/portfolio.png",
        "alt": "Portfolio screenshot",
        "docs": "https://docs.example.com",
        "code": "https://github.com/brady/portfolio",
        "tech": ["FastAPI", "Docker"],
        "details": {
            "intro": "Built for speed and clarity",
            "features": [{"title": "Resume Generator", "description": "Auto-generates resumes"}],
            "conclusion": "Used by 100+ devs"
        }
    }
    project = client.post("/v1/projects/", json=project_payload).json()

    # Create award
    award_payload = {
        "title": "Top Engineer",
        "description": "Recognized for backend excellence",
        "icon": "./images/awards/top-engineer.png",
        "date": "June 2025"
    }
    award = client.post("/v1/awards/", json=award_payload).json()

    # Create skills
    skill_payloads = [
        {"name": "FastAPI", "icon": "./icons/fastapi.png", "category": SkillCategory.backend, "rank": 1},
        {"name": "Docker", "icon": "./icons/docker.png", "category": SkillCategory.backend, "rank": 2},
        {"name": "React", "icon": "./icons/react.png", "category": SkillCategory.frontend, "rank": 1}
    ]
    skills = [client.post("/v1/skills/", json=payload).json() for payload in skill_payloads]

    return {
        "job": job,
        "project": project,
        "award": award,
        "skills": skills
    }

def test_get_portfolio(client, seed_portfolio_data):
    response = client.get("/v1/portfolio")
    assert response.status_code == 200

    data = response.json()
    assert "jobs" in data
    assert "projects" in data
    assert "awards" in data
    assert "skills" in data

    # Validate job structure
    job = data["jobs"][0]
    assert job["company"] == "Dispatch Technologies"
    assert "details" in job and isinstance(job["details"], list)

    # Validate project structure
    project = data["projects"][0]
    assert project["title"] == "Portfolio Platform"
    assert "details" in project and "features" in project["details"]

    # Validate award structure
    award = data["awards"][0]
    assert award["title"] == "Top Engineer"
    assert award["date"] == "June 2025"

    # Validate skills grouping
    assert "backend" in data["skills"]
    backend_skills = data["skills"]["backend"]
    assert any(s["name"] == "FastAPI" for s in backend_skills)
    assert any(s["name"] == "Docker" for s in backend_skills)
