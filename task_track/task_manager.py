import sqlite3
from task import Task

class TaskManager:
    def __init__(self, db_path="tasks.db"):
        self.db_path = db_path
        self._create_tables()

    def _get_connection(self):
<<<<<<< HEAD
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # rows behave like dicts (row["id"], row["name"], etc.)
        return conn
=======
        return sqlite3.connect(self.db_path)
>>>>>>> 4181ab57c82ec49ced4741dd6d4efd13d3d69f91

    def _create_tables(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                last_login TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                course TEXT,
                due_date TEXT,
                priority TEXT,
                status TEXT DEFAULT 'Pending',
                created_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        conn.commit()
        conn.close()

    # ---------- USER METHODS ----------

    def add_user(self, name, role="student"):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, role) VALUES (?, ?)", (name, role))
        conn.commit()
        conn.close()

    def get_all_users(self):
<<<<<<< HEAD
        """Returns a list of dicts: [{'id':1,'name':...,'role':...,'last_login':...}, ...]"""
=======
>>>>>>> 4181ab57c82ec49ced4741dd6d4efd13d3d69f91
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, role, last_login FROM users")
        rows = cursor.fetchall()
        conn.close()
<<<<<<< HEAD
        return [dict(row) for row in rows]

    def get_user_by_id(self, user_id):
        """Returns a dict, or None if not found."""
=======
        return rows

    def get_user_by_id(self, user_id):
>>>>>>> 4181ab57c82ec49ced4741dd6d4efd13d3d69f91
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, role, last_login FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
<<<<<<< HEAD
        return dict(row) if row else None
=======
        return row
>>>>>>> 4181ab57c82ec49ced4741dd6d4efd13d3d69f91

    def update_last_login(self, user_id, timestamp):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (timestamp, user_id))
        conn.commit()
        conn.close()

    # ---------- TASK METHODS ----------

    def add_task(self, task: Task):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (user_id, title, course, due_date, priority, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (task.user_id, task.title, task.course, task.due_date,
              task.priority, task.status, task.created_at))
        conn.commit()
        conn.close()

    def get_tasks_for_user(self, user_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()
<<<<<<< HEAD
        return [Task.from_dict(dict(row)) for row in rows]

    def update_status(self, task_id, new_status, user_id):
        """user_id is required so a student can only update THEIR OWN tasks."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET status = ? WHERE id = ? AND user_id = ?",
            (new_status, task_id, user_id)
        )
        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()
        return updated

    def delete_task(self, task_id, user_id):
        """user_id is required so a student can only delete THEIR OWN tasks."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, user_id)
        )
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted
=======
        columns = ["id", "user_id", "title", "course", "due_date", "priority", "status", "created_at"]
        return [Task.from_dict(dict(zip(columns, row))) for row in rows]

    def update_status(self, task_id, new_status):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
        conn.commit()
        conn.close()

    def delete_task(self, task_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
>>>>>>> 4181ab57c82ec49ced4741dd6d4efd13d3d69f91


if __name__ == "__main__":
    tm = TaskManager("test_tasks.db")
    tm.add_user("Student A", "student")
    tm.add_user("Admin", "admin")
    print(tm.get_all_users())

    from datetime import date
    t = Task(title="Finish essay", course="ENG101", due_date="2026-07-30",
              priority="High", user_id=1, created_at=str(date.today()))
    tm.add_task(t)
<<<<<<< HEAD
    print(tm.get_tasks_for_user(1))
=======
    print(tm.get_tasks_for_user(1))
>>>>>>> 4181ab57c82ec49ced4741dd6d4efd13d3d69f91
