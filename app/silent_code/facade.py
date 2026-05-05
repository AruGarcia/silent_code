from app.silent_code.models import Task

STATUS_ALL = "all"
STATUS_PENDING = "pending"
STATUS_COMPLETED = "completed"
DEFAULT_STATUS_FILTER = STATUS_ALL


def tasks_for_user(user):
    return Task.objects.filter(user=user)


def list_tasks_for_user(user, status_filter=DEFAULT_STATUS_FILTER):
    return filter_tasks_by_status(tasks_for_user(user), status_filter)


def filter_tasks_by_status(queryset, status_filter):
    if status_filter == STATUS_PENDING:
        return queryset.filter(is_completed=False)
    if status_filter == STATUS_COMPLETED:
        return queryset.filter(is_completed=True)
    return queryset


def task_counts_for_user(user):
    user_tasks = tasks_for_user(user)
    return {
        STATUS_ALL: user_tasks.count(),
        STATUS_PENDING: user_tasks.filter(is_completed=False).count(),
        STATUS_COMPLETED: user_tasks.filter(is_completed=True).count(),
    }


def create_task(*, user, title, description=""):
    return Task.objects.create(
        user=user,
        title=title,
        description=description,
    )


def update_task(*, task, title, description=""):
    task.title = title
    task.description = description
    task.save(update_fields=["title", "description", "updated_at"])
    return task


def toggle_task_completion(*, task):
    task.is_completed = not task.is_completed
    task.save(update_fields=["is_completed", "updated_at"])
    return task


def delete_task(*, task):
    task.delete()
