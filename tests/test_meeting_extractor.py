from app.automation.meeting_extractor import extract_meeting_details


test_email = {
    "subject": "Project discussion tomorrow",
    "body": """
Hi,

Can we have a project discussion tomorrow at 3 PM?
It should take around 30 minutes.

Thanks
"""
}

result = extract_meeting_details(test_email)

print("\n📅 MEETING DETAIL EXTRACTION")
print("==============================")
print(f"Is Meeting       : {result['is_meeting']}")
print(f"Title            : {result['title']}")
print(f"Date             : {result['date']}")
print(f"Start Time       : {result['start_time']}")
print(f"Duration         : {result['duration_minutes']} minutes")
print(f"Description      : {result['description']}")

print("\n✅ MEETING EXTRACTION COMPLETE!")