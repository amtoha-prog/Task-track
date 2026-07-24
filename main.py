def get_all_users():
    # TEMPORARY — Tapiwanashe's real version will query SQLite instead
    return [
        {"id": 1, "name": "Alissa", "role": "student"},
        {"id": 2, "name": "TK", "role": "student"},
        {"id": 3, "name": "Simeon", "role": "admin"}
    ]


def update_last_login(user_id):
    # TEMPORARY — Replcae it with Tapiwanashe's real version
    #  will update the database
    print(f"(stub) Updating last login for user {user_id}")


def show_reminders():
    # TEMPORARY — Replace it with Regan's real version will check due dates
    print("(stub) Checking for upcoming deadlines...")


def show_admin_dashboard():
    # TEMPORARY — Replace it with Tess's real version will show user stats
    print("(stub) Showing admin dashboard...")


# Creating a main task menu to show options
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
            # TEMPORARY — will call the real "add task"
            #  function once it's ready
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
            break  # exits the while loop, ending the menu
        else:
            print("That's not a valid option. Please try again.")


# Printing the login in screen
def show_login_screen():
    users = get_all_users()
    print("==== TASK-TRACK ====")
    for user in users:
        print(f"{user['id']}. {user['name']}")

# Ask the user to pick which account they are by number
    try:
        choice = int(input("Select your user number: "))
    except ValueError:
        print("Please enter a valid user number.")
        return

    # To search the users list for the one whose id matches the choice
    selected_user = None
    for user in users:
        if user["id"] == choice:
            selected_user = user

    # TEMPORARY - swap with Aliane's validators.py once it's ready
    if selected_user is None:
        print("That's not a valid user number. Please try again.")
        return

# Confirm to the user which account was selected
    print(f"Welcome, {selected_user['name']}!")

# Route the user based on their role: admin goes straight to their dashboard,
# while students go through login tracking, reminders then the main task menu
    if selected_user["role"] == "admin":
        show_admin_dashboard()
    else:
        update_last_login(selected_user["id"])
        show_reminders()
        show_main_menu()


show_login_screen()



