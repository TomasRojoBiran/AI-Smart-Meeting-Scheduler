import os

from celery import Celery
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__, template_folder="../templates")
    app.secret_key = os.getenv("SECRET_KEY")

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
    app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"

    db.init_app(app)
    migrate.init_app(app, db)

    celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
    celery.conf.update(app.config)

    from .auth_gmail import auth_gmail as auth_gmail_blueprint
    from .auth_outlook import auth_outlook as auth_outlook_blueprint
    from .routes import main as main_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_gmail_blueprint, url_prefix="/auth/gmail")
    app.register_blueprint(auth_outlook_blueprint, url_prefix="/auth/outlook")

    return app
