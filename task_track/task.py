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

    def to_dict(self):
        """Convert the Task object into a dictionary — used when saving to the database."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "course": self.course,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        """Rebuild a Task object from a dictionary — used when reading rows back from the database."""
        return cls(
            id=data.get("id"),
            user_id=data.get("user_id"),
            title=data.get("title"),
            course=data.get("course"),
            due_date=data.get("due_date"),
            priority=data.get("priority"),
            status=data.get("status"),
            created_at=data.get("created_at"),
        )

    def __repr__(self):
        return f"Task({self.title}, {self.course}, due {self.due_date}, {self.status})"

