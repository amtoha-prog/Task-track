class Task:
    def __init__(self, title, course, due_date, priority, status="Pending",
                 id=None, user_id=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.course = course
        self.due_date = due_date       # expected format: "YYYY-MM-DD"
        self.priority = priority       # "High" / "Medium" / "Low"
        self.status = status           # "Pending" / "In Progress" / "Completed"
        self.created_at = created_at

