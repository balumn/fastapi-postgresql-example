import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from app.core.sql_models import Users
from app.v1.services.user import register_user as register_user_service
from app.core.database.db_util import get_db
from app.core.schemas import UserRegistration

router = APIRouter()


@router.post("/register/", status_code=500)
async def register_user(
        user_data: UserRegistration = Depends(),
        db: Session = Depends(get_db),
        response_status: Response = None,
):
    # Check if the email or phone already exist in the database
    if db.query(Users).filter(Users.email == user_data.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    if db.query(Users).filter(Users.phone == user_data.phone).first():
        raise HTTPException(status_code=409, detail="Phone number already registered")

    try:
        result = await register_user_service(db, user_data)
    except Exception as e:
        db.rollback()
        logging.error(e, exc_info=True)
        return str(e)
    finally:
        db.close()
    response_status.status_code = status.HTTP_201_CREATED
    return {
        "status": "Created",
        "data": result
    }
