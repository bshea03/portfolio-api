from fastapi import APIRouter, Response, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.database import get_db
from app.utils.security import verify_api_key
from app.utils.limiting import limiter
from fastapi import Request

router = APIRouter(prefix="/v1/projects", tags=["Projects v1"])

@router.get("/", response_model=list[ProjectRead])
@limiter.limit("10/minute")
def get_projects(request: Request, db: Session = Depends(get_db)):
    return db.query(Project).all()

@router.get("/{projectId}", response_model=ProjectRead)
@limiter.limit("10/minute")
def get_project(request: Request, projectId: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == projectId).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No project with id {projectId} found"
        )
    return project

@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_api_key)])
@limiter.limit("10/minute")
def create_project(request: Request, payload: ProjectCreate, db: Session = Depends(get_db)):
    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.patch("/{projectId}", response_model=ProjectRead, dependencies=[Depends(verify_api_key)])
@limiter.limit("10/minute")
def update_project(request: Request, projectId: int, payload: ProjectUpdate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == projectId).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No project with id {projectId} found"
        )

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)
    return project

@router.delete("/{projectId}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_api_key)])
@limiter.limit("10/minute")
def delete_project(request: Request, projectId: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == projectId).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No project with id {projectId} found"
        )

    db.delete(project)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
