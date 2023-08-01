import re

from fastapi import HTTPException

# REGEX EXPRESSIONS
REGX_EMAIL = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
REGEX_USER_PASSWORD = "^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)(?=.*?[\W_]).{8,}$"
REGEX_PHONE = r"^([+]?\d{2}?)?\d{9,13}$"

"""
normally we should raise a ValueError in validators
But for some reason ValueError won't be catched by FastAPI inside a Depends()
Depends() is necessary here since we should use a Form() (multipart/form-data), because we have a file upload
Body and Form cannot be used together: HTTP Limitation
"""


def is_valid_email(email):
    return re.match(REGX_EMAIL, email) and 7 < len(email) < 320


def validate_email(cls, v):
    if not is_valid_email(v):
        raise HTTPException(status_code=422, detail="Email is not valid")
    return v


def is_valid_user_password(password):
    return re.match(REGEX_USER_PASSWORD, password)


def validate_password(cls, v):
    if not is_valid_user_password(v):
        raise HTTPException(status_code=422,
                            detail="Invalid password. Min of 8 chars, 1 upper, 1 lower, 1 number and 1 special char.")
    return v


def is_valid_phone(phone):
    return re.match(REGEX_PHONE, phone)


def validate_phone(cls, v):
    if not is_valid_phone(v):
        raise HTTPException(status_code=422, detail="Invalid phone number")
    return v
