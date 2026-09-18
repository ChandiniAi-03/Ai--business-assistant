from app.services.gmail_service import (
    get_recent_emails,
    get_email_body
)

from app.services.database import (
    initialize_database,
    save_log,
    is_email_processed,
    mark_email_processed
)

from app.automation.task_automation import automate_task
from app.automation.email_analyzer import analyze_email
from app.automation.response_generator import generate_ai_response


def run_inbox_automation():

    print("\n🤖 AI BUSINESS ASSISTANT")
    print("==============================")
    print("📧 Scanning Gmail...\n")

    initialize_database()

    emails = get_recent_emails(max_results=10)

    if not emails:

        print("No emails found.")

        return


    processed_count = 0
    skipped_count = 0
    tasks_found = 0
    responses_generated = 0


    for email in emails:

        email_id = email["id"]


        # Check whether email was already processed

        if is_email_processed(email_id):

            print("--------------------------------")
            print("⏭️ Skipping already processed email")
            print(f"Subject : {email['subject']}")

            skipped_count += 1

            continue


        # Get full email body

        email["body"] = get_email_body(email_id)


        # ====================================================
        # TASK AUTOMATION
        # ====================================================

        result = automate_task(email)


        if result:

            tasks_found += 1

            print("--------------------------------")
            print(f"📋 Task       : {result['task']}")
            print(f"🎯 Priority   : {result['priority']}")
            print(f"📅 Due Date   : {result['due_date']}")
            print(f"📌 Status     : {result['status']}")


        else:

            print("--------------------------------")
            print("ℹ️ No actionable task found.")
            print(f"Subject : {email['subject']}")


        # ====================================================
        # AI RESPONSE GENERATION
        # ====================================================

        analysis = analyze_email(email)


        if analysis.get("needs_response"):

            print("\n🤖 Generating AI response...")


            response = generate_ai_response(
                email,
                analysis
            )


            responses_generated += 1


            print("\n✉️ AI RESPONSE:")
            print("------------------------------")
            print(response)


        # ====================================================
        # MARK EMAIL AS PROCESSED
        # ====================================================

        mark_email_processed(email_id)

        processed_count += 1


    # ========================================================
    # AUTOMATION LOG
    # ========================================================

    save_log(
        action="Gmail automation",
        status="success",
        details=(
            f"Processed: {processed_count}, "
            f"Skipped: {skipped_count}, "
            f"Tasks found: {tasks_found}, "
            f"Responses generated: {responses_generated}"
        )
    )


    print("\n==============================")
    print(f"New emails processed : {processed_count}")
    print(f"Already processed    : {skipped_count}")
    print(f"Tasks found          : {tasks_found}")
    print(
        f"Responses generated  : "
        f"{responses_generated}"
    )
    print("✅ INBOX AUTOMATION COMPLETE!")
    print("==============================")


if __name__ == "__main__":

    run_inbox_automation()