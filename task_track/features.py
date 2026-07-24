from datetime import datetime, date


def _parse_due_date(task):
    """Safely converts a task's due_date string into a date object.
    Returns None if the date is missing or badly formatted, instead of crashing."""
    try:
        return datetime.strptime(task.due_date, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def filter_by_status(tasks, status):
    """Returns only the tasks matching a given status
    (e.g. 'Pending', 'In Progress', 'Completed')."""
    return [t for t in tasks if t.status.lower() == status.lower()]


def filter_by_course(tasks, course):
    """Returns only the tasks matching a given course/category."""
    return [t for t in tasks if t.course.lower() == course.lower()]


def filter_by_priority(tasks, priority):
    """Returns only the tasks matching a given priority."""
    return [t for t in tasks if t.priority.lower() == priority.lower()]


def filter_by_due_date(tasks, due_date):
    """Returns only the tasks matching an exact due date (YYYY-MM-DD).
    Used by the 'View & Filter Tasks -> Due date' menu option."""
    return [t for t in tasks if t.due_date == due_date]


def sort_by_due_date(tasks, reverse=False):
    """Returns tasks sorted by nearest due date first.
    Tasks with a missing/invalid due date are pushed to the end
    rather than crashing the sort."""
    def sort_key(t):
        d = _parse_due_date(t)
        return d if d else date.max

    return sorted(tasks, key=sort_key, reverse=reverse)


def sort_by_priority(tasks):
    """Returns tasks sorted High -> Medium -> Low."""
    order = {"High": 0, "Medium": 1, "Low": 2}
    return sorted(tasks, key=lambda t: order.get(t.priority, 99))


def get_overdue_tasks(tasks, today=None):
    """Returns tasks whose due date has already passed and are not completed."""
    today = today or date.today()
    overdue = []
    for t in tasks:
        if t.status == "Completed":
            continue
        due = _parse_due_date(t)
        if due and due < today:
            overdue.append(t)
    return overdue


def get_upcoming_deadlines(tasks, days_ahead=2, today=None):
    """Returns tasks due within the next `days_ahead` days (inclusive),
    excluding completed and overdue tasks. This is the core function
    that powers the automatic reminders shown right after login."""
    today = today or date.today()
    upcoming = []
    for t in tasks:
        if t.status == "Completed":
            continue
        due = _parse_due_date(t)
        if due is None:
            continue
        days_left = (due - today).days
        if 0 <= days_left <= days_ahead:
            upcoming.append(t)
    return sort_by_due_date(upcoming)


def get_reminder_summary(tasks, days_ahead=2, today=None):
    """Combines overdue + upcoming into the two lists main.py needs
    to build the reminders block shown after login."""
    return {
        "overdue": get_overdue_tasks(tasks, today=today),
        "upcoming": get_upcoming_deadlines(tasks, days_ahead=days_ahead, today=today),
    }
