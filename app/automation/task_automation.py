from app.automation.task_extractor import extract_task_details
from app.services.database import initialize_database, save_task, save_log


def automate_task(email):
    task_details = extract_task_details(email)

    if not task_details.get("is_task"):
        return None

    task = task_details.get("task")
    priority = task_details.get("priority")
    due_date = task_details.get("due_date")
    description = task_details.get("description")

    if not task:
        save_log(
            action="Task extraction",
            status="failed",
            details="AI detected a task but returned no task description."
        )
        return None

    task_id = save_task(
        task=task,
        priority=priority,
        due_date=due_date,
        description=description,
        source_email=email.get("from", "")
    )

    save_log(
        action="Task created",
        status="success",
        details=f"Task ID: {task_id} | {task}"
    )

    return {
        "id": task_id,
        "task": task,
        "priority": priority,
        "due_date": due_date,
        "description": description,
        "status": "pending"
    }


if __name__ == "__main__":

    initialize_database()

    test_email = {
        "from": "test@example.com",
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

    result = automate_task(test_email)

    print("\n📋 TASK AUTOMATION")
    print("==============================")

    if result:
        print(f"Task ID     : {result['id']}")
        print(f"Task        : {result['task']}")
        print(f"Priority    : {result['priority']}")
        print(f"Due Date    : {result['due_date']}")
        print(f"Description : {result['description']}")
        print(f"Status      : {result['status']}")

        print("\n✅ TASK SAVED TO DATABASE!")

    else:
        print("No actionable task found.")