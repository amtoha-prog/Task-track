from datetime import datetime

VALID_PRIORITIES = ("High", "Medium", "Low")
VALID_STATUSES = ("Pending", "In Progress", "Completed")


def is_valid_date(date_str):
    """Checks the date is a real calendar date in YYYY-MM-DD format.
    Returns True/False — does not crash on garbage input."""
    if not date_str:
        return False
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_valid_priority(priority):
    """Checks priority is one of High / Medium / Low (case-insensitive)."""
    if not priority:
        return False
    return priority.strip().capitalize() in VALID_PRIORITIES


def normalize_priority(priority):
    """Returns the properly-capitalized priority string, e.g. 'high' -> 'High'.
    Call is_valid_priority() first to make sure it's actually valid."""
    return priority.strip().capitalize()


def is_valid_status(status):
    """Checks status is one of Pending / In Progress / Completed (case-insensitive)."""
    if not status:
        return False
    return status.strip().title() in VALID_STATUSES


def normalize_status(status):
    return status.strip().title()


def is_valid_menu_choice(choice, valid_options):
    """Checks the user's menu input is one of the allowed option strings.
    valid_options is something like ["1", "2", "3", "4", "5", "6"]."""
    return choice in valid_options


def is_valid_user_selection(choice_str, users):
    """Checks a login screen selection is a real, existing user ID.
    Returns (True, user_dict) if valid, (False, None) if not —
    so the caller never has to guess whether choice_str was even a number."""
    if not choice_str.isdigit():
        return False, None

    choice_id = int(choice_str)
    for user in users:
        if user["id"] == choice_id:
            return True, user
    return False, None


def is_valid_task_id(id_str, tasks):
    """Checks a task ID entered by the user actually exists in their task list.
    Returns (True, task_id) or (False, None)."""
    if not id_str.isdigit():
        return False, None

    task_id = int(id_str)
    existing_ids = [t.id for t in tasks]
    if task_id in existing_ids:
        return True, task_id
    return False, None


if __name__ == "__main__":
    # Quick local sanity checks — run with: python3 validators.py
    print(is_valid_date("2026-07-30"))   # True
    print(is_valid_date("2026-13-40"))   # False (not a real date)
    print(is_valid_date("30/07/2026"))   # False (wrong format)
    print(is_valid_date(""))             # False

    print(is_valid_priority("High"))     # True
    print(is_valid_priority("high"))     # True
    print(is_valid_priority("Urgent"))   # False

    print(is_valid_status("in progress"))  # True
    print(is_valid_status("Done"))          # False

    print(is_valid_menu_choice("3", ["1", "2", "3", "4", "5", "6"]))  # True
    print(is_valid_menu_choice("9", ["1", "2", "3", "4", "5", "6"]))  # False

    sample_users = [{"id": 1, "name": "Alissa"}, {"id": 2, "name": "TK"}]
    print(is_valid_user_selection("1", sample_users))   # (True, {...Alissa})
    print(is_valid_user_selection("99", sample_users))  # (False, None)
    print(is_valid_user_selection("abc", sample_users)) # (False, None)
