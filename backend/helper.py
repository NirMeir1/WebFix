from pydantic import HttpUrl

def normalize_url(url: HttpUrl) -> str:
    return str(url).strip().lower()