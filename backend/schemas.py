from pydantic import BaseModel

class UrlRequest(BaseModel):
    url: str

class UrlResponse(BaseModel):
    output: str