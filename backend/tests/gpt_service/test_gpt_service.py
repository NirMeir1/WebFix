import pytest
from unittest.mock import patch, AsyncMock, mock_open
from gpt_service import ChatGPTService

@pytest.mark.asyncio
async def test_generate_response():
    url = "https://www.happiness.co.il/"
    report_type = "Test Report"
    email = "test@example.com"
    dummy_template = (
        "URL: {url}\n"
        "Report: {report_type}\n"
        "Email: {email}"
    )
    expected_prompt = (
        f"URL: {url}\n"
        f"Report: {report_type}\n"
        f"Email: {email}"
    )
    mock_response = "This is a generated response."

    with patch("gpt_service.AsyncOpenAI") as MockOpenAI, \
         patch("builtins.open", mock_open(read_data=dummy_template)), \
         patch("gpt_service.Path.exists", return_value=True):

        mock_client = AsyncMock()
        MockOpenAI.return_value = mock_client

        # Set up the async API call mock to return a response with the mock_response.
        mock_choice = AsyncMock()
        mock_choice.message.content = mock_response
        mock_client.chat.completions.create.return_value = AsyncMock(
            choices=[mock_choice]
        )

        gpt_service = ChatGPTService()
        result = await gpt_service.generate_response(url, report_type, email)

        # Verify that the API call was made with the expected prompt
        mock_client.chat.completions.create.assert_called_once()
        args, kwargs = mock_client.chat.completions.create.call_args
        messages = kwargs.get("messages")
        assert messages[0]["content"] == expected_prompt

        assert result == mock_response