from app.services.gmail_service import get_gmail_service


def get_header(headers, name):
    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]

    return "Not available"


def main():

    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        maxResults=5
    ).execute()

    messages = results.get("messages", [])

    print("\n====================================")
    print("📧 AI BUSINESS ASSISTANT")
    print("====================================")

    print(f"\nMessages found: {len(messages)}\n")

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

        sender = get_header(headers, "From")
        subject = get_header(headers, "Subject")
        date = get_header(headers, "Date")

        print("------------------------------------")
        print(f"📨 From    : {sender}")
        print(f"📌 Subject : {subject}")
        print(f"📅 Date    : {date}")
        print(f"🆔 ID      : {message['id']}")

    print("\n✅ Gmail email reading successful!")


if __name__ == "__main__":
    main()