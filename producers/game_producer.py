# producers
# game_producer.py

import json
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Config from .env
DATA_DIR = os.getenv("BASE_DATA_DIR", "data")
LIVE_DATA_FILE = os.getenv("LIVE_DATA_FILE_NAME", "wnba_playoffs_live.json")
MESSAGE_INTERVAL = float(os.getenv("MESSAGE_INTERVAL_SECONDS", 3))

# Path to the JSON file
data_file_path = os.path.join(DATA_DIR, LIVE_DATA_FILE)

def load_game_events(file_path):
    """Load simulated WNBA game events from a JSON file."""
    try:
        with open(file_path, "r") as f:
            events = json.load(f)
        print(f"[INFO] Loaded {len(events)} game events.")
        return events
    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"[ERROR] Failed to decode JSON from {file_path}")
        return []

def stream_events(events, interval):
    """Simulate live streaming of game events."""
    for event in events:
       
        print(json.dumps(event))  

def main():
    events = load_game_events(data_file_path)
    if events:
        print("[INFO] Starting event stream...\n")
        stream_events(events, MESSAGE_INTERVAL)
        print("\n[INFO] Finished streaming all events.")
    else:
        print("[INFO] No events to stream.")

if __name__ == "__main__":
    main()
