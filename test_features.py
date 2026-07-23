from task import Task

mock_tasks = [
    Task("Essay Draft", "English", "2026-07-25", "High", "Pending", id=1),
    Task("Data Structures Assignment 3", "BSE 1102", "2026-07-24", "High", "Pending", id=2),
    Task("Peer Learning Reflection", "BSE 1090", "2026-07-26", "Medium", "In Progress", id=3),
    Task("Math Problem Set", "MATH 101", "2026-07-23", "Low", "Completed", id=4),
    Task("Group Project Report", "BSE 1102", "2026-07-30", "High", "Pending", id=5),
]

for t in mock_tasks:
    print(t)

from features import filter_by_status
print("\n-- Filter by status: Pending --")
for t in filter_by_status(mock_tasks, "Pending"):
    print(t)

from features import filter_by_course
print("\n-- Filter by course: BSE 1102 --")
for t in filter_by_course(mock_tasks, "BSE 1102"):
    print(t)

from features import filter_by_due_date
print("\n-- Filter by due date: 2026-07-24 --")
for t in filter_by_due_date(mock_tasks, "2026-07-24"):
    print(t)

from features import sort_by_due_date
print("\n-- Sort by due date (soonest first) --")
for t in sort_by_due_date(mock_tasks):
    print(t)
