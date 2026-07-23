def get_all_users():
    # TEMPORARY stub — Tapiwanashe's real version will query SQLite instead
    return [
        {"id": 1, "name": "Alissa", "role": "student"},
        {"id": 2, "name": "TK", "role": "student"},
        {"id": 3, "name": "Simeon", "role": "admin"}
    ]

def show_login_screen():
    users = get_all_users()
    print("==== TASK-TRACK ====")
    for user in users:
        print(f"{user['id']}. {user['name']}")

show_login_screen()