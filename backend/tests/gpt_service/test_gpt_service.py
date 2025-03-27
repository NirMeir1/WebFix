import pytest
from unittest.mock import patch, AsyncMock
from gpt_service import ChatGPTService

@pytest.mark.asyncio
async def test_generate_response():
    url = "https://www.happiness.co.il/"
    mock_response = "This is a generated response."

    # Correctly patching with AsyncMock for async functions
    with patch("gpt_service.AsyncOpenAI") as MockOpenAI:
        mock_client = AsyncMock()
        MockOpenAI.return_value = mock_client
        
        # Correctly mock async API call
        mock_client.chat.completions.create.return_value = AsyncMock(
            choices=[
                AsyncMock(message=AsyncMock(content=mock_response))
            ]
        )

        gpt_service = ChatGPTService()
        result = await gpt_service.generate_response(url)

        assert result == mock_response