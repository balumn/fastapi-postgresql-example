import os

from fastapi import HTTPException, UploadFile
from app.core.sql_models import Users, Profile, model_to_dict
from app.core.schemas import UserRegistration
from app.config import settings


async def register_user(db, user_data: UserRegistration):
    new_user = None
    # Create a new user in the database
    new_user = Users(full_name=user_data.full_name, email=user_data.email,
                     password=user_data.password, phone=user_data.phone)
    db.add(new_user)
    db.commit()

    # If a profile picture is uploaded, save it to the database
    if user_data.profile_picture:
        # Example: Save the profile picture to the user's profile_picture field
        file_path = save_profile_picture(user_data.profile_picture)
        new_profile = Profile(user_id=new_user.id, profile_picture=file_path)
        db.add(new_profile)
        db.commit()
        # Save the changes to the database
        db.commit()
    user_dict = model_to_dict(new_user)
    user_dict["profile_picture"] = new_user.profile.profile_picture
    return user_dict


def save_profile_picture(profile_picture: UploadFile) -> str:
    # Here, you can implement the logic to save the profile picture
    # For example, save the file to a file system or cloud storage and return the file path or URL
    # Make sure to handle file names, extensions, and security considerations

    # This example assumes you are saving the file in a local directory named "profile_pictures"
    directory = f"{settings.fs_mount_path}profile_pictures"
    file_path = f"{directory}/{profile_picture.filename}"
    os.makedirs(directory, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(profile_picture.file.read())

    return file_path
