from datetime import datetime, timedelta

from .models import Meeting, Participant, db


def find_common_time_slot(availability, duration):
    work_start = 9
    work_end = 17

    availability_slots = []
    for slot in availability:
        start = datetime.strptime(slot["start"], "%Y-%m-%dT%H:%M:%S")
        end = datetime.strptime(slot["end"], "%Y-%m-%dT%H:%M:%S")
        availability_slots.append({"start": start, "end": end})

    print(f"Availability slots: {availability_slots}")

    # Use the date from the first availability slot for the current_time
    if availability_slots:
        current_time = availability_slots[0]["start"].replace(
            hour=work_start, minute=0, second=0, microsecond=0
        )
        end_of_day = current_time.replace(
            hour=work_end, minute=0, second=0, microsecond=0
        )

        while current_time < end_of_day:
            available_for_all = all(
                slot["start"] <= current_time
                and slot["end"] >= (current_time + timedelta(minutes=duration))
                for slot in availability_slots
            )

            print(f"Checking slot: {current_time} - Available: {available_for_all}")

            if available_for_all:
                print(f"Common time slot found: {current_time}")
                return current_time.strftime("%Y-%m-%dT%H:%M:%S")

            current_time += timedelta(minutes=30)

    print("No common time slot found")
    return None


def schedule_meeting(meeting_details):
    print(f"Scheduling meeting with details: {meeting_details}")
    availability = meeting_details["availability"]
    duration = meeting_details["duration"]
    common_time_slot = find_common_time_slot(availability, duration)

    if common_time_slot:
        # Fetch the organizer based on email
        organizer_email = "test@example.com"  # You can change this as needed
        organizer = Participant.query.filter_by(email=organizer_email).first()
        if not organizer:
            return "Organizer not found"

        # Save the meeting to the database
        new_meeting = Meeting(
            title="Scheduled Meeting",
            description="Automatically scheduled meeting",
            date=datetime.strptime(common_time_slot, "%Y-%m-%dT%H:%M:%S").date(),
            time=datetime.strptime(common_time_slot, "%Y-%m-%dT%H:%M:%S").time(),
            participants="test@example.com",  # Update this as needed
            organizer_id=organizer.id,
        )
        db.session.add(new_meeting)
        db.session.commit()
        return f"Meeting scheduled at {common_time_slot}"
    else:
        return "No common time slot available"
