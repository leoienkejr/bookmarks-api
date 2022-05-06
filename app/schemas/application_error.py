from pydantic import BaseModel


class ApplicationErrorResponse(BaseModel):
    error_code: int
    error_str: str
    http_status: int
    message: str
