# enterprise_task_system/app/utils/message_formatter.py

from app.models.task import Task
from app.models.user import User
from app.models.work_id import WorkID

def format_task_creation_message(
    *,
    task: Task,
    user: User,
    work_id: WorkID
) -> str:
    """
    Formats a message to be sent upon task creation.

    The message is structured to resemble an email notification, providing
    clear and concise information about the newly created task.

    Args:
        task: The task that was created.
        user: The user who created the task.
        work_id: The unique work ID assigned to the task.

    Returns:
        A formatted string representing the message content.
    """
    message = f"""
    From: System Notification <noreply@enterprise.com>
    To: {user.email}
    Subject: New Task Created: {task.title}

    Hello {user.username},

    A new task has been created and assigned to you.

    Details:
    -------------------
    Work ID: {work_id.work_id_str}
    Task ID: {task.id}
    Title: {task.title}
    Description: {task.description or 'N/A'}
    Status: {task.status}
    Created At: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}
    -------------------

    You can view the task details in the system.

    Thank you,
    The Enterprise Task System
    """
    return message.strip()
