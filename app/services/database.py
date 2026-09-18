import os
import sqlite3


BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

DATABASE_FILE = os.path.join(
    BASE_DIR,
    "data",
    "assistant.db"
)


def get_connection():

    os.makedirs(
        os.path.dirname(DATABASE_FILE),
        exist_ok=True
    )

    connection = sqlite3.connect(DATABASE_FILE)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    # -----------------------------
    # Tasks table
    # -----------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            priority TEXT,
            due_date TEXT,
            description TEXT,
            status TEXT DEFAULT 'pending',
            source_email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


    # -----------------------------
    # Automation logs table
    # -----------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS automation_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            status TEXT NOT NULL,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


    # -----------------------------
    # Processed emails table
    # -----------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS processed_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_id TEXT UNIQUE NOT NULL,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


    # -----------------------------
    # Meetings table
    # -----------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            meeting_date TEXT,
            start_time TEXT,
            end_time TEXT,
            description TEXT,
            calendar_link TEXT,
            source_email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


    # -----------------------------
    # AI responses table
    # -----------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient TEXT,
            subject TEXT,
            response TEXT NOT NULL,
            source_email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


    connection.commit()

    connection.close()


# ============================================================
# TASK FUNCTIONS
# ============================================================


def save_task(
    task,
    priority,
    due_date,
    description,
    source_email
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO tasks
        (
            task,
            priority,
            due_date,
            description,
            source_email
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        task,
        priority,
        due_date,
        description,
        source_email
    ))

    connection.commit()

    task_id = cursor.lastrowid

    connection.close()

    return task_id


# ============================================================
# LOG FUNCTIONS
# ============================================================


def save_log(
    action,
    status,
    details=""
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO automation_logs
        (
            action,
            status,
            details
        )
        VALUES (?, ?, ?)
    """, (
        action,
        status,
        details
    ))

    connection.commit()

    connection.close()


# ============================================================
# PROCESSED EMAIL FUNCTIONS
# ============================================================


def is_email_processed(email_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM processed_emails
        WHERE email_id = ?
    """, (email_id,))

    result = cursor.fetchone()

    connection.close()

    return result is not None


def mark_email_processed(email_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO processed_emails
        (
            email_id
        )
        VALUES (?)
    """, (email_id,))

    connection.commit()

    connection.close()


# ============================================================
# MEETING FUNCTIONS
# ============================================================


def save_meeting(
    title,
    meeting_date,
    start_time,
    end_time,
    description,
    calendar_link,
    source_email
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO meetings
        (
            title,
            meeting_date,
            start_time,
            end_time,
            description,
            calendar_link,
            source_email
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        meeting_date,
        start_time,
        end_time,
        description,
        calendar_link,
        source_email
    ))

    connection.commit()

    meeting_id = cursor.lastrowid

    connection.close()

    return meeting_id


# ============================================================
# AI RESPONSE FUNCTIONS
# ============================================================


def save_ai_response(
    recipient,
    subject,
    response,
    source_email
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO ai_responses
        (
            recipient,
            subject,
            response,
            source_email
        )
        VALUES (?, ?, ?, ?)
    """, (
        recipient,
        subject,
        response,
        source_email
    ))

    connection.commit()

    response_id = cursor.lastrowid

    connection.close()

    return response_id

    # ============================================================
# MEETING DUPLICATE CHECK
# ============================================================

def meeting_exists(
    title,
    meeting_date,
    start_time,
    source_email
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM meetings
        WHERE title = ?
        AND meeting_date = ?
        AND start_time = ?
        AND source_email = ?
    """, (
        title,
        meeting_date,
        start_time,
        source_email
    ))

    result = cursor.fetchone()

    connection.close()

    return result is not None