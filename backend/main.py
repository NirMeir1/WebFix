from fastapi import FastAPI, HTTPException
from schemas import UrlRequest, UrlResponse
from gpt_service import ChatGPTService
from cache import get_cached_response, save_response, is_recent_response
from dotenv import load_dotenv
from pydantic import HttpUrl

load_dotenv()

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend is running"}


@app.post("/analyze-url", response_model=UrlResponse)
async def analyze_url(request: UrlRequest):
    try:
        validated_url = HttpUrl.validate(request.url)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid URL")

    if is_recent_response(request.url):
        return UrlResponse(output=get_cached_response(request.url))

    gpt = ChatGPTService()
    output = await gpt.generate_response(request.url)
    save_response(request.url, output)
    return UrlResponse(output=output)