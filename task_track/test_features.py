from datetime import date
from task import Task
from features import (
    filter_by_status,
    filter_by_course,
    filter_by_priority,
    filter_by_due_date,
    sort_by_due_date,
    sort_by_priority,
    get_overdue_tasks,
    get_upcoming_deadlines,
    get_reminder_summary,
)

# "Today" fixed for repeatable test results, not the real system date
TODAY = date(2026, 7, 24)

mock_tasks = [
    Task(title="Essay Draft", course="English", due_date="2026-07-25",
         priority="High", status="Pending", id=1, user_id=1),
    Task(title="Data Structures Assignment 3", course="BSE 1102", due_date="2026-07-24",
         priority="High", status="Pending", id=2, user_id=1),
    Task(title="Peer Learning Reflection", course="BSE 1090", due_date="2026-07-26",
         priority="Medium", status="In Progress", id=3, user_id=1),
    Task(title="Math Problem Set", course="MATH 101", due_date="2026-07-23",
         priority="Low", status="Completed", id=4, user_id=1),
    Task(title="Group Project Report", course="BSE 1102", due_date="2026-07-30",
         priority="High", status="Pending", id=5, user_id=1),
    Task(title="Old Reading Response", course="English", due_date="2026-07-20",
         priority="Medium", status="Pending", id=6, user_id=1),  # overdue
]

print("-- filter_by_status: Pending --")
for t in filter_by_status(mock_tasks, "Pending"):
    print(" ", t)

print("\n-- filter_by_course: BSE 1102 --")
for t in filter_by_course(mock_tasks, "BSE 1102"):
    print(" ", t)

print("\n-- filter_by_priority: High --")
for t in filter_by_priority(mock_tasks, "High"):
    print(" ", t)

print("\n-- filter_by_due_date: 2026-07-24 --")
for t in filter_by_due_date(mock_tasks, "2026-07-24"):
    print(" ", t)

print("\n-- sort_by_due_date --")
for t in sort_by_due_date(mock_tasks):
    print(" ", t)

print("\n-- sort_by_priority --")
for t in sort_by_priority(mock_tasks):
    print(" ", t)

print("\n-- get_overdue_tasks (today = 2026-07-24) --")
for t in get_overdue_tasks(mock_tasks, today=TODAY):
    print(" ", t)

print("\n-- get_upcoming_deadlines (2 days, today = 2026-07-24) --")
for t in get_upcoming_deadlines(mock_tasks, days_ahead=2, today=TODAY):
    print(" ", t)

print("\n-- get_reminder_summary --")
summary = get_reminder_summary(mock_tasks, today=TODAY)
print("Overdue:", summary["overdue"])
print("Upcoming:", summary["upcoming"])
