from fastapi import APIRouter
from app.routers.v1.skill import router as skill_router
from app.routers.v1.portfolio import router as portfolio_router
from app.routers.v1.job import router as job_router
from app.routers.v1.project import router as project_router
from app.routers.v1.award import router as award_router

api_router = APIRouter()
api_router.include_router(skill_router)
api_router.include_router(portfolio_router)
api_router.include_router(job_router)
api_router.include_router(project_router)
api_router.include_router(award_router)
