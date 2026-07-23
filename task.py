class Task:
    def __init__(self, title, course, due_date, priority, status="Pending", id=None):
        self.id = id
        self.title = title
        self.course = course
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "course": self.course,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status
        }

    def __repr__(self):
        return f"Task({self.title}, {self.course}, {self.due_date}, {self.priority}, {self.status})"
