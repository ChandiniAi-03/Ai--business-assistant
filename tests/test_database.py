from app.services.database import (
    initialize_database,
    save_task,
    save_log
)


initialize_database()

task_id = save_task(
    task="Review project report",
    priority="high",
    due_date="2026-09-18",
    description="Review the report and send feedback.",
    source_email="test@example.com"
)

save_log(
    action="Task created",
    status="success",
    details=f"Task ID: {task_id}"
)

print("\n🗄️ DATABASE TEST")
print("==============================")
print(f"Task ID : {task_id}")
print("Database initialized successfully.")
print("Task saved successfully.")
print("Automation log saved successfully.")

print("\n✅ DATABASE TEST COMPLETE!")