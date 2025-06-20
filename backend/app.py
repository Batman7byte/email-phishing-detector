import base64
import os
import pickle
import threading
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API Scopes
SCOPES = ["https://mail.google.com/"]


app = Flask(__name__)
CORS(app)

# Load phishing detection model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

emails_cache = []  # Store scanned emails in memory


# Authenticate with Gmail API
def authenticate_gmail():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("../backend/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return creds


# Fetch unread emails from Gmail
def fetch_emails():
    global emails_cache
    creds = authenticate_gmail()
    service = build("gmail", "v1", credentials=creds)

    try:
        results = service.users().messages().list(userId="me", labelIds=["INBOX"], q="is:unread").execute()
        messages = results.get("messages", [])

        emails = []
        for msg in messages:
            msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
            email_body = ""

            if "payload" in msg_data and "parts" in msg_data["payload"]:
                for part in msg_data["payload"]["parts"]:
                    if part["mimeType"] == "text/plain" and "data" in part["body"]:
                        email_body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                        break

            # Predict if the email is phishing
            is_phishing = model.predict([email_body])[0]

            emails.append({
                "id": msg["id"],
                "snippet": msg_data["snippet"],
                "body": email_body,
                "is_phishing": bool(is_phishing)
            })

        emails_cache = emails  # Update cache with new emails
    except Exception as e:
        print(f"Error fetching emails: {e}")


# Background thread for real-time scanning
def scan_emails_continuously():
    while True:
        fetch_emails()
        time.sleep(10)  # Scan every 10 seconds


# API endpoint to return scanned emails
@app.route("/emails", methods=["GET"])
def get_emails():
    return jsonify(emails_cache)


import traceback
from googleapiclient.errors import HttpError  # ✅ Import this

@app.route("/delete_emails", methods=["POST"])
def delete_emails():
    try:
        data = request.json
        email_ids = data.get("email_ids", [])

        if not email_ids:
            return jsonify({"error": "No email IDs provided"}), 400  # 🚨 Proper error handling

        creds = authenticate_gmail()
        service = build("gmail", "v1", credentials=creds)

        for email_id in email_ids:
            service.users().messages().modify(
                userId="me",
                id=email_id,
                body={"removeLabelIds": ["INBOX"], "addLabelIds": ["TRASH"]}
            ).execute()

        return jsonify({"message": "Emails moved to Trash"}), 200

    except HttpError as e:
        error_details = e.content.decode("utf-8") if hasattr(e, "content") else str(e)
        print(f"Google API Error: {error_details}")  # 🔍 Print full error details
        return jsonify({"error": "Google API Error", "details": error_details}), 500

    except Exception as e:
        error_message = traceback.format_exc()
        print(f"Unexpected Error: {error_message}")  # 🔍 Print unexpected errors
        return jsonify({"error": str(e), "details": error_message}), 500





# Start background scanning thread
threading.Thread(target=scan_emails_continuously, daemon=True).start()

if __name__ == "__main__":
    app.run(debug=True)
