import uuid
from datetime import datetime

def generate_id():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    short_uuid = str(uuid.uuid4())[:8]
    return f"{timestamp}_{short_uuid}"
