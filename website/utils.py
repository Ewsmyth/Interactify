import os
import uuid
from datetime import datetime

def generate_unique_filename(username, file_extension):
    current_time = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    random_digits = str(uuid.uuid4().int & (1 << 32) - 1).zfill(5)
    return f"{username}_{current_time}_time_{random_digits}.{file_extension}"