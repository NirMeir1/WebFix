import os
from pathlib import Path
from openai import AsyncOpenAI
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class ChatGPTService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"
        logger.info("ChatGPTService initialized with model %s", self.model)

    async def generate_response(self, url: str, report_type: str, email: Optional[str] = None) -> str:
        logger.info(f"Generating response for URL: {url}")

        # Select the appropriate template file based on report_type
        template_filename = "deep_prompt_template.txt" if report_type == "deep" else "prompt_template.txt"
        template_path = Path(__file__).parent / "prompts" / template_filename

        # Check if the template file exists
        if not template_path.exists():
            logger.error(f"Template file not found at {template_path}")
            raise FileNotFoundError(f"Template file not found at {template_path}")
        
        # Read the template file
        with open(template_path, "r", encoding="utf-8") as file:
            template = file.read()

        # Replace the placeholders in the template with the values
        system_prompt = template.replace("{url}", str(url))
                                # .replace("{report_type}", report_type) \
                                # .replace("{email}", str(email) if email else "")

        # Print the system prompt for validation
        print(f"Generated System Prompt: {system_prompt}")  # Print the full system prompt for validation

        try:
            response = await self.client.responses.create(
                model="gpt-4o-mini", # need to play with this to get the right model
                input=[
                    {
                    "role": "system",
                    "content": [
                        {
                        "type": "input_text",
                        "text": system_prompt
                        }
                    ]
                    }
                ],
                text={
                    "format": {
                    "type": "json_schema",
                    "name": "cro_site_audit",
                    "schema": {
                        "type": "object",
                        "required": [
                        "schema_version",
                        "site",
                        "generated_at",
                        "pages"
                        ],
                        "properties": {
                        "site": {
                            "type": "string"
                        },
                        "pages": {
                            "type": "object",
                            "required": [
                            "home",
                            "category",
                            "product",
                            "cart",
                            "checkout",
                            "footer"
                            ],
                            "properties": {
                            "cart": {
                                "$ref": "#/definitions/pageReport"
                            },
                            "home": {
                                "$ref": "#/definitions/pageReport"
                            },
                            "footer": {
                                "$ref": "#/definitions/pageReport"
                            },
                            "product": {
                                "$ref": "#/definitions/pageReport"
                            },
                            "category": {
                                "$ref": "#/definitions/pageReport"
                            },
                            "checkout": {
                                "$ref": "#/definitions/pageReport"
                            }
                            },
                            "additionalProperties": False
                        },
                        "generated_at": {
                            "type": "string"
                        },
                        "schema_version": {
                            "type": "string"
                        },
                        "overall_observations": {
                            "type": "string"
                        }
                        },
                        "definitions": {
                        "criterion": {
                            "type": "object",
                            "required": [
                            "criterion",
                            "finding",
                            "score"
                            ],
                            "properties": {
                            "score": {
                                "type": "integer"
                            },
                            "finding": {
                                "type": "string"
                            },
                            "criterion": {
                                "type": "string"
                            }
                            },
                            "additionalProperties": False
                        },
                        "pageReport": {
                            "type": "object",
                            "required": [
                            "desktop",
                            "mobile"
                            ],
                            "properties": {
                            "mobile": {
                                "$ref": "#/definitions/deviceReport"
                            },
                            "desktop": {
                                "$ref": "#/definitions/deviceReport"
                            }
                            },
                            "additionalProperties": False
                        },
                        "deviceReport": {
                            "type": "object",
                            "required": [
                            "criteria",
                            "average_score",
                            "label",
                            "recommendations"
                            ],
                            "properties": {
                            "label": {
                                "enum": [
                                "Excellent",
                                "Good",
                                "Can Be Improved",
                                "Bad"
                                ],
                                "type": "string"
                            },
                            "criteria": {
                                "type": "array",
                                "items": {
                                "$ref": "#/definitions/criterion"
                                }
                            },
                            "average_score": {
                                "type": "number"
                            },
                            "recommendations": {
                                "type": "array",
                                "items": {
                                "type": "string"
                                }
                            }
                            },
                            "additionalProperties": False
                        }
                        },
                        "additionalProperties": False
                    },
                    "strict": False
                    }
                },
                reasoning={},
                tools=[
                    {
                    "type": "web_search",
                    "user_location": {
                        "type": "approximate"
                    },
                    "search_context_size": "medium"
                    }
                ],
                tool_choice="none",
                temperature=0.1,
                max_output_tokens=2508,
                top_p=1,
                store=True
                )

            logger.info(f"Response generated for URL: {url}")

            # Safely extract the assistant’s reply (assumes the assistant message is the last one)
            try:
                assistant_section = response.output[-1]
                # make sure there *is* at least one content entry
                if not assistant_section.content:
                    raise ValueError(f"No content in assistant_section: {assistant_section!r}")
                assistant_reply = assistant_section.content[0].text.strip()
            except (IndexError, AttributeError) as e:
                logger.error("Failed to parse assistant reply, response.output=%r: %s", response.output, e)
                raise

            logger.info(f"Assistant Reply:\n{assistant_reply}")

            return assistant_reply

        except Exception as e:
            logger.error(f"Error generating response for URL: {url}, Error: {str(e)}")
            raise
    
    async def generate_gpt_report(self, url: str, report_type: str, email: Optional[str] = None) -> str:
        """
        Helper function to generate a GPT response using the ChatGPTService.
        """
        output = await self.generate_response(url, report_type, email)
        return output