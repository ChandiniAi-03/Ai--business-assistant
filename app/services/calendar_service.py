import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/calendar"
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
    "calendar_token.json"
)


def get_calendar_service():
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

            credentials = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as token:
            token.write(credentials.to_json())

    service = build(
        "calendar",
        "v3",
        credentials=credentials
    )

    return service

def create_calendar_event(
    title,
    description,
    start_time,
    end_time,
):
    service = get_calendar_service()

    event = {
        "summary": title,
        "description": description,
        "start": {
            "dateTime": start_time,
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": end_time,
            "timeZone": "Asia/Kolkata",
        },
    }

    created_event = service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    return created_event