import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from app.core.database.db_util import get_db
from app.core.schemas import UserRegistration
from app.core.sql_models import Users
from app.v1.services.user import register_user as register_user_service, fetch_by_id as fetch_user_by_id
from app.v1.utils import CommonResponse

router = APIRouter()


@router.post("/register/", status_code=500)
async def register_user(
        user_data: UserRegistration = Depends(),
        db: Session = Depends(get_db),
        response_status: Response = None,
):
    response = CommonResponse()
    response.status = "failure"
    response.data = None

    # Checking if the email or phone already exist in the database
    if db.query(Users).filter(Users.email == user_data.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    if db.query(Users).filter(Users.phone == user_data.phone).first():
        raise HTTPException(status_code=409, detail="Phone number already registered")

    # @TODO: Check if the file name exists in the storage (or else it will overwrite)

    try:
        response.data = await register_user_service(db, user_data)
        response.status = "User created successfully"
    except Exception as e:
        db.rollback()
        logging.error(e, exc_info=True)
        response.message = str(e)
    finally:
        db.close()
    response_status.status_code = status.HTTP_201_CREATED
    return response


@router.get("/user/id/{user_id}", status_code=500)
async def get_user(
        user_id: int,
        response_status: Response = None,
        db: Session = Depends(get_db),
):
    """
    Get the User given by id
    """
    response = CommonResponse()
    response.status = "failure"
    response.data = None

    try:
        db_user = fetch_user_by_id(db, user_id)
        if db_user:
            response.data = db_user
            response.status = "success"
            response.message = f"Successfully fetched the user {user_id}"
            response_status.status_code = status.HTTP_200_OK
        else:
            response_status.status_code = status.HTTP_404_NOT_FOUND
            response.message = "User not found for the given user id!"

    except Exception as e:
        logging.error(e, exc_info=True)
        return str(e)

    return response
