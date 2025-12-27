# enterprise_task_system/app/utils/work_id_generator.py

import time
import random
import string

def generate_work_id() -> str:
    """
    Generates a unique, human-readable work ID.

    The format is TSK-<timestamp>-<random_chars>.
    - TSK: A static prefix for "Task".
    - timestamp: A millisecond timestamp to ensure chronological order and uniqueness.
    - random_chars: A short random string to prevent collisions in high-throughput scenarios.

    Returns:
        A string representing the unique work ID.
    """
    # Get the current time in milliseconds as an integer
    timestamp = int(time.time() * 1000)

    # Generate a short random string (4 characters)
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

    # Combine the parts to form the final work ID
    work_id = f"TSK-{timestamp}-{random_chars}"

    return work_id
