from datetime import date
from task_manager import TaskManager
from task import Task
from validators import is_valid_user_selection
from features import get_reminder_summary

tm = TaskManager()


def seed_users_if_needed():
    # Creates the 3 student accounts + 1 admin the first time the app runs
    # on a fresh database. Does nothing if users already exist.
    if not tm.get_all_users():
        tm.add_user("Student A", "student")
        tm.add_user("Student B", "student")
        tm.add_user("Student C", "student")
        tm.add_user("Admin", "admin")
        print("First run detected — seeded 3 students + 1 admin.")


def show_admin_dashboard():
    raw_users = tm.get_all_users()
    users = [{"id": u[0], "name": u[1], "role": u[2], "last_login": u[3]} for u in raw_users]
    today = str(date.today())
    print("==== ADMIN DASHBOARD ====")
    for user in users:
        if user["role"] == "admin":
            continue
        tasks = tm.get_tasks_for_user(user["id"])
        pending = len([t for t in tasks if t.status != "Completed"])
        overdue = len([t for t in tasks if t.status != "Completed" and t.due_date < today])
        print(f"{user['name']} | Last login: {user['last_login']} | Pending: {pending} | Overdue: {overdue}")


def show_reminders(user_id):
    # TEMPORARY local wrapper — Regan's real show_reminders() isn't in features.py yet.
    # Uses the real get_reminder_summary() that already exists there.
    tasks = tm.get_tasks_for_user(user_id)
    summary = get_reminder_summary(tasks)
    print("==== REMINDERS ====")
    if summary["overdue"]:
        print("Overdue:")
        for t in summary["overdue"]:
            print(f"  - {t.title} ({t.due_date})")
    if summary["upcoming"]:
        print("Upcoming:")
        for t in summary["upcoming"]:
            print(f"  - {t.title} ({t.due_date})")
    if not summary["overdue"] and not summary["upcoming"]:
        print("Nothing due soon.")


def show_login_screen():
    raw_users = tm.get_all_users()
    users = [{"id": u[0], "name": u[1], "role": u[2], "last_login": u[3]} for u in raw_users]
    print("==== TASK-TRACK ====")
    for user in users:
        print(f"{user['id']}. {user['name']}")

    choice_str = input("Select your user number: ")
    valid, selected = is_valid_user_selection(choice_str, users)

    if not valid:
        print("That's not a valid user number. Please try again.")
        return

    print(f"Welcome, {selected['name']}!")

    if selected["role"] == "admin":
        show_admin_dashboard()
    else:
        tm.update_last_login(selected["id"], str(date.today()))
        show_reminders(selected["id"])
        show_main_menu(selected["id"])


def show_main_menu(user_id):
    while True:
        print("==== TASK-TRACK ====")
        print("1. Add New Task/Assignment")
        print("2. View & Filter Tasks")
        print("3. Update Task Status")
        print("4. Edit or Delete Task")
        print("5. View Upcoming Deadlines")
        print("6. Exit")

        option = input("Enter your choice: ")

        if option == "1":
            title = input("Enter task title: ")
            course = input("Enter course/category: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            priority = input("Enter priority (High/Medium/Low): ")
            t = Task(title=title, course=course, due_date=due_date,
                     priority=priority, user_id=user_id, created_at=str(date.today()))
            tm.add_task(t)
            print("Task saved successfully!")
        elif option == "2":
            for t in tm.get_tasks_for_user(user_id):
                print(f"{t.id}. {t.title} - {t.course} - Due: {t.due_date} - {t.priority} - {t.status}")
        elif option == "3":
            task_id = int(input("Task ID: "))
            new_status = input("New status: 1) In Progress 2) Completed: ")
            tm.update_status(task_id, "In Progress" if new_status == "1" else "Completed")
            print("Status updated.")
        elif option == "4":
            task_id = int(input("Task ID: "))
            tm.delete_task(task_id)
            print("Task deleted.")
        elif option == "5":
            tasks = sorted(tm.get_tasks_for_user(user_id), key=lambda t: t.due_date)
            for t in tasks:
                print(f"{t.title} - {t.course} - Due: {t.due_date}")
        elif option == "6":
            print("Saving all data...")
            print("Goodbye!")
            break
        else:
            print("That's not a valid option. Please try again.")


show_login_screen()
