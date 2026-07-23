def get_all_users():
    # TEMPORARY — Tapiwanashe's real version will query SQLite instead
    return [
        {"id": 1, "name": "Alissa", "role": "student"},
        {"id": 2, "name": "TK", "role": "student"},
        {"id": 3, "name": "Simeon", "role": "admin"}
    ]

# Printing the login screen
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





show_login_screen()





