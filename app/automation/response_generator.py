import ollama

from app.services.database import (
    initialize_database,
    save_ai_response,
    save_log
)


def generate_ai_response(email, email_analysis):

    initialize_database()

    sender = email.get("from", "")
    subject = email.get("subject", "")

    intent = email_analysis.get(
        "intent",
        "general"
    )

    urgency = email_analysis.get(
        "urgency",
        "low"
    )


    prompt = f"""
You are an AI business assistant.

Generate a professional, polite, concise email reply.

Email sender:
{sender}

Email subject:
{subject}

Detected intent:
{intent}

Urgency:
{urgency}

Rules:
- Do not invent facts.
- Do not promise a specific meeting time.
- Do not mention that you are an AI.
- Keep the response between 3 and 6 sentences.
- Make it sound natural and professional.
"""


    response = ollama.chat(

        model="llama3.2",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    generated_response = (
        response["message"]["content"]
        .strip()
    )


    # Save AI response to database

    response_id = save_ai_response(

        recipient=sender,

        subject=subject,

        response=generated_response,

        source_email=sender
    )


    # Save automation log

    save_log(

        action="AI response generated",

        status="success",

        details=(
            f"Response ID: {response_id} | "
            f"Subject: {subject}"
        )
    )


    print("\n💾 AI RESPONSE SAVED")

    print(
        f"Response ID: {response_id}"
    )


    return generated_response