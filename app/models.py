from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    meetings = db.relationship("Meeting", backref="organizer", lazy=True)

    def __repr__(self):
        return f"<User {self.name}>"


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    participants = db.Column(db.String(500), nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Meeting {self.title} on {self.date} at {self.time}>"
