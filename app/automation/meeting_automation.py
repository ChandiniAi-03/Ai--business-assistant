from datetime import datetime, timedelta

from app.services.gmail_service import (
    get_recent_emails,
    get_email_body
)

from app.automation.meeting_extractor import (
    extract_meeting_details
)

from app.services.calendar_service import (
    create_calendar_event
)

from app.services.database import (
    initialize_database,
    save_meeting,
    save_log,
    meeting_exists
)


def automate_meetings():

    print("\n🤖 MEETING AUTOMATION")
    print("==============================")


    # Initialize database

    initialize_database()


    # Get recent Gmail emails

    emails = get_recent_emails(
        max_results=10
    )


    if not emails:

        print("No emails found.")

        return


    meetings_found = 0

    meetings_saved = 0


    for email in emails:

        # Get full email body

        email["body"] = get_email_body(
            email["id"]
        )


        # Extract meeting information using AI

        meeting = extract_meeting_details(
            email
        )


        # Skip emails that are not meeting requests

        if not meeting.get("is_meeting"):

            continue


        meetings_found += 1


        print("\n📧 Meeting request detected!")

        print(
            f"Subject : {email['subject']}"
        )

        print(
            f"Title   : {meeting.get('title')}"
        )

        print(
            f"Date    : {meeting.get('date')}"
        )

        print(
            f"Time    : {meeting.get('start_time')}"
        )

        print(
            f"Duration: {meeting.get('duration_minutes')} minutes"
        )


        # Check required information

        if (
            not meeting.get("date")
            or not meeting.get("start_time")
        ):

            print(
                "⚠️ Missing date or time. "
                "Calendar event not created."
            )

            save_log(
                action="Meeting automation",
                status="failed",
                details=(
                    "Missing meeting date or start time "
                    f"for email: {email['subject']}"
                )
            )

            continue


        duration = meeting.get(
            "duration_minutes"
        )


        if not duration:

            print(
                "⚠️ Missing duration. "
                "Calendar event not created."
            )

            save_log(
                action="Meeting automation",
                status="failed",
                details=(
                    "Missing meeting duration "
                    f"for email: {email['subject']}"
                )
            )

            continue

        # Prevent duplicate calendar events

        meeting_title = (
            meeting.get("title")
            or "Meeting"
        )

        if meeting_exists(
            title=meeting_title,
            meeting_date=meeting.get("date"),
            start_time=meeting.get("start_time"),
            source_email=email.get("from", "")
        ):

            print(
                "⏭️ Meeting already exists. "
                "Skipping duplicate."
            )

            save_log(
                action="Meeting automation",
                status="skipped",
                details=(
                    f"Duplicate meeting skipped: "
                    f"{meeting_title}"
                )
            )

            continue

        # Create start datetime

        start_datetime = datetime.fromisoformat(
            f"{meeting['date']}"
            f"T{meeting['start_time']}:00+05:30"
        )


        # Calculate end time

        end_datetime = (
            start_datetime
            + timedelta(
                minutes=int(duration)
            )
        )


        # Create event in Google Calendar

        event = create_calendar_event(

            title=(
                meeting.get("title")
                or "Meeting"
            ),

            description=(
                meeting.get("description")
                or email["body"]
            ),

            start_time=(
                start_datetime.isoformat()
            ),

            end_time=(
                end_datetime.isoformat()
            )
        )


        print(
            "\n📅 CALENDAR EVENT CREATED"
        )

        print(
            f"Title : {event.get('summary')}"
        )

        print(
            f"Link  : {event.get('htmlLink')}"
        )


        # Save meeting into SQLite database

        meeting_id = save_meeting(

            title=meeting_title,
            

            meeting_date=meeting.get(
                "date"
            ),

            start_time=meeting.get(
                "start_time"
            ),

            end_time=end_datetime.strftime(
                "%H:%M"
            ),

            description=(
                meeting.get("description")
                or email["body"]
            ),

            calendar_link=event.get(
                "htmlLink"
            ),

            source_email=email.get(
                "from",
                ""
            )
        )


        meetings_saved += 1


        # Save automation log

        save_log(

            action="Meeting created",

            status="success",

            details=(
                f"Meeting ID: {meeting_id} | "
                f"{meeting.get('title')} | "
                f"{meeting.get('date')} "
                f"{meeting.get('start_time')}"
            )
        )


        print(
            f"💾 Meeting saved to database "
            f"(ID: {meeting_id})"
        )


    print("\n==============================")

    print(
        f"Meetings detected : {meetings_found}"
    )

    print(
        f"Meetings saved    : {meetings_saved}"
    )

    print(
        "✅ MEETING AUTOMATION COMPLETE!"
    )

    print("==============================")


if __name__ == "__main__":

    automate_meetings()