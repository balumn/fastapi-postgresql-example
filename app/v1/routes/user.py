from fastapi import APIRouter, Depends
from app.core.schemas import UserRegistration

router = APIRouter()


@router.post("/register/")
def register_user(user_data: UserRegistration = Depends()):

    return {"message": "User registration successful"}
