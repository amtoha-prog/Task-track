from datetime import datetime, timedelta


def _parse_due_datetime(task):
    """Safely converts a task's due_date string into a full datetime object
    (date + time). Supports both the new "YYYY-MM-DD HH:MM" format and the
    older date-only "YYYY-MM-DD" format (treated as 23:59 that day, so old
    tasks don't break). Returns None if the value is missing or malformed,
    instead of crashing."""
    if not task.due_date:
        return None
    try:
        return datetime.strptime(task.due_date, "%Y-%m-%d %H:%M")
    except (ValueError, TypeError):
        pass
    try:
        return datetime.strptime(task.due_date, "%Y-%m-%d").replace(hour=23, minute=59)
    except (ValueError, TypeError):
        return None


def parse_due_datetime(task):
    """Public wrapper around the internal due-date parser, for use by
    main.py when displaying a task's due date/time and countdown."""
    return _parse_due_datetime(task)


def format_time_remaining(due_dt, now=None):
    """Turns a due datetime into a short human-readable string like
    '2 hours left', '3 days left', or 'Overdue by 5 hours'."""
    now = now or datetime.now()
    delta = due_dt - now
    seconds = delta.total_seconds()

    if seconds < 0:
        overdue_seconds = -seconds
        if overdue_seconds < 3600:
            minutes = max(1, int(overdue_seconds // 60))
            return f"Overdue by {minutes} minute{'s' if minutes != 1 else ''}"
        if overdue_seconds < 86400:
            hours = int(overdue_seconds // 3600)
            return f"Overdue by {hours} hour{'s' if hours != 1 else ''}"
        days = int(overdue_seconds // 86400)
        return f"Overdue by {days} day{'s' if days != 1 else ''}"

    if seconds < 3600:
        minutes = max(1, int(seconds // 60))
        return f"{minutes} minute{'s' if minutes != 1 else ''} left"
    if seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} left"
    days = int(seconds // 86400)
    return f"{days} day{'s' if days != 1 else ''} left"


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
    """Returns only the tasks matching an exact due_date string
    (e.g. "2026-07-31 23:59"). Used by the 'View & Filter Tasks -> Due date'
    menu option."""
    return [t for t in tasks if t.due_date == due_date]


def sort_by_due_date(tasks, reverse=False):
    """Returns tasks sorted by nearest due date+time first.
    Tasks with a missing/invalid due date are pushed to the end
    rather than crashing the sort."""
    def sort_key(t):
        dt = _parse_due_datetime(t)
        return dt if dt else datetime.max

    return sorted(tasks, key=sort_key, reverse=reverse)


def sort_by_priority(tasks):
    """Returns tasks sorted High -> Medium -> Low."""
    order = {"High": 0, "Medium": 1, "Low": 2}
    return sorted(tasks, key=lambda t: order.get(t.priority, 99))


def get_overdue_tasks(tasks, now=None):
    """Returns tasks whose due date+time has already passed and are not completed."""
    now = now or datetime.now()
    overdue = []
    for t in tasks:
        if t.status == "Completed":
            continue
        due = _parse_due_datetime(t)
        if due and due < now:
            overdue.append(t)
    return overdue


def get_upcoming_deadlines(tasks, days_ahead=2, now=None):
    """Returns tasks due within the next `days_ahead` days (inclusive) from
    right now, excluding completed and overdue tasks. This is the core
    function that powers the automatic reminders shown right after login."""
    now = now or datetime.now()
    horizon = now + timedelta(days=days_ahead)
    upcoming = []
    for t in tasks:
        if t.status == "Completed":
            continue
        due = _parse_due_datetime(t)
        if due is None:
            continue
        if now <= due <= horizon:
            upcoming.append(t)
    return sort_by_due_date(upcoming)


def get_reminder_summary(tasks, days_ahead=2, now=None):
    """Combines overdue + upcoming into the two lists main.py needs
    to build the reminders block shown after login. Each task in both
    lists can be paired with format_time_remaining(_parse_due_datetime(t))
    to show a countdown like '2 hours left' or 'Overdue by 3 days'."""
    return {
        "overdue": get_overdue_tasks(tasks, now=now),
        "upcoming": get_upcoming_deadlines(tasks, days_ahead=days_ahead, now=now),
    }
