def filter_by_status(tasks, status):
    return [task for task in tasks if task.status == status]

def filter_by_course(tasks, course):
    return [task for task in tasks if task.course == course]

def filter_by_due_date(tasks, due_date):
    return [task for task in tasks if task.due_date == due_date]
