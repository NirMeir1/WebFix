import re

def is_valid_url(url: str) -> bool:
    pattern = re.compile(
        r"^(https?://)?(www\.)?([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}(/[\w\-._~:/?#[\]@!$&'()*+,;=]*)?$"
    )
    return bool(pattern.match(url))