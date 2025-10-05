# utils/utils_producer.py

import json
import time

print("utils_producer.py loaded")  # confirms correct file is being used

def send_event(event, delay=0):
    """
    Send a single WNBA game event (currently prints to console).
    """
    try:
        print(json.dumps(event))
        if delay > 0:
            time.sleep(delay)
    except Exception as e:
        print(f"[ERROR] Failed to send event: {e}")
