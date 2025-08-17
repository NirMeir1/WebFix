from pydantic import HttpUrl
from user_agents import parse

def normalize_url(url: HttpUrl) -> str:
    return str(url).strip().lower()

def is_mobile(user_agent_str: str) -> bool:
    user_agent = parse(user_agent_str)
    return user_agent.is_mobile or user_agent.is_tablet
