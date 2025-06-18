from copy import deepcopy
import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

from openai import AsyncOpenAI
from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)

# ─── Configuration ─────────────────────────────────────────────────────────────

MODEL          = "gpt-4o"
MAX_TOKENS     = 25000
TEMPERATURE    = 0.1
TOP_P          = 1.0
STORE          = True

BASE_DIR     = Path(__file__).parent
TEMPLATE_DIR = BASE_DIR / "prompts"
SCHEMA_PATH  = BASE_DIR / "schemas" / "cro_site_audit.schema.json"

# Load your JSON Schema exactly once
try:
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        CRO_SCHEMA = json.load(f)
except FileNotFoundError:
    logger.error("CRO schema file not found at %s", SCHEMA_PATH)
    raise

class ChatGPTError(Exception):
    """Raised when something goes wrong in ChatGPTService."""
    pass

# ─── Service Class ──────────────────────────────────────────────────────────────

class ChatGPTService:
    def __init__(
        self,
        client: Optional[AsyncOpenAI] = None,
        api_key: Optional[str] = None,
        model: str = MODEL,
    ):
        self.client = client or AsyncOpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model
        logger.info("ChatGPTService initialized with model %s", self.model)

    async def _load_template(self, report_type: str) -> str:
        filename = "deep_prompt_template.txt" if report_type == "deep" else "prompt_template.txt"
        path = TEMPLATE_DIR / filename
        logger.info(f"⚙️ Loading prompt template: {filename}")
        if not path.exists():
            logger.error("Template file not found at %s", path)
            raise ChatGPTError(f"Missing prompt template: {path}")
        return path.read_text(encoding="utf-8")

    def _build_system_prompt(
        self,
        template: str,
        url: str,
        report_type: str,
        email: Optional[str],
    ) -> str:
        prompt = template.replace("{url}", url)\
            .replace("{report_type}", report_type) 
        # extend here if you need {report_type} or {email} placeholders
        return prompt

    def _build_payload(self, system_prompt: str, report_type: str) -> Dict[str, Any]:
        schema = deepcopy(CRO_SCHEMA)
        pages_schema = schema["properties"]["pages"]
        props = pages_schema["properties"]

        base_keys = ["home","category","product","cart","checkout","footer"]
        deep_keys = ["general","navigation","search","cart_widget"]

        if report_type == "basic":
            # Remove deep‐only properties entirely
            for key in deep_keys:
                props.pop(key, None)
            pages_schema["required"] = base_keys
        else:
            # Keep all properties, require all of them
            pages_schema["required"] = base_keys + deep_keys

        return {
            "model": self.model,
            "input": [
                {
                    "role": "system",
                    "content": [{"type": "input_text", "text": system_prompt}],
                }
            ],
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "cro_site_audit",
                    "schema": schema,
                    "strict": False,
                }
            },
            "reasoning": {},
            "tools": [
                {
                    "type": "web_search",
                    "user_location": {"type": "approximate"},
                    "search_context_size": "medium",
                }
            ],
            "tool_choice": "none",
            "temperature": TEMPERATURE,
            "max_output_tokens": MAX_TOKENS,
            "top_p": TOP_P,
            "store": STORE,
        }

    async def _call_openai(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        logger.debug("Calling OpenAI with payload: %s", payload)
        try:
            return await self.client.responses.create(**payload)
        except Exception as e:
            logger.error("OpenAI API call failed: %s", e)
            raise ChatGPTError(f"OpenAI API error: {e}")

    def _parse_and_validate(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        try:
            message = raw.output[-1]
            if not message.content:
                raise ChatGPTError("Assistant returned no content")
            text = message.content[0].text.strip()
            logger.debug("⚙️ Raw assistant text:\n" + message.content[0].text)
            data = json.loads(text)
        except (IndexError, AttributeError, json.JSONDecodeError) as e:
            logger.error("Parsing assistant response failed: %s", e)
            raise ChatGPTError(f"Failed to parse response: {e}")

        try:
            validate(instance=data, schema=CRO_SCHEMA)
        except ValidationError as e:
            logger.error("Schema validation error: %s", e)
            raise ChatGPTError(f"Response did not match schema: {e.message}")

        return data

    async def generate_response(
        self,
        url: str,
        report_type: str,
        email: Optional[str] = None,
    ) -> Dict[str, Any]:
        logger.info("Generating CRO report for URL: %s", url)
        template      = await self._load_template(report_type)
        system_prompt = self._build_system_prompt(template, url, report_type, email)
        payload       = self._build_payload(system_prompt, report_type)
        raw           = await self._call_openai(payload)
        return self._parse_and_validate(raw)

    async def generate_gpt_report(
        self,
        url: str,
        report_type: str,
        email: Optional[str] = None,
    ) -> str:
        data = await self.generate_response(url, report_type, email)
        # Return as compact JSON string
        return json.dumps(data, ensure_ascii=False)
