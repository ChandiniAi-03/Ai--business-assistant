from app.automation.meeting_extractor import extract_meeting_details


test_email = {
    "subject": "Project discussion tomorrow at 3 PM",
    "body": """
    Hi,

    Can we have a project discussion tomorrow at 3 PM?
    The meeting will take around 30 minutes.

    Thanks
    """
}


print("\n🤖 TESTING MEETING EXTRACTION")
print("==============================")

meeting = extract_meeting_details(test_email)


print(f"Is Meeting : {meeting.get('is_meeting')}")
print(f"Title      : {meeting.get('title')}")
print(f"Date       : {meeting.get('date')}")
print(f"Time       : {meeting.get('start_time')}")
print(
    f"Duration   : "
    f"{meeting.get('duration_minutes')} minutes"
)


if meeting.get("is_meeting"):

    if meeting.get("duration_minutes"):

        print("\n✅ Meeting details extracted successfully!")

    else:

        print(
            "\n⚠️ Meeting detected, "
            "but duration was not extracted."
        )

else:

    print("\nℹ️ No meeting detected.")


print("==============================")