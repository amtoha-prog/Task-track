from datetime import date
from task_manager import TaskManager
from task import Task
from validators import (
    is_valid_user_selection,
    is_valid_task_id,
    is_valid_date,
    is_valid_priority,
    normalize_priority,
)
from features import get_reminder_summary, get_overdue_tasks, get_upcoming_deadlines

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
        overdue_task = Task(title="Overdue lab report", course="BIO110",
                             due_date="2026-07-20", priority="High",
                             user_id=1, created_at=str(date.today()))
        tm.add_task(overdue_task)


def show_admin_dashboard():
    while True:
        users = tm.get_all_users()
        print("\n" + "=" * 40)
        print("        ADMIN DASHBOARD")
        print("=" * 40)
        for user in users:
            if user["role"] == "admin":
                continue
            tasks = tm.get_tasks_for_user(user["id"])
            pending = len([t for t in tasks if t.status != "Completed"])
            overdue = len(get_overdue_tasks(tasks))
            print(f"{user['name']} | Last login: {user['last_login']} | Pending: {pending} | Overdue: {overdue}")
        print("=" * 40)
        print("1. Refresh dashboard")
        print("2. Exit")
        choice = input("Enter your choice: ")
        if choice == "2":
            print("\nSaving all data...")
            print("Goodbye!")
            break

def show_reminders(user_id):
    tasks = tm.get_tasks_for_user(user_id)
    summary = get_reminder_summary(tasks)
    print("\n" + "=" * 40)
    print("        REMINDERS")
    print("=" * 40)
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
    print("=" * 40 + "\n")


def show_login_screen():
    users = tm.get_all_users()
    print()
    print("=" * 40)
    print("        WELCOME TO TASK-TRACK")
    print("   Your college task & assignment tracker")
    print("=" * 40)
    print("\nPlease log in to your profile:\n")
    for user in users:
        print(f"  {user['id']}. {user['name']}")
    print()

    choice_str = input("Enter the number next to your name to log in: ")
    valid, selected = is_valid_user_selection(choice_str, users)

    if not valid:
        print("\nHmm, that's not a valid profile number. Please try again.\n")
        return

    print(f"\nWelcome back, {selected['name']}! Logging you in...\n")

    if selected["role"] == "admin":
        show_admin_dashboard()
    else:
        tm.update_last_login(selected["id"], str(date.today()))
        show_reminders(selected["id"])
        show_main_menu(selected["id"])

def show_main_menu(user_id):
    while True:
        print("=" * 40)
        print("           MAIN MENU")
        print("=" * 40)
        print("1. Add New Task/Assignment")
        print("2. View & Filter Tasks")
        print("3. Update Task Status")
        print("4. Edit or Delete Task")
        print("5. View Upcoming Deadlines")
        print("6. Exit")
        print("=" * 40)

        option = input("Enter your choice: ")
        print()

        if option == "1":
            title = input("Enter task title: ")
            course = input("Enter course/category: ")

            due_date = input("Enter due date (YYYY-MM-DD): ")
            if not is_valid_date(due_date):
                print("That's not a valid date. Task not saved.")
                continue

            priority = input("Enter priority (High/Medium/Low): ")
            if not is_valid_priority(priority):
                print("That's not a valid priority. Task not saved.")
                continue
            priority = normalize_priority(priority)

            t = Task(title=title, course=course, due_date=due_date,
                     priority=priority, user_id=user_id, created_at=str(date.today()))
            tm.add_task(t)
            print("Task saved successfully!")

        elif option == "2":
            for t in tm.get_tasks_for_user(user_id):
                print(f"{t.id}. {t.title} - {t.course} - Due: {t.due_date} - {t.priority} - {t.status}")

        elif option == "3":
            my_tasks = tm.get_tasks_for_user(user_id)
            task_id_str = input("Task ID: ")
            valid, task_id = is_valid_task_id(task_id_str, my_tasks)
            if not valid:
                print("That's not a valid task ID for your account.")
                continue

            new_status = input("New status: 1) In Progress 2) Completed: ")
            status_to_set = "In Progress" if new_status == "1" else "Completed"
            tm.update_status(task_id, status_to_set, user_id)
            print("Status updated.")

        elif option == "4":
            my_tasks = tm.get_tasks_for_user(user_id)
            task_id_str = input("Task ID: ")
            valid, task_id = is_valid_task_id(task_id_str, my_tasks)
            if not valid:
                print("That's not a valid task ID for your account.")
                continue

            action = input("1) Edit  2) Delete: ")

            if action == "1":
                current = tm.get_task_by_id(task_id, user_id)
                print(f"Editing '{current.title}' - press Enter to keep the current value.")

                new_title = input(f"Title [{current.title}]: ").strip() or current.title
                new_course = input(f"Course [{current.course}]: ").strip() or current.course

                new_due = input(f"Due date [{current.due_date}]: ").strip() or current.due_date
                if not is_valid_date(new_due):
                    print("That's not a valid date. Edit cancelled - nothing was changed.")
                    continue

                new_priority_raw = input(f"Priority [{current.priority}]: ").strip() or current.priority
                if not is_valid_priority(new_priority_raw):
                    print("That's not a valid priority. Edit cancelled - nothing was changed.")
                    continue
                new_priority = normalize_priority(new_priority_raw)

                tm.edit_task(task_id, user_id, new_title, new_course, new_due, new_priority)
                print("Task updated.")

            elif action == "2":
                target = tm.get_task_by_id(task_id, user_id)
                confirm = input(f"Delete '{target.title}'? Type 'yes' to confirm: ")
                if confirm.strip().lower() == "yes":
                    tm.delete_task(task_id, user_id)
                    print("Task deleted.")
                else:
                    print("Delete cancelled - nothing was changed.")

            else:
                print("That's not a valid option. Returning to menu.")

        elif option == "5":
            all_tasks = tm.get_tasks_for_user(user_id)
            upcoming = get_upcoming_deadlines(all_tasks, days_ahead=7)
            if not upcoming:
                print("Nothing due in the next 7 days.")
            for t in upcoming:
                print(f"{t.title} - {t.course} - Due: {t.due_date}")

        elif option == "6":
            print("Saving all data...")
            print("Goodbye!")
            break

        else:
            print("That's not a valid option. Please try again.")


if __name__ == "__main__":
 seed_users_if_needed()
 show_login_screen()
