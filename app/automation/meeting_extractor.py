import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import ollama


def extract_meeting_details(email):
    subject = email.get("subject", "")
    body = email.get("body", "")

    today = datetime.now(ZoneInfo("Asia/Kolkata")).date()
    today_str = today.isoformat()
    tomorrow_str = (today + timedelta(days=1)).isoformat()

    prompt = f"""
You are a meeting-information extraction assistant.

Today's date is {today_str}.
Tomorrow's date is {tomorrow_str}.

Read the email below and extract meeting details.

Subject:
{subject}

Email:
{body}

Return ONLY valid JSON in exactly this format:

{{
    "is_meeting": true,
    "title": "short meeting title",
    "date": "YYYY-MM-DD",
    "start_time": "HH:MM",
    "duration_minutes": 30,
    "description": "short description"
}}

Rules:
- If this is not a meeting request, set "is_meeting" to false.
- Use 24-hour time.
- If the date or time is missing, use null.
- Do not invent missing information.
- If the email says "today", use today's date: {today_str}.
- If the email says "tomorrow", use tomorrow's date: {tomorrow_str}.
- If the email says "day after tomorrow", use the date two days from today.
- duration_minutes should be a number or null.
- Return ONLY JSON. Do not add explanations or markdown.
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

    content = response["message"]["content"].strip()

    try:
        return json.loads(content)

    except json.JSONDecodeError:
        print("⚠️ AI returned invalid JSON:")
        print(content)

        return {
            "is_meeting": False,
            "title": None,
            "date": None,
            "start_time": None,
            "duration_minutes": None,
            "description": None
        }