import os

import requests
from flask import Blueprint, jsonify, redirect, request, session, url_for
from msal import ConfidentialClientApplication

auth_outlook = Blueprint("auth_outlook", __name__)

CLIENT_ID = os.getenv("OUTLOOK_CLIENT_ID")
CLIENT_SECRET = os.getenv("OUTLOOK_CLIENT_SECRET")
TENANT_ID = os.getenv("OUTLOOK_TENANT_ID")
REDIRECT_URI = "http://localhost:5000/auth/outlook/callback"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = [
    "https://graph.microsoft.com/Mail.Read",
    "https://graph.microsoft.com/Calendars.Read",
]


@auth_outlook.route("/auth/outlook/login")
def login():
    client = ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
    )
    auth_url = client.get_authorization_request_url(SCOPES, redirect_uri=REDIRECT_URI)
    return redirect(auth_url)


@auth_outlook.route("/auth/outlook/callback")
def callback():
    client = ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
    )
    code = request.args.get("code")
    result = client.acquire_token_by_authorization_code(
        code, scopes=SCOPES, redirect_uri=REDIRECT_URI
    )

    if "access_token" in result:
        session["outlook_token"] = result["access_token"]
    else:
        return "Authorization failed.", 400

    return redirect(url_for("main.index"))


@auth_outlook.route("/auth/outlook/logout")
def logout():
    session.pop("outlook_token", None)
    return redirect(url_for("main.index"))


@auth_outlook.route("/auth/outlook/test")
def test_outlook():
    if "outlook_token" not in session:
        return redirect("auth_outlook.login")

    headers = {"Authorization": "Bearer " + session["outlook_token"]}
    response = requests.get(
        "https://graph.microsoft.com/v1.0/me/messages", headers=headers
    )
    email_list = response.json().get("value", [])

    return jsonify(email_list)
