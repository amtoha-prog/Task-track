"""
Integration test for TaskTrack.
Run with: python3 test_integration.py

This does NOT touch the real tasks.db — it uses a separate test database
so running this never wipes or messes with anyone's local data.
"""

import os
from task import Task
from task_manager import TaskManager
from validators import (
    is_valid_date, is_valid_priority, normalize_priority,
    is_valid_status, normalize_status, is_valid_user_selection, is_valid_task_id,
)
from features import get_reminder_summary, get_overdue_tasks, sort_by_due_date

TEST_DB = "test_integration.db"


def cleanup():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_user_creation_and_login():
    manager = TaskManager(TEST_DB)
    manager.add_user("Test Student", "student")
    manager.add_user("Test Admin", "admin")
    users = manager.get_all_users()
    assert len(users) == 2, "Expected 2 users after adding 2"

    is_valid, user = is_valid_user_selection("1", users)
    assert is_valid and user["name"] == "Test Student", "Valid login should succeed"

    is_valid, user = is_valid_user_selection("99", users)
    assert not is_valid, "Invalid user ID should fail"

    print("PASS: user creation and login validation")


def test_task_crud_is_scoped_to_user():
    manager = TaskManager(TEST_DB)
    users = manager.get_all_users()
    student_id = users[0]["id"]

    t = Task(title="Integration test task", course="TEST101",
             due_date="2026-08-01", priority="High", user_id=student_id)
    manager.add_task(t)

    tasks = manager.get_tasks_for_user(student_id)
    assert len(tasks) == 1, "Student should have exactly 1 task"
    assert tasks[0].user_id == student_id, "Task must be scoped to the right user"

    other_user_tasks = manager.get_tasks_for_user(9999)
    assert len(other_user_tasks) == 0, "A different/nonexistent user must see no tasks"

    manager.update_status(tasks[0].id, "Completed", student_id)
    updated = manager.get_tasks_for_user(student_id)
    assert updated[0].status == "Completed", "Status update should persist"

    manager.delete_task(tasks[0].id, student_id)
    after_delete = manager.get_tasks_for_user(student_id)
    assert len(after_delete) == 0, "Task should be gone after delete"

    print("PASS: task CRUD is correctly scoped per user")


def test_validators_reject_bad_input():
    assert is_valid_date("2026-08-01") is True
    assert is_valid_date("not-a-date") is False
    assert is_valid_priority("high") is True
    assert is_valid_priority("urgent") is False
    assert normalize_priority("high") == "High"
    assert is_valid_status("completed") is True
    assert is_valid_status("done") is False
    print("PASS: validators correctly accept/reject input")


def test_reminders_and_overdue_logic():
    manager = TaskManager(TEST_DB)
    users = manager.get_all_users()
    student_id = users[0]["id"]

    overdue_task = Task(title="Overdue task", course="TEST101",
                         due_date="2020-01-01", priority="High", user_id=student_id)
    manager.add_task(overdue_task)

    tasks = manager.get_tasks_for_user(student_id)
    overdue = get_overdue_tasks(tasks)
    assert len(overdue) == 1, "Should detect exactly 1 overdue task"

    summary = get_reminder_summary(tasks)
    assert "overdue" in summary and "upcoming" in summary, "Summary must have both keys"

    print("PASS: reminders and overdue detection work end-to-end")


def test_admin_can_see_all_students():
    manager = TaskManager(TEST_DB)
    users = manager.get_all_users()
    students = [u for u in users if u["role"] == "student"]
    assert len(students) >= 1, "There should be at least 1 student for admin to view"

    for student in students:
        tasks = manager.get_tasks_for_user(student["id"])
        _ = get_overdue_tasks(tasks)

    print("PASS: admin dashboard data path works for all students")


if __name__ == "__main__":
    cleanup()
    test_user_creation_and_login()
    test_task_crud_is_scoped_to_user()
    test_validators_reject_bad_input()
    test_reminders_and_overdue_logic()
    test_admin_can_see_all_students()
    cleanup()
    print("\nALL INTEGRATION TESTS PASSED")
