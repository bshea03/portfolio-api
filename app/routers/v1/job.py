from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from app.utils.security import verify_api_key
from app.models.job import Job
from app.schemas.job import JobCreate, JobRead, JobUpdate
from app.database import get_db
from app.utils.limiting import limiter
from fastapi import Request

router = APIRouter(prefix="/v1/jobs", tags=["Jobs v1"])

@router.get('', response_model=list[JobRead])
@limiter.limit("10/minute")
def jobs(request: Request, db: Session = Depends(get_db)):
    return db.query(Job).all()

@router.post('', response_model=JobRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_api_key)])
@limiter.limit("10/minute")
def create_job(request: Request, payload: JobCreate, db: Session = Depends(get_db)):
    job = Job(**payload.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

@router.patch('/{jobId}', response_model=JobRead, dependencies=[Depends(verify_api_key)])
@limiter.limit("10/minute")
def update_job(request: Request, jobId: int, payload: JobUpdate, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == jobId).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No job with id {jobId} found')

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(job, key, value)

    db.commit()
    db.refresh(job)
    return job

@router.get('/{jobId}', response_model=JobRead)
@limiter.limit("10/minute")
def get_job(request: Request, jobId: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == jobId).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No job with id {jobId} found')
    return job

@router.delete('/{jobId}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_api_key)])
@limiter.limit("10/minute")
def delete_job(request: Request, jobId: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == jobId).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No job with id {jobId} found')
    db.delete(job)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
