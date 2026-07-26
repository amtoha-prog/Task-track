# TaskTrack

A multi-user task and assignment tracker built for college students, developed by **Group 21** for PLP-2.

TaskTrack helps students manage their academic workload in one place — adding, tracking, and prioritizing assignments — while giving admins a way to see which students are staying on top of their deadlines.

---

## Table of Contents

- [The Problem](#the-problem)
- [Our Solution](#our-solution)
- [Features](#features)
- [Database Design](#database-design)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Running the Tests](#running-the-tests)
- [Why SQLite Instead of MySQL](#why-sqlite-instead-of-mysql)
- [Team & Contributions](#team--contributions)
- [Challenges & How We Solved Them](#challenges--how-we-solved-them)
- [Future Improvements](#future-improvements)

---

## The Problem

College students juggle multiple courses, deadlines, and personal responsibilities at once. When tasks aren't tracked in one place, it's easy for something to slip through the cracks — a missed assignment, a deadline nobody reminded you about.

Existing tools like Canvas do send reminders, but they're passive — a student has to actively check a menu, and there's no way for an advisor to tell whether a student has actually seen or acted on that reminder. TaskTrack addresses this specific gap: **active, automatic reminders**, and an **admin view** that shows whether students are actually engaging with them.

## Our Solution

TaskTrack is a terminal-based, menu-driven Python application that gives students a simple, centralized way to manage their academic workload — create, categorize, prioritize, and track tasks from start to finish.

- **Organize** — add tasks with a title, course, due date, and priority.
- **Track** — move each task through Pending → In Progress → Completed.
- **Focus** — automatic reminders on login surface anything overdue or due soon, with no need to dig through a menu.
- **Persist** — a local SQLite database keeps everything saved between sessions.

An admin account can also log in to see every student's last login time, pending task count, and overdue task count at a glance — giving visibility into student engagement that a standard LMS reminder system doesn't provide.

## Features

| Feature | Description |
|---|---|
| Login & profile selection | Pick your account from a numbered list on startup — supports multiple students plus an admin. |
| Automatic reminders | Shown immediately after login: anything overdue, and anything due within 2 days. |
| Add task/assignment | Enter a title, course, due date, and priority — validated before saving. |
| View & filter tasks | See all your tasks, or narrow by status, course, or due date. |
| Update task status | Move a task between Pending, In Progress, and Completed. |
| Edit or delete task | Correct a mistake, or remove a task no longer needed. |
| View upcoming deadlines | Tasks due soonest, sorted to the top, separate from the automatic reminder window. |
| Admin dashboard | Every student's last login, pending count, and overdue count, at a glance. |

All user input — dates, priorities, statuses, menu choices, and login/task selections — is validated before it reaches the database, so invalid input is caught and re-prompted rather than crashing the app.

## Database Design

TaskTrack uses two linked SQLite tables. Every task belongs to exactly one user via a foreign key, which is what makes multi-user support and the admin dashboard possible.

**`users`**

| Column | Type | Notes |
|---|---|---|
| `id` | INTEGER PRIMARY KEY | Auto-incrementing user ID |
| `name` | TEXT | Student's display name, shown on login and the dashboard |
| `role` | TEXT | `"student"` or `"admin"` — controls where login routes to |
| `last_login` | TEXT | Updated automatically every time this user logs in |

**`tasks`**

| Column | Type | Notes |
|---|---|---|
| `id` | INTEGER PRIMARY KEY | Auto-incrementing task ID |
| `user_id` | INTEGER (FK → `users.id`) | Links this task to its owner |
| `title` | TEXT | Task/assignment title |
| `course` | TEXT | Course or category |
| `due_date` | TEXT | Stored as `YYYY-MM-DD` |
| `priority` | TEXT | High / Medium / Low |
| `status` | TEXT | Pending / In Progress / Completed |
| `created_at` | TEXT | Date the task was added |

Data flows one way through the app: input is collected and validated in `main.py`, written to SQLite via `task_manager.py`, and read back out — filtered, sorted, and summarized — through `features.py` before being displayed to the student or admin.

## Project Structure

```
task_track/
├── main.py               — menu loop, login screen, admin dashboard (entry point)
├── task.py                — Task class (OOP model)
├── task_manager.py        — TaskManager class: all SQLite logic
├── validators.py          — input validation (dates, priority, status, login, task IDs)
├── features.py             — filter, sort, and reminder/overdue logic
├── test_integration.py    — end-to-end tests across all modules
├── tasks.db               — auto-created on first run (not committed to Git)
└── README.md
```

`main.py` is the single entry point — running it is all that's needed to start the application.

## Getting Started

**Requirements:** Python 3.8 or later. No external packages — everything runs on Python's standard library (`sqlite3`, `datetime`).

1. Clone the repository:
   ```bash
   git clone https://github.com/amtoha-prog/Task-track
   cd task-track/task_track
   ```
2. Run the app:
   ```bash
   python3 main.py
   ```
3. On first run, TaskTrack automatically seeds 3 demo student accounts and 1 admin account with sample tasks, so there's immediately something to interact with.
4. Select a user number to log in as a student, or the admin account to view the dashboard.

No server, no database installation, and no configuration steps are required — cloning and running `python3 main.py` is the entire setup.

## Running the Tests

```bash
python3 test_integration.py
```

This runs a full integration suite against a separate test database (never touching your local `tasks.db`), covering:

- User creation and login validation
- Task CRUD correctly scoped per user
- Input validation for dates, priorities, and statuses
- Reminder and overdue detection logic
- The admin dashboard's data path across multiple students

## Why SQLite Instead of MySQL

TaskTrack is an offline, single-device application by design. MySQL requires a running server process on every machine, which adds setup overhead across a 6-person team on a short timeline and doesn't match this project's architecture. SQLite ships with Python's standard library, requires no installation or server, and fully satisfies the project's SQL database requirement — including role-based, multi-user data through the `users`/`tasks` schema above.

## Team & Contributions

Each member owned one focused module, based on the work they carried forward from PLP-1. Everyone worked on their own Git branch and merged into `main` via pull request, so individual commit history is visible and attributable.

| Member | Responsibility | File(s) Owned |
|---|---|---|
| Tsungirirai Machingura | Task class (OOP model) | `task.py` |
| Tapiwanashe Kambare | Database layer — SQLite connection, schema, and queries | `task_manager.py` |
| Alissa Bonaventura Mtoha | Menu / UI layer — login screen, main menu, admin routing | `main.py` |
| Aliane Irumva | Input validation | `validators.py` |
| Regan Ayiecho | Filtering, sorting, and reminder/overdue logic | `features.py` |
| Ikenwe Testimony | Integration, testing, and documentation | `test_integration.py`, README, admin dashboard polish |

## Challenges & How We Solved Them

| Challenge | How We Solved It |
|---|---|
| Choosing a database under a 4-day timeline | Switched from MySQL to SQLite — no server setup, ships with Python. |
| Adding multi-user support mid-project | Added a `users` table and a `user_id` foreign key rather than rebuilding the schema from scratch. |
| Keeping modules working before teammates finished theirs | Stubbed each other's functions with matching names and signatures, then swapped in the real implementations during integration. |
