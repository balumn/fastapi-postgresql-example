from pydantic import BaseModel
import re

REGX_EMAIL = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


class CommonResponse(BaseModel):
    status: str = "failure"
    message: str = "API failed"
    data: str = []

    class Config:
        json_schema_extra = {
            "example": {"status": "failure", "message": "API failed", "data": None}
        }


def validate_email(cls, v):
    if not re.match(REGX_EMAIL, v) and 7 < len(v) < 320:
        raise ValueError("Invalid Email!")
    return v