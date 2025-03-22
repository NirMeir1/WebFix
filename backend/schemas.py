from pydantic import BaseModel, HttpUrl

class UrlRequest(BaseModel):
    url: HttpUrl

class UrlResponse(BaseModel):
    output: str