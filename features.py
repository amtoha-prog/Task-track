def filter_by_status(tasks, status):
    return [task for task in tasks if task.status == status]

def filter_by_course(tasks, course):
    return [task for task in tasks if task.course == course]

def filter_by_due_date(tasks, due_date):
    return [task for task in tasks if task.due_date == due_date]

def sort_by_due_date(tasks):
    return sorted(tasks, key=lambda task: task.due_date)

def get_upcoming_deadlines(tasks):
    not_completed = [task for task in tasks if task.status != "Completed"]
    return sort_by_due_date(not_completed)
