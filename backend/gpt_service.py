import os
from pathlib import Path
from openai import AsyncOpenAI
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class ChatGPTService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-3.5-turbo"
        logger.info("ChatGPTService initialized with model %s", self.model)

    async def generate_response(self, url: str, report_type: str, industry: str, email: Optional[str] = None) -> str:
        logger.info(f"Generating response for URL: {url}")

        # Define template file path
        template_path = Path(__file__).parent / "prompts" / "prompt_template.txt"

        # Check if the template file exists
        if not template_path.exists():
            logger.error(f"Template file not found at {template_path}")
            raise FileNotFoundError(f"Template file not found at {template_path}")
        
        # Read the template file
        with open(template_path, "r") as file:
            template = file.read()

        # Replace the placeholders in the template with the values
        system_prompt = template.replace("{url}", str(url)) \
                                .replace("{report_type}", str(report_type)) \
                                .replace("{industry}", str(industry)) \
                                .replace("{email}", str(email) if email else "")

        # Print the system prompt for validation
        logger.debug(f"System prompt generated: {system_prompt[:100]}...")  # Log the first 100 chars for brevity
        print(f"Generated System Prompt: {system_prompt}")  # Print the full system prompt for validation

        try:
            # Call the OpenAI API to generate the response
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": system_prompt}],
                max_tokens=5,
                temperature=0.2,
                top_p=1.0,
                frequency_penalty=0.2,
                presence_penalty=0
            )
            logger.info(f"Response generated for URL: {url}")
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating response for URL: {url}, Error: {str(e)}")
            raise