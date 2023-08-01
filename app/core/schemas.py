from fastapi import UploadFile, Form
from pydantic import BaseModel, field_validator

from app.v1.validators import validate_email, validate_password, validate_phone


class UserRegistration(BaseModel):
    full_name: str
    email: str
    password: str
    phone: str
    profile_picture: UploadFile = Form(...)

    email_validation = field_validator("email", check_fields=False)(
        validate_email
    )

    password_validation = field_validator("password", check_fields=False)(
        validate_password
    )

    phone_validation = field_validator("phone", check_fields=False)(
        validate_phone
    )
