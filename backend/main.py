from fastapi import FastAPI
from backend.schemas import UrlRequest, UrlResponse
from backend.gpt_service import ChatGPTService
from backend.cache import (
    get_cached_response,
    save_response,
    is_recent_response,
    initialize_cache
)
from dotenv import load_dotenv
from logging_config import setup_logging
import logging

# Set up logging once at the start of your application
setup_logging()

# Create a logger for this module
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Backend is running"}


@app.post("/analyze-url", response_model=UrlResponse)
async def analyze_url(request: UrlRequest):
    
    logger.info(f"Initialize cache when the POST request is made")
    initialize_cache() 

    logger.info(f"Analyzing URL: {request.url}")
    
    # Check if the response is cached
    if is_recent_response(request.url):
        logger.info(f"Returning cached response for URL: {request.url}")
        return UrlResponse(output=get_cached_response(request.url))
    
    # If not cached, process the URL using ChatGPT
    try:
        gpt = ChatGPTService()
        logger.info(f"Generating response for URL: {request.url}")
        output = await gpt.generate_response(request.url)
        
        # Save the new response
        save_response(request.url, output)
        logger.info(f"Response generated and saved for URL: {request.url}")
        
        return UrlResponse(output=output)
    except Exception as e:
        logger.error(f"Error generating response for URL: {request.url}, Error: {str(e)}")
        return {"error": "An error occurred while processing the request. Please try again later."}