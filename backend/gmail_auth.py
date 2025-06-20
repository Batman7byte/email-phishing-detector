import os
import pickle
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(BASE_DIR, "token.pickle")
CREDENTIALS_PATH = os.path.join(BASE_DIR, "./credentials.json")


# Authenticate Gmail API
def authenticate_gmail():
    creds = None

    # Load saved credentials
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "rb") as token:
            creds = pickle.load(token)

    # Refresh or request new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0, access_type="offline")

        # Save credentials for later use
        with open(TOKEN_PATH, "wb") as token:
            pickle.dump(creds, token)

    return creds


# Function to extract email body correctly
def extract_email_body(payload):
    """Extracts plain text email body, handling multipart emails."""
    email_body = ""

    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                try:
                    email_body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                except Exception as e:
                    print(f"Decoding error: {e}")
                    email_body = ""
                break
    else:
        # If no "parts", try extracting from body
        try:
            email_body = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")
        except Exception as e:
            print(f"Decoding error: {e}")
            email_body = ""

    return email_body


# Fetch unread emails
def fetch_emails():
    creds = authenticate_gmail()
    service = build("gmail", "v1", credentials=creds)

    # Get unread emails
    results = service.users().messages().list(userId="me", labelIds=["INBOX"], q="is:unread").execute()
    messages = results.get("messages", [])

    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        email_body = extract_email_body(msg_data["payload"])

        emails.append({
            "id": msg["id"],
            "snippet": msg_data.get("snippet", ""),
            "body": email_body
        })

    return emails


# Run the script (for testing)
if __name__ == "__main__":
    fetched_emails = fetch_emails()
    for email in fetched_emails:
        print(f"Email ID: {email['id']}\nSnippet: {email['snippet']}\nBody: {email['body']}\n{'-' * 50}")
