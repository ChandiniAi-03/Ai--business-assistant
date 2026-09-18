from app.automation.task_extractor import extract_task_details


test_email = {
    "subject": "Report review required",
    "body": """
Hi,

Please review the project report and send your
feedback by tomorrow.

This is important because we need to finalize
the report soon.

Thanks
"""
}


result = extract_task_details(test_email)

print("\n📋 TASK EXTRACTION")
print("==============================")
print(f"Is Task      : {result['is_task']}")
print(f"Task         : {result['task']}")
print(f"Priority     : {result['priority']}")
print(f"Due Date     : {result['due_date']}")
print(f"Description  : {result['description']}")
print(f"Status       : {result['status']}")

print("\n✅ TASK EXTRACTION COMPLETE!")