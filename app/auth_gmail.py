import os

from flask import Blueprint, jsonify, redirect, request, session, url_for
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

auth_gmail = Blueprint("auth_gmail", __name__)

CLIENT_SECRETS_FILE = os.getenv("GMAIL_CLIENT_SECRETS_FILE")
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar.readonly",
]
REDIRECT_URI = "http://localhost:5000/auth/gmail/callback"

flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI
)


@auth_gmail.route("/auth/gmail/login")
def login():
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )
    session["state"] = state
    return redirect(authorization_url)


@auth_gmail.route("/auth/gmail/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        return "State does not match!", 400

    credentials = flow.credentials
    session["google_credentials"] = credentials_to_dict(credentials)

    return redirect(url_for("main.index"))


@auth_gmail.route("/auth/gmail/logout")
def logout():
    session.pop("google_credentials", None)
    return redirect(url_for("main.index"))


@auth_gmail.route("/auth/gmail/test")
def test_gmail():
    if "google_credentials" not in session:
        return redirect("auth_gmail.login")

    credentials = Credentials(**session["google_credentials"])
    service = build("gmail", "v1", credentials=credentials)
    results = service.users().messages().list(userId="me").execute()
    messages = results.get("messages", [])
    email_list = []
    for message in messages:
        msg = service.users().messages().get(userId="me", id=message["id"]).execute()
        email_list.append(msg["snippet"])

    return jsonify(email_list)


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }
