from flask import Flask, render_template, redirect, url_for
import os

from app.services.database import (
    initialize_database,
    get_connection
)

from app.automation.inbox_automation import (
    run_inbox_automation
)

from app.automation.meeting_automation import (
    automate_meetings
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
    static_url_path="/static"
)


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/")
def home():

    initialize_database()

    connection = get_connection()
    cursor = connection.cursor()


    # Emails processed

    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM processed_emails
    """)

    emails_processed = cursor.fetchone()["count"]


    # Action items

    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM tasks
    """)

    action_items = cursor.fetchone()["count"]


    # Meetings

    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM meetings
    """)

    meetings = cursor.fetchone()["count"]


    # AI responses

    cursor.execute("""
        SELECT COUNT(*) AS count
        FROM ai_responses
    """)

    responses = cursor.fetchone()["count"]


    # Tasks

    cursor.execute("""
        SELECT
            id,
            task,
            priority,
            due_date,
            description,
            status,
            source_email,
            created_at
        FROM tasks
        ORDER BY id DESC
    """)

    tasks = [
        dict(row)
        for row in cursor.fetchall()
    ]


    # Meetings

    cursor.execute("""
        SELECT
            id,
            title,
            meeting_date,
            start_time,
            end_time,
            description,
            calendar_link,
            source_email,
            created_at
        FROM meetings
        ORDER BY id DESC
        LIMIT 10
    """)

    meeting_list = [
        dict(row)
        for row in cursor.fetchall()
    ]


    # AI responses

    cursor.execute("""
        SELECT
            id,
            recipient,
            subject,
            response,
            source_email,
            created_at
        FROM ai_responses
        ORDER BY id DESC
        LIMIT 10
    """)

    response_list = [
        dict(row)
        for row in cursor.fetchall()
    ]


    # Automation logs

    cursor.execute("""
        SELECT
            id,
            action,
            status,
            details,
            created_at
        FROM automation_logs
        ORDER BY id DESC
        LIMIT 10
    """)

    logs = [
        dict(row)
        for row in cursor.fetchall()
    ]


    connection.close()


    return render_template(
        "dashboard.html",

        emails_processed=emails_processed,

        action_items=action_items,

        meetings=meetings,

        responses=responses,

        tasks=tasks,

        meeting_list=meeting_list,

        response_list=response_list,

        logs=logs
    )


# ============================================================
# SCAN GMAIL
# ============================================================

@app.route("/run-inbox-automation")
def run_inbox():

    try:

        run_inbox_automation()

    except Exception as error:

        print(
            f"❌ Inbox automation error: {error}"
        )

    return redirect(url_for("home"))


# ============================================================
# PROCESS MEETINGS
# ============================================================

@app.route("/run-meeting-automation")
def run_meetings():

    try:

        automate_meetings()

    except Exception as error:

        print(
            f"❌ Meeting automation error: {error}"
        )

    return redirect(url_for("home"))


# ============================================================
# FULL AUTOMATION
# ============================================================

@app.route("/run-full-automation")
def run_full_automation():

    try:

        print("\n🤖 FULL AI AUTOMATION")
        print("==============================")

        run_inbox_automation()

        automate_meetings()

        print("==============================")
        print("✅ FULL AUTOMATION COMPLETE!")
        print("==============================")


    except Exception as error:

        print(
            f"❌ Full automation error: {error}"
        )


    return redirect(url_for("home"))


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(debug=True)