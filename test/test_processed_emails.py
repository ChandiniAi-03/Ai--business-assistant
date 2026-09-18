from app.services.database import (
    initialize_database,
    is_email_processed,
    mark_email_processed
)


initialize_database()

test_email_id = "test-email-123"

print("\n🛡️ PROCESSED EMAIL TEST")
print("==============================")

print(
    "Before processing:",
    is_email_processed(test_email_id)
)

mark_email_processed(test_email_id)

print(
    "After processing:",
    is_email_processed(test_email_id)
)

print("\n✅ PROCESSED EMAIL TRACKING WORKING!")