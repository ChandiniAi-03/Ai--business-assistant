from app.automation.email_analyzer import analyze_email


test_email = {
    "id": "test123",
    "from": "client@example.com",
    "subject": "Urgent: Can we schedule a meeting tomorrow?"
}


result = analyze_email(test_email)


print("\n🧠 AI BUSINESS ASSISTANT")
print("==============================")

print(f"📧 From            : {result['from']}")
print(f"📌 Subject         : {result['subject']}")
print(f"🎯 Intent          : {result['intent']}")
print(f"✅ Action Required : {result['action_required']}")
print(f"✍️ Needs Response  : {result['needs_response']}")
print(f"🚨 Urgency         : {result['urgency']}")
print(f"📋 Task            : {result['task']}")