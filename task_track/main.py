from datetime import date
from task_manager import TaskManager
from task import Task
from validators import is_valid_user_selection
from features import show_reminders

tm = TaskManager()


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


def show_main_menu():
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
            print("(stub) Adding a new task...")
        elif option == "2":
            print("(stub) Viewing & filtering tasks...")
        elif option == "3":
            print("(stub) Updating task status...")
        elif option == "4":
            print("(stub) Editing or deleting a task...")
        elif option == "5":
            print("(stub) Viewing upcoming deadlines...")
        elif option == "6":
            print("Saving all data...")
            print("Goodbye!")
            break
        else:
            print("That's not a valid option. Please try again.")


def show_login_screen():
    users = get_all_users()
    print("==== TASK-TRACK ====")
    for user in users:
        print(f"{user['id']}. {user['name']}")

    try:
        choice = int(input("Select your user number: "))
    except ValueError:
        print("Please enter a valid user number.")
        return

    selected_user = None
    for user in users:
        if user["id"] == choice:
            selected_user = user

    if selected_user is None:
        print("That's not a valid user number. Please try again.")
        return

    print(f"Welcome, {selected_user['name']}!")

    if selected_user["role"] == "admin":
        show_admin_dashboard()
    else:
        update_last_login(selected_user["id"])
        show_reminders()
        show_main_menu()


show_login_screen()
