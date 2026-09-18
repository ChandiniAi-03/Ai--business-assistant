import json
from datetime import datetime
from zoneinfo import ZoneInfo

import ollama


def extract_task_details(email):
    subject = email.get("subject", "")
    body = email.get("body", "")

    today = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).date().isoformat()

    prompt = f"""
You are a task extraction assistant.

Today's date is {today}.

Read the email below and determine whether it contains
an actionable task.

Subject:
{subject}

Email:
{body}

Return ONLY valid JSON in exactly this format:

{{
    "is_task": true,
    "task": "short task description",
    "priority": "high",
    "due_date": "YYYY-MM-DD",
    "description": "short description",
    "status": "pending"
}}

Rules:
- If there is no actionable task, set "is_task" to false.
- Priority must be one of: high, medium, low.
- If priority is not clear, use "medium".
- If there is no due date, use null.
- Do not invent a due date.
- If the email says "today", use today's date.
- If the email says "tomorrow", use tomorrow's date.
- Convert dates to YYYY-MM-DD.
- Status must always be "pending".
- Return ONLY JSON.
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
            "is_task": False,
            "task": None,
            "priority": None,
            "due_date": None,
            "description": None,
            "status": None
        }