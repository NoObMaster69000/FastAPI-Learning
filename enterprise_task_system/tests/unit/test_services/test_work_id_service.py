# enterprise_task_system/tests/unit/test_services/test_work_id_service.py

from app.services.work_id_service import work_id_service
from app.models.user import User
from app.models.task import Task

def test_generate_and_assign_work_id(db_session):
    """
    Test that the WorkIDService can generate and assign a work ID to a task.
    """
    # Create a sample user
    user = User(username="testuser", email="test@example.com", hashed_password="password")
    db_session.add(user)
    db_session.commit()

    # Create a sample task
    task = Task(title="Test Task", description="Test Description", owner_id=user.id)
    db_session.add(task)
    db_session.commit()

    work_id = work_id_service.generate_and_assign_work_id(db_session, task=task)

    assert work_id is not None
    assert work_id.task_id == task.id
    assert work_id.work_id_str is not None
    assert work_id.work_id_str.startswith("TSK-")
