from app.automation.response_generator import generate_ai_response


test_email = {
    "from": "client@example.com",
    "subject": "Can we schedule a meeting tomorrow?"
}

test_analysis = {
    "intent": "meeting_request",
    "urgency": "medium"
}


response = generate_ai_response(
    test_email,
    test_analysis
)

print("\n🤖 LOCAL AI RESPONSE")
print("==============================")
print(response)
print("\n✅ LOCAL AI RESPONSE SUCCESSFUL!")