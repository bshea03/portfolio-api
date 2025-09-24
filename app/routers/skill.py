from collections import defaultdict
from typing import Optional
from fastapi import APIRouter, Query, Response, status, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.skill import Skill, SkillCategory
from app.schemas.skill import SkillCreate, SkillRead, SkillReorder, SkillUpdate
from app.database import get_db
from app.utils.security import verify_api_key
from app.utils.skill_ranks import apply_rank_update, normalize_ranks, shift_ranks_for_insert
from app.utils.limiting import limiter
from fastapi import Request

router = APIRouter()

@router.get("/", response_model=dict)
@limiter.limit("10/minute")
def get_all_skills(
    request: Request, 
    category: Optional[SkillCategory] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    skills = db.query(Skill).order_by(Skill.category, Skill.rank).all()

    grouped = defaultdict(list)
    for skill in skills:
        grouped[skill.category].append({
            "name": skill.name,
            "icon": skill.icon,
            "rank": skill.rank
        })

    return dict(grouped)

@router.get("/{category}", response_model=list[SkillRead])
@limiter.limit("10/minute")
def get_skills_by_category(request: Request, category: SkillCategory, db: Session = Depends(get_db)):
    skills = db.query(Skill).filter(Skill.category == category).order_by(Skill.rank).all()

    if not skills:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No {category} skills found"
        )

    return skills

@router.post("/", response_model=SkillRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_api_key)])
@limiter.limit("10/minute")
def create_skill(request: Request, payload: SkillCreate, db: Session = Depends(get_db)):
    if payload.rank is not None:
        shift_ranks_for_insert(None, payload.category, payload.rank, db)
        skill = Skill(**payload.model_dump())
    else:
        max_rank = (
            db.query(func.max(Skill.rank))
            .filter(Skill.category == payload.category)
            .scalar()
            or 0
        )
        skill = Skill(
            name=payload.name,
            icon=payload.icon,
            category=payload.category,
            rank=max_rank + 1
        )

    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill

@router.post("/normalize", response_model=dict, dependencies=[Depends(verify_api_key)])
@limiter.limit("10/minute")
def normalize_skills(request: Request, category: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Normalize skill ranks so they are sequential with no gaps/duplicates.
    Optionally provide ?category=frontend (or backend, etc.) to limit scope.
    """
    normalize_ranks(db, category=category)
    return {
        "message": f"Ranks normalized{' for ' + category if category else ' for all categories'}"
    }

@router.patch("/{skill_id}", response_model=SkillRead, dependencies=[Depends(verify_api_key)])
@limiter.limit("10/minute")
def update_skill(request: Request, skill_id: int, payload: SkillUpdate, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    update_data = payload.model_dump(exclude_unset=True)

    if "rank" in update_data and update_data["rank"] != skill.rank:
        new_rank = update_data["rank"]
        category = update_data.get("category", skill.category)
        apply_rank_update(skill, new_rank, category, db)

    for field, value in update_data.items():
        if field not in {"rank", "category"}:
            setattr(skill, field, value)

    db.commit()
    db.refresh(skill)
    return skill

@router.delete("/{skill_id}", response_model=dict, dependencies=[Depends(verify_api_key)])
@limiter.limit("10/minute")
def delete_skill(request: Request, skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    category = skill.category
    deleted_rank = skill.rank

    db.delete(skill)

    db.query(Skill).filter(
        Skill.category == category,
        Skill.rank > deleted_rank
    ).update({Skill.rank: Skill.rank - 1}, synchronize_session="fetch")

    db.commit()
    return {"message": f"Skill {skill.name} deleted and ranks shifted in {category}"}
