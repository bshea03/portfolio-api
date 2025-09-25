from sqlalchemy.orm import Session
from fastapi import APIRouter, Response, status, HTTPException, Depends
from app.database import get_db
from app.models.award import Award
from app.schemas.award import AwardCreate, AwardRead, AwardUpdate
from app.utils.security import verify_api_key
from app.utils.limiting import limiter
from fastapi import Request

router = APIRouter(prefix="/v1/awards", tags=["Awards v1"])

@router.get('/', response_model=list[AwardRead])
@limiter.limit("10/minute")
def get_awards(request: Request, db: Session = Depends(get_db)):
    return db.query(Award).all()

@router.get('/{awardId}', response_model=AwardRead)
@limiter.limit("10/minute")
def get_award(request: Request, awardId: int, db: Session = Depends(get_db)):
    award = db.query(Award).filter(Award.id == awardId).first()
    if not award:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No award with id {awardId} found'
        )
    return award

@router.post('/', response_model=AwardRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_api_key)])
@limiter.limit("10/minute")
def create_award(request: Request, payload: AwardCreate, db: Session = Depends(get_db)):
    award = Award(**payload.model_dump())
    db.add(award)
    db.commit()
    db.refresh(award)
    return award

@router.patch('/{awardId}', response_model=AwardRead, dependencies=[Depends(verify_api_key)])
@limiter.limit("10/minute")
def update_award(request: Request, awardId: int, payload: AwardUpdate, db: Session = Depends(get_db)):
    award = db.query(Award).filter(Award.id == awardId).first()
    if not award:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No award with id {awardId} found'
        )

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(award, key, value)

    db.commit()
    db.refresh(award)
    return award

@router.delete('/{awardId}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_api_key)])
@limiter.limit("10/minute")
def delete_award(request: Request, awardId: int, db: Session = Depends(get_db)):
    award = db.query(Award).filter(Award.id == awardId).first()
    if not award:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No award with id {awardId} found'
        )

    db.delete(award)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
