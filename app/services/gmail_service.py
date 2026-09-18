import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

CREDENTIALS_FILE = os.path.join(
    BASE_DIR,
    "credentials",
    "credentials.json"
)

TOKEN_FILE = os.path.join(
    BASE_DIR,
    "token.json"
)


def get_gmail_service():

    credentials = None

    if os.path.exists(TOKEN_FILE):
        credentials = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    if not credentials or not credentials.valid:

        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )

            credentials = flow.run_local_server(
                port=0
            )

        with open(TOKEN_FILE, "w") as token:
            token.write(credentials.to_json())

    service = build(
        "gmail",
        "v1",
        credentials=credentials
    )

    return service

def get_header(headers, name):

    for header in headers:

        if header["name"].lower() == name.lower():
            return header["value"]

    return "Not available"

def get_recent_emails(max_results=10):

    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])

    emails = []

    for message in messages:

        message_data = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="metadata",
            metadataHeaders=[
                "From",
                "Subject",
                "Date"
            ]
        ).execute()

        headers = message_data["payload"]["headers"]

        email_info = {
            "id": message["id"],
            "from": get_header(headers, "From"),
            "subject": get_header(headers, "Subject"),
            "date": get_header(headers, "Date")
        }

        emails.append(email_info)

    return emails

def get_email_body(message_id):
    service = get_gmail_service()

    message = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    payload = message.get("payload", {})

    def extract_text(part):
        mime_type = part.get("mimeType", "")
        body_data = part.get("body", {}).get("data")

        if mime_type == "text/plain" and body_data:
            import base64
            return base64.urlsafe_b64decode(
                body_data
            ).decode("utf-8", errors="ignore")

        for subpart in part.get("parts", []):
            text = extract_text(subpart)
            if text:
                return text

        return ""

    return extract_text(payload)