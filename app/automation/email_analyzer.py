def analyze_email(email):
    subject = email.get("subject", "")
    sender = email.get("from", "")
    body = email.get("body", "")

    text = f"{subject} {sender} {body}".lower()

    result = {
        "email_id": email.get("id"),
        "from": sender,
        "subject": subject,
        "body": body,
        "intent": "general",
        "action_required": False,
        "needs_response": False,
        "urgency": "low",
        "task": None
    }

    if any(word in text for word in [
        "meeting",
        "schedule",
        "call",
        "appointment"
    ]):
        result["intent"] = "meeting_request"
        result["action_required"] = True
        result["needs_response"] = True
        result["task"] = "Review and schedule meeting"

    if any(word in text for word in [
        "urgent",
        "asap",
        "immediately",
        "deadline"
    ]):
        result["urgency"] = "high"

    elif any(word in text for word in [
        "please send",
        "please review",
        "action required",
        "follow up",
        "complete"
    ]):
        result["intent"] = "task"
        result["action_required"] = True
        result["needs_response"] = True
        result["task"] = "Review email and complete requested action"

    elif any(word in text for word in [
        "question",
        "request",
        "could you",
        "can you",
        "please"
    ]):
        result["intent"] = "response_required"
        result["needs_response"] = True

    return result


def analyze_emails(emails):
    analyzed_emails = []

    for email in emails:
        analysis = analyze_email(email)
        analyzed_emails.append(analysis)

    return analyzed_emails