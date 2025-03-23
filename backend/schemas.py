from pydantic import BaseModel, HttpUrl
import logging

logger = logging.getLogger(__name__)

class UrlRequest(BaseModel):
    url: HttpUrl

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Log when a new UrlRequest instance is created
        logger.info(f"UrlRequest created with URL: {self.url}")

class UrlResponse(BaseModel):
    output: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Log when a new UrlResponse instance is created
        logger.info(f"UrlResponse created with output: {self.output[:100]}...")
