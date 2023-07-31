from fastapi import UploadFile, Form
from pydantic import BaseModel


class UserRegistration(BaseModel):
    full_name: str
    email: str
    password: str
    phone: str
    profile_picture: UploadFile = Form(...)
