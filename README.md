# Task-Track

A simple command-line task manager built for ALU coursework. Users log in, then either view an admin dashboard (admins) or manage their own tasks (students).

## Features

- Login screen - select your user from a list pulled from the SQLite database.
- Admin dashboard - shows each student's pending and overdue task counts.
- Student main menu:
  1. Add a new task/assignment
  2. View & filter tasks
  3. Update task status
  4. Edit or delete a task
  5. View upcoming deadlines
  6. Exit
- Reminders - students see overdue and upcoming tasks right after login.

## Project structure

- task_track/main.py - Entry point, login, dashboard, and menu flow
- task_track/task_manager.py - TaskManager class, all SQLite database access
- task_track/task.py - Task data model
- task_track/validators.py - Input validation helpers
- task_track/features.py - Task filtering, sorting, and reminder logic
- task_track/test_features.py - Tests for features.py

## Running it

From inside task_track/:

    python3 main.py

The database (tasks.db) is created Automatically on first run and is not tracked in git. To test locally, seed a few users first:

    python3 -c "
    from task_manager import TaskManager
    tm = TaskManager()
    tm.add_user('Alissa', 'student')
    tm.add_user('TK', 'student')
    tm.add_user('Simeon', 'admin')
    "

## Known gaps

- show_reminders() is not yet implemented in features.py. main.py currently uses a temporary local wrapper built on get_reminder_summary().
