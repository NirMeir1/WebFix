from pydantic import BaseModel, HttpUrl, EmailStr, model_validator
from typing import Optional, ClassVar

class UrlRequest(BaseModel):
    url: HttpUrl
    report_type: str  # This will indicate "basic" or "deep"
    industry: str     # Industry field (dropdown list values)
    email: Optional[EmailStr] = None

    # Defining allowed values as class variables with ClassVar annotation
    allowed_report_types: ClassVar[list[str]] = ["basic", "deep"]
    allowed_industries: ClassVar[list[str]] = ["finance", "technology", "healthcare", "education"]  # Add more as needed

    @model_validator(mode="before")
    def validate_report_type_and_industry(cls, values):
        report_type = values.get('report_type')
        industry = values.get('industry')

        if report_type not in cls.allowed_report_types:
            raise ValueError(f"Invalid report_type '{report_type}'. Valid options are: {', '.join(cls.allowed_report_types)}")

        if industry not in cls.allowed_industries:
            raise ValueError(f"Invalid industry '{industry}'. Valid options are: {', '.join(cls.allowed_industries)}")

        return values


class UrlResponse(BaseModel):
    output: str
    message: str