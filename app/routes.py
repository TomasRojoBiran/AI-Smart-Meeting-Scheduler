from flask import Blueprint, jsonify, render_template, request

from .models import Meeting, Participant, db
from .nlp import extract_meeting_details
from .scheduler import schedule_meeting

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/schedule", methods=["POST"])
def schedule():
    email_content = request.json.get("email")
    meeting_details = extract_meeting_details(email_content)
    scheduled_time = schedule_meeting(meeting_details)
    if scheduled_time != "No common time slot available":
        return jsonify({"scheduled_time": f"Meeting scheduled at {scheduled_time}"})
    else:
        return jsonify({"scheduled_time": "No common time slot available"})


# Participant management routes
@main.route("/participants", methods=["POST"])
def create_participant():
    data = request.json
    new_participant = Participant(email=data["email"], name=data["name"])
    db.session.add(new_participant)
    db.session.commit()
    return jsonify({"message": "Participant created successfully"}), 201


@main.route("/participants", methods=["GET"])
def get_participants():
    participants = Participant.query.all()
    return jsonify(
        [
            {"id": participant.id, "email": participant.email, "name": participant.name}
            for participant in participants
        ]
    )


@main.route("/participants/<int:id>", methods=["PUT"])
def update_participant(id):
    data = request.json
    participant = Participant.query.get_or_404(id)
    participant.email = data.get("email", participant.email)
    participant.name = data.get("name", participant.name)
    db.session.commit()
    return jsonify({"message": "Participant updated successfully"})


@main.route("/participants/<int:id>", methods=["DELETE"])
def delete_participant(id):
    participant = Participant.query.get_or_404(id)
    db.session.delete(participant)
    db.session.commit()
    return jsonify({"message": "Participant deleted successfully"})


# Meeting management routes
@main.route("/meetings", methods=["POST"])
def create_meeting():
    data = request.json
    new_meeting = Meeting(
        title=data["title"],
        description=data.get("description"),
        date=data["date"],
        time=data["time"],
        participants=data["participants"],
        organizer_id=data["organizer_id"],
    )
    db.session.add(new_meeting)
    db.session.commit()
    return jsonify({"message": "Meeting created successfully"}), 201


@main.route("/meetings", methods=["GET"])
def get_meetings():
    meetings = Meeting.query.all()
    return jsonify(
        [
            {
                "id": meeting.id,
                "title": meeting.title,
                "description": meeting.description,
                "date": meeting.date.isoformat(),
                "time": meeting.time.isoformat(),
                "participants": meeting.participants,
                "organizer_id": meeting.organizer_id,
            }
            for meeting in meetings
        ]
    )


@main.route("/meetings/<int:id>", methods=["PUT"])
def update_meeting(id):
    data = request.json
    meeting = Meeting.query.get_or_404(id)
    meeting.title = data.get("title", meeting.title)
    meeting.description = data.get("description", meeting.description)
    meeting.date = data.get("date", meeting.date)
    meeting.time = data.get("time", meeting.time)
    meeting.participants = data.get("participants", meeting.participants)
    meeting.organizer_id = data.get("organizer_id", meeting.organizer_id)
    db.session.commit()
    return jsonify({"message": "Meeting updated successfully"})


@main.route("/meetings/<int:id>", methods=["DELETE"])
def delete_meeting(id):
    meeting = Meeting.query.get_or_404(id)
    db.session.delete(meeting)
    db.session.commit()
    return jsonify({"message": "Meeting deleted successfully"})
