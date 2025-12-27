# enterprise_task_system/tests/unit/test_utils/test_work_id_generator.py

from app.utils.work_id_generator import generate_work_id

def test_generate_work_id():
    """
    Test that the work ID generator returns a string in the correct format.
    """
    work_id = generate_work_id()

    assert isinstance(work_id, str)
    assert work_id.startswith("TSK-")
    parts = work_id.split("-")
    assert len(parts) == 3
    assert parts[1].isdigit()
    assert len(parts[2]) == 4
