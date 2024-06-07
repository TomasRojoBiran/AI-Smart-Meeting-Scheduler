import pytest

from app.nlp import extract_meeting_details


def test_extract_meeting_details():
    email_content = "Schedule a meeting for tomorrow at 10 AM."
    details = extract_meeting_details(email_content)
    assert details is not None
