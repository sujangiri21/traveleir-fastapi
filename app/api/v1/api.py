from fastapi import APIRouter
from app.api.v1.endpoints import packages, passport, stats

api_router = APIRouter()
api_router.include_router(packages.router, prefix="/packages", tags=["packages"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])
api_router.include_router(passport.router, prefix="/passport", tags=["passport"])

