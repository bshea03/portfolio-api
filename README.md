# 📘 `api.bradyshea.dev` — Portfolio API

A lightweight REST API built with FastAPI, PostgreSQL, and Docker to power [bradyshea.dev](https://bradyshea.dev). It serves portfolio information to the frontend and allows secure admin access for dynamic data management.

This API was implemented as a way to learn FastAPI, Docker, and modern backend best practices, while simultaneously gaining experience deploying a production-ready service.

---

## 🔐 Authentication & Rate Limiting

- Protected routes (`POST`, `PATCH`, `DELETE`) require an `x-api-key` header.
- Rate limiting is enforced via [SlowAPI](https://github.com/laurentS/slowapi): `10 requests/minute` per IP.

---

## 🧭 Endpoints

### 📂 `/v1/portfolio`

Returns the full portfolio payload used by the frontend.

```http
GET /v1/portfolio
```

- Returns: { jobs, projects, awards, skills }
- Skills are grouped by category and sorted by rank.

---

### 🏆 `v1/awards`
http```
GET    /v1/awards               # List all awards  
GET    /v1/awards/{id}          # Get award by ID  
POST   /v1/awards               # Create new award (auth required)  
PATCH  /v1/awards/{id}          # Update award (auth required)  
DELETE /v1/awards/{id}          # Delete award (auth required)
```

---

###  💼 `/v1/jobs`
http```
GET    /v1/job                  # List all jobs  
GET    /v1/job/{id}             # Get job by ID  
POST   /v1/job                  # Create new job (auth required)  
PATCH  /v1/job/{id}             # Update job (auth required)  
DELETE /v1/job/{id}             # Delete job (auth required)
```

---

### 🧪 `/v1/projects`
http```
GET    /v1/projects             # List all projects  
GET    /v1/projects/{id}        # Get project by ID  
POST   /v1/projects             # Create new project (auth required)  
PATCH  /v1/projects/{id}        # Update project (auth required)  
DELETE /v1/projects/{id}        # Delete project (auth required)
```

---

### 🧠 `/v1/skills`
http```
GET    /v1/skills               # Get all skills grouped by category  
GET    /v1/skills/{category}    # Get skills by category  
POST   /v1/skills               # Create new skill (auth required)  
PATCH  /v1/skills/{id}          # Update skill (auth required)  
DELETE /v1/skills/{id}          # Delete skill (auth required)  
POST   /v1/skills/normalize     # Normalize skill ranks (auth required)  
```

- Skill creation supports automatic or manual rank assignment.
- Rank normalization ensures sequential ordering with no gaps or duplicates.

---

## 🛠️ Tech Stack
- FastAPI + Pydantic for routing and schema validation
- PostgreSQL + SQLAlchemy for data persistence
- Alembic for versioned migrations
- Docker for containerized deployment
- Nginx + Certbot for HTTPS and reverse proxy
- GitHub Actions for CI/CD

---

## 🚀 Deployment
- Hosted on DigitalOcean via Docker
- Reverse proxy configured with Nginx
- SSL certificates managed with Certbot
- CI/CD pipeline automates build, test, and deploy