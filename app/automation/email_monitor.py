from app.services.gmail_service import get_recent_emails


def monitor_emails():

    emails = get_recent_emails(max_results=10)

    print("\n📧 EMAIL MONITOR")
    print("==============================")

    print(f"Emails detected: {len(emails)}\n")

    for email in emails:

        print("--------------------------------")
        print(f"From    : {email['from']}")
        print(f"Subject : {email['subject']}")
        print(f"Date    : {email['date']}")
        print(f"ID      : {email['id']}")

    return emails


if __name__ == "__main__":
    monitor_emails()