from flask import Blueprint, jsonify, render_template, request

from .email_gmail import fetch_gmail_email
from .email_outlook import fetch_outlook_emails
from .models import Meeting, User, db
from .nlp import extract_meeting_details
from .scheduler import schedule_meeting

main = Blueprint("main", __name__)


# Home route
@main.route("/")
def index():
    return render_template("index.html")


# Schedule Meeting
@main.route("/schedule", methods=["POST"])
def schedule():
    email_content = request.json.get("email")
    meeting_details = extract_meeting_details(email_content)
    scheduled_time = schedule_meeting(meeting_details)
    return jsonify({"scheduled_time": scheduled_time})


# Fetch Gmail Emails
@main.route("/emails/gmail", methods=["GET"])
def gmail_emails():
    emails = fetch_gmail_emails()
    return jsonify({"emails": emails})


# Fetch Outlook Emails
@main.route("/emails/outlook", methods=["GET"])
def outlook_emails():
    emails = fetch_outlook_emails()
    return jsonify({"emails": emails})


# Create User
@main.route("/users", methods=["POST"])
def create_user():
    data = request.json
    new_user = User(email=data["email"], name=data["name"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201


# Read Users
@main.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify(
        [{"id": user.id, "email": user.email, "name": user.name} for user in users]
    )


# Update User
@main.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.json
    user = User.query.get_or_404(id)
    user.email = data.get("email", user.email)
    user.name = data.get("name", user.name)
    db.session.commit()
    return jsonify({"message": "User updated successfully"})


# Delete User
@main.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})


# Create Meeting
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


# Read Meetings
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


# Update Meeting
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


# Delete Meeting
@main.route("/meetings/<int:id>", methods=["DELETE"])
def delete_meeting(id):
    meeting = Meeting.query.get_or_404(id)
    db.session.delete(meeting)
    db.session.commit()
    return jsonify({"message": "Meeting deleted successfully"})
