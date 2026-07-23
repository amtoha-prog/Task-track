def filter_by_status(tasks, status):
    return [task for task in tasks if task.status == status]
