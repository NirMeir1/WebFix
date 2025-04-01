import pytest
from botocore.exceptions import ClientError
from backend.email_service import (
    generate_jwt_token,
    decode_jwt_token,
    send_verification_email,
    send_report_to_user,
    ses_client,
    FRONTEND_VERIFY_URL,
)

# --- JWT Function Tests ---

def test_generate_decode_jwt():
    # Test that data encoded into a JWT can be decoded correctly.
    data = {"user": "test", "role": "admin"}
    token = generate_jwt_token(data)
    decoded = decode_jwt_token(token)
    assert decoded == data

# --- Dummy SES Client for Success Tests ---

class DummySESClient:
    def __init__(self):
        self.called = False
        self.last_kwargs = None

    def send_raw_email(self, **kwargs):
        self.called = True
        self.last_kwargs = kwargs
        return {"MessageId": "dummy-id"}

@pytest.fixture
def dummy_ses(monkeypatch):
    dummy = DummySESClient()
    monkeypatch.setattr(ses_client, "send_raw_email", dummy.send_raw_email)
    return dummy

# --- Email Function Success Tests ---

def test_send_verification_email_success(dummy_ses):
    test_email = "test@example.com"
    test_token = "dummy-token"
    send_verification_email(test_email, test_token)
    # Check that the dummy SES client was called.
    assert dummy_ses.called is True
    # Verify the verification link was built correctly.
    expected_link = f"{FRONTEND_VERIFY_URL}?token={test_token}"
    raw_message = dummy_ses.last_kwargs["RawMessage"]["Data"]
    assert expected_link in raw_message

def test_send_report_to_user_success(dummy_ses):
    test_email = "test@example.com"
    test_report = "This is a report."
    send_report_to_user(test_email, test_report)
    assert dummy_ses.called is True
    raw_message = dummy_ses.last_kwargs["RawMessage"]["Data"]
    assert test_report in raw_message

# --- Helper for Forcing SES Failures ---

def dummy_send_raw_email_failure(**kwargs):
    error_response = {"Error": {"Code": "TestError", "Message": "Test failure"}}
    raise ClientError(error_response, "SendRawEmail")

# --- Email Function Failure Tests ---

def test_send_verification_email_failure(monkeypatch):
    test_email = "test@example.com"
    test_token = "dummy-token"
    monkeypatch.setattr(ses_client, "send_raw_email", dummy_send_raw_email_failure)
    with pytest.raises(ClientError):
        send_verification_email(test_email, test_token)

def test_send_report_to_user_failure(monkeypatch):
    test_email = "test@example.com"
    test_report = "This is a report."
    monkeypatch.setattr(ses_client, "send_raw_email", dummy_send_raw_email_failure)
    with pytest.raises(ClientError):
        send_report_to_user(test_email, test_report)