from fastapi import APIRouter
from app.api.v1.endpoints import packages

api_router = APIRouter()
api_router.include_router(packages.router, prefix="/packages", tags=["packages"])
