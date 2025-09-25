from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.job import Job
from app.models.project import Project
from app.models.award import Award
from app.models.skill import Skill
from app.schemas.job import JobRead
from app.schemas.project import ProjectRead
from app.schemas.award import AwardRead
from app.schemas.skill import SkillRead, SkillCategory
from app.utils.limiting import limiter
from fastapi import Request

router = APIRouter(prefix="/v1/portfolio", tags=["Portfolio v1"])

@router.get("/", response_model=dict)
@limiter.limit("10/minute")
def get_portfolio(request: Request, db: Session = Depends(get_db)):
    jobs = db.query(Job).order_by(Job.created_at.desc()).all()
    projects = db.query(Project).order_by(Project.created_at.desc()).all()
    awards = db.query(Award).order_by(Award.date.desc()).all()
    skills = db.query(Skill).order_by(Skill.category, Skill.rank).all()

    grouped_skills = {}
    for skill in skills:
        grouped_skills.setdefault(skill.category, []).append({
            "name": skill.name,
            "icon": skill.icon,
            "rank": skill.rank
        })

    return {
        "jobs": [JobRead.model_validate(j).model_dump() for j in jobs],
        "projects": [ProjectRead.model_validate(p).model_dump() for p in projects],
        "awards": [AwardRead.model_validate(a).model_dump() for a in awards],
        "skills": grouped_skills
    }
