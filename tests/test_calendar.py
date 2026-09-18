from app.services.calendar_service import get_calendar_service


def main():
    service = get_calendar_service()

    calendar_list = service.calendarList().list().execute()

    print("\n📅 GOOGLE CALENDAR")
    print("==============================")

    for calendar in calendar_list.get("items", []):
        print(f"📌 {calendar.get('summary')}")

    print("\n✅ GOOGLE CALENDAR CONNECTION SUCCESSFUL!")


if __name__ == "__main__":
    main()