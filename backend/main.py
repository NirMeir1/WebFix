from fastapi import FastAPI, HTTPException
from schemas import UrlRequest, UrlResponse
from gpt_service import ChatGPTService
from cache import get_cached_response, save_response, is_recent_response
from utils import is_valid_url
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend is running"}


@app.post("/analyze-url", response_model=UrlResponse)
async def analyze_url(request: UrlRequest):
    if not is_valid_url(request.url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    if is_recent_response(request.url):
        return UrlResponse(output=get_cached_response(request.url))

    gpt = ChatGPTService()
    output = await gpt.generate_response(request.url)
    save_response(request.url, output)
    return UrlResponse(output=output)