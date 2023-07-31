from fastapi import APIRouter
from app.v1.routes.user import router as user_router

api_router = APIRouter()
api_router.include_router(user_router, tags=["User Module APIs"])
