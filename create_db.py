from app import create_app, db
from app.models import Meeting, User

app = create_app()
with app.app_context():
    db.create_all()
