from pydantic import BaseModel, HttpUrl, EmailStr, model_validator
from typing import Optional, ClassVar, Literal
from email_validator import validate_email, EmailNotValidError

class UrlRequest(BaseModel):
    url: HttpUrl
    report_type: Literal["basic", "deep"]  # Restricting to specific values using Literal
    email: Optional[EmailStr] = None

    allowed_report_types: ClassVar[list[str]] = ["basic", "deep"]

    # Using @model_validator for overall validation at the model level
    @model_validator(mode="before")
    def validate_fields(cls, values):
        report_type = values.get('report_type')

        # Validate report_type
        if report_type not in cls.allowed_report_types:
            raise ValueError(f"Invalid report_type '{report_type}'. Valid options are: {', '.join(cls.allowed_report_types)}")

        # Email validation if provided
        email = values.get('email')
        if email:
            try:
                # Validate the email format using email-validator library
                validate_email(email)

            except EmailNotValidError as e:
                raise ValueError(f"Invalid email: {e}")

        # Uncomment the following lines if you want to enforce email for deep report
        
         # ✅ Enforce required email for deep report
        # if report_type == 'deep' and not email:
        #     raise ValueError("Email is required for a deep report.")
        
        return values

class UrlResponse(BaseModel):
    output: str
    screenshot_base64: Optional[str] = None
    is_cached: bool