from pydantic import BaseModel


class CommonResponse(BaseModel):
    status: str = "failure"
    message: str = "API failed"
    data: str = []

    class Config:
        json_schema_extra = {
            "example": {"status": "failure", "message": "API failed", "data": None}
        }
