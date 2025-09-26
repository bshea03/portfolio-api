from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.database import Base, SessionLocal, engine
from app.routers.router import api_router
from app.utils.skill_ranks import normalize_ranks

log = logging.getLogger("uvicorn")
limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup...")
    db = SessionLocal()
    try:
        normalize_ranks(db)  # normalize everything at startup
    finally:
        db.close()
    
    yield 

    print("Application shutdown...")

app = FastAPI(
  title="Brady's Backend API",
  description="Unified API for jobs, projects, and more",
  version="1.0.0",
  lifespan=lifespan
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# CORS setup — allow frontend access
origins = [
    "http://localhost:3000", 
    "https://bshea03.github.io/",
    "https://bradyshea.dev/" # your frontend dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# Health check endpoint
@app.get("/healthchecker")
def health_check():
    return {"message": "FastAPI backend is running"}