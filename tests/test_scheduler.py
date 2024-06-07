import pytest

from app.scheduler import schedule_meeting


def test_schedule_meeting():
    meeting_details = {"date": "2024-06-15", "time": "10:00:00"}
    scheduled_time = schedule_meeting(meeting_details)
    assert scheduled_time == "2024-06-15 10:00:00"
