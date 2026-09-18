from app.services.gmail_service import get_recent_emails, get_email_body
from app.automation.email_analyzer import analyze_emails
from app.automation.response_generator import generate_ai_response


def main():
    print("\n🧠 AI BUSINESS ASSISTANT")
    print("==============================")
    print("📧 Reading and analyzing your Gmail...\n")

    emails = get_recent_emails(max_results=10)

    if not emails:
        print("No emails found.")
        return

    # Add the actual email body to every email
    for email in emails:
        email["body"] = get_email_body(email["id"])

    analyzed_emails = analyze_emails(emails)

    for email in analyzed_emails:
        print("--------------------------------")
        print(f"📨 From            : {email['from']}")
        print(f"📌 Subject         : {email['subject']}")
        print(f"🎯 Intent          : {email['intent']}")
        print(f"✅ Action Required : {email['action_required']}")
        print(f"✍️ Needs Response  : {email['needs_response']}")
        print(f"🚨 Urgency         : {email['urgency']}")
        print(f"📋 Task            : {email['task']}")

        if email["needs_response"]:
            original_email = next(
                item for item in emails
                if item["id"] == email["email_id"]
            )

            response = generate_ai_response(
                original_email,
                email
            )

            print("\n🤖 AI GENERATED RESPONSE:")
            print("------------------------------")
            print(response)

    print("\n================================")
    print("✅ FULL EMAIL ANALYSIS COMPLETE!")
    print("================================")


if __name__ == "__main__":
    main()