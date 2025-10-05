# ============================================
# producers/game_producer.py
# WNBA Playoffs Streaming Producer
# ============================================

import os
import sys
import json
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

# Ensure project root is in path so we can import utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.utils_producer import send_event


# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()

DATA_DIR = os.getenv("BASE_DATA_DIR", "data")
LIVE_DATA_FILE = os.getenv("LIVE_DATA_FILE_NAME", "wnba_playoffs_live.json")
MESSAGE_INTERVAL = float(os.getenv("MESSAGE_INTERVAL_SECONDS", 3))

data_file_path = os.path.join(DATA_DIR, LIVE_DATA_FILE)


# ----------------------------
# Helper: Load event data
# ----------------------------
def load_game_data(file_path):
    """Load WNBA game events from a JSON file."""
    if not os.path.exists(file_path):
        print(f"[ERROR] Data file not found: {file_path}")
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Normalize event structure
    for e in data:
        e["points_scored"] = e.get("points_scored", e.get("points", 0))
        e.pop("points", None)
    return data


# ----------------------------
# Simulate live streaming
# ----------------------------
def stream_events(events, delay=3):
    """Simulate sending live WNBA game events with a time delay."""
    for event in events:
        event["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        event["points_scored"] = event.get("points_scored", 0)

        send_event(event, delay=delay)
        print(f"[INFO] Sent event: {event}")
        time.sleep(delay)


# ----------------------------
# Main function
# ----------------------------
def main():
    print("[INFO] Starting WNBA Producer...")
    print(f"[INFO] Streaming events from: {data_file_path}")

    events = load_game_data(data_file_path)
    if not events:
        print("[ERROR] No events to stream. Exiting.")
        return

    print(f"[INFO] Loaded {len(events)} events from {data_file_path}")
    stream_events(events, MESSAGE_INTERVAL)


# ----------------------------
# Run the producer
# ----------------------------
if __name__ == "__main__":
    main()
