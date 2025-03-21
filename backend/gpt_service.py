import os
from openai import AsyncOpenAI

class ChatGPTService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-3.5-turbo"

    async def generate_response(self, url: str) -> str:
        with open("prompt_template.txt", "r") as file:
            template = file.read()

        system_prompt = template.replace("{url}", url)

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt}
            ],
            max_tokens=10,
            temperature=0.2,
            top_p=1.0,
            frequency_penalty=0.2,
            presence_penalty=0
        )
        return response.choices[0].message.content.strip()