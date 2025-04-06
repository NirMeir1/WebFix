import os
from pathlib import Path
from openai import AsyncOpenAI
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class ChatGPTService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o"
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
                                .replace("{report_type}", report_type) \
                                .replace("{industry}", industry) \
                                .replace("{email}", str(email) if email else "")

        # Print the system prompt for validation
        logger.debug(f"System prompt generated: {system_prompt[:100]}...")  # Log the first 100 chars for brevity
        print(f"Generated System Prompt: {system_prompt}")  # Print the full system prompt for validation

        try:
            # Call the OpenAI API to generate the response
            response = await self.client.responses.create(
                model=self.model,
                tools=[{"type": "web_search_preview", "search_context_size": "high"}],
                tool_choice={"type": "web_search_preview"},
                input=system_prompt
                # max_tokens=5,
                # temperature=0.2,
                # top_p=1.0,
                # frequency_penalty=0.2,
                # presence_penalty=0
            )
            logger.info(f"Response generated for URL: {url}")

            assistant_reply = response.choices[0].message.content[0].text.strip()
            return assistant_reply

        except Exception as e:
            logger.error(f"Error generating response for URL: {url}, Error: {str(e)}")
            raise
    
    async def generate_gpt_report(self, url: str, report_type: str, industry: str, email: Optional[str] = None) -> str:
        """
        Helper function to generate a GPT response using the ChatGPTService.
        """
        output = await self.generate_response(url, report_type, industry, email)
        return output