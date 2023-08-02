import os
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from fastapi import UploadFile
from app.core.sql_models import Users, Profile, model_to_dict
from app.core.schemas import UserRegistration
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def format_user(user: Users):
    """
    Format a Users object to json for response

    :param user:
    :return: dict
    """
    user_dict = model_to_dict(user)
    user_dict["profile_picture"] = user.profile.profile_picture
    user_dict.pop("password")
    return user_dict


async def register_user(db: Session, user_data: UserRegistration):
    password = hash_password(user_data.password)
    # Create a new user in the database
    new_user = Users(full_name=user_data.full_name, email=user_data.email,
                     password=password, phone=user_data.phone)
    db.add(new_user)
    db.commit()

    # If a profile picture is uploaded, save it to the database
    if user_data.profile_picture:
        # Example: Save the profile picture to the user's profile_picture field
        file_path = save_profile_picture(user_data.profile_picture)
        new_profile = Profile(user_id=new_user.id, profile_picture=file_path)
        db.add(new_profile)
        # Save the changes to the database
        db.commit()
    return format_user(new_user)


def save_profile_picture(profile_picture: UploadFile) -> str:
    """
    Implementing the logic to save files onto the storage location
    :param profile_picture:
    :return:
    """

    # This example assumes you are saving the file in a local directory named "profile_pictures"
    directory = f"{settings.fs_mount_path}profile_pictures"
    file_path = f"{directory}/{profile_picture.filename}"
    os.makedirs(directory, exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(profile_picture.file.read())

    return file_path


def fetch_by_id(db: Session, user_id: int):
    user_object = db.query(Users).filter(user_id == Users.id).first()
    if not user_object:
        return None
    return format_user(user_object)


def hash_password(password: str):
    return pwd_context.hash(password)
