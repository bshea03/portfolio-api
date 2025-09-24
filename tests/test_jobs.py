import pytest

@pytest.fixture
def job_payload():
    return {
        "company": "Dispatch Technologies",
        "icon": "./images/jobs/dispatch.png",
        "description": "Senior Software Engineer • Software Engineer",
        "dates": "December 2021 - August 2025 (Full-time)",
        "details": [
            {
                "text": "<strong>Organized and led frontend guild meetings</strong> to educate engineers and facilitate in-depth discussions on frontend topics within the context of our apps."
            },
            {
                "text": "<strong>Directed the transition of our frontend</strong> from Travis CI to GitHub Actions and from Cypress end-to-end tests to Playwright, cutting our CI/CD build time by nearly 75% and enabling more reliable test coverage."
            },
            {
                "text": "<strong>Integrated Cursor AI into the development workflow</strong>, significantly accelerating development and reducing turnaround time for story completion by ~30%."
            },
            {
                "text": "<strong>Led a 5-engineer team across multiple sprints</strong>, coordinating story assignment, writing build plans, and maintaining continuous communication with Product to align deliverables with business goals.",
                "children": [
                    {
                        "text": "<strong>Mentored and managed associate engineers</strong>, providing technical guidance and career development support."
                    }
                ]
            }
        ],
        "skills": [
            "TypeScript", "React", "Redux", "React Native", "CSS", "TailwindCSS",
            "TanStack Query", "Ruby on Rails", "PostgreSQL", "Golang", "Node.js",
            "AWS", "Jest", "React Testing Library", "Cypress", "Playwright",
            "Webpack", "Github Actions", "CI/CD", "Cursor AI"
        ]
    }

@pytest.fixture
def created_job(client, job_payload):
    response = client.post("/api/jobs/", json=job_payload)
    assert response.status_code == 201
    return response.json()

def assert_list_items_equal(expected, actual):
    assert expected["text"] == actual["text"]
    if "children" in expected:
        assert "children" in actual
        assert len(expected["children"]) == len(actual["children"])
        for e_child, a_child in zip(expected["children"], actual["children"]):
            assert_list_items_equal(e_child, a_child)
    else:
        assert "children" not in actual or actual["children"] is None

def test_get_all_jobs(client, job_payload, created_job):
    response = client.get("/api/jobs/")
    assert response.status_code == 200
    jobs = response.json()
    assert any(job["company"] == job_payload["company"] for job in jobs)

def test_get_single_job(client, created_job):
    job_id = created_job["id"]
    response = client.get(f"/api/jobs/{job_id}")
    assert response.status_code == 200
    assert response.json()["company"] == created_job["company"]

def test_update_job(client, created_job):
    job_id = created_job["id"]
    update_payload = {
        "company": "Dispatch AI",
        "description": "Updated description"
    }
    response = client.patch(f"/api/jobs/{job_id}", json=update_payload)
    assert response.status_code == 200
    job = response.json()
    assert job["company"] == "Dispatch AI"
    assert job["description"] == "Updated description"

def test_delete_job(client, created_job):
    job_id = created_job["id"]
    response = client.delete(f"/api/jobs/{job_id}")
    assert response.status_code == 204

    # Confirm deletion
    response = client.get(f"/api/jobs/{job_id}")
    assert response.status_code == 404
