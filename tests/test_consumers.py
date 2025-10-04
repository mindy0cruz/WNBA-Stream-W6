"""
tests/test_consumers.py

Minimal tests for consumer idempotency.
"""

import json
import pathlib
import sqlite3
import pytest

from consumers.sqlite_consumer_case import init_db, insert_message


def test_init_db_is_idempotent(tmp_path: pathlib.Path):
    """Verify init_db can be called multiple times without error."""
    db_path = tmp_path / "test.sqlite"
    
    # Call twice - should not fail
    init_db(db_path)
    init_db(db_path)  # Second call should be safe
    
    # Verify table exists
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='streamed_messages';")
        assert cur.fetchone() is not None


def test_init_db_preserves_data(tmp_path: pathlib.Path):
    """Verify init_db doesn't drop existing data."""
    db_path = tmp_path / "test.sqlite"
    
    # Initialize and insert a message
    init_db(db_path)
    msg = {
        "message": "test",
        "author": "A",
        "timestamp": "2025-01-01 00:00:00",
        "category": "x",
        "sentiment": 0.5,
        "keyword_mentioned": "k",
        "message_length": 4,
    }
    insert_message(msg, db_path)
    
    # Call init_db again
    init_db(db_path)
    
    # Verify data still exists
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM streamed_messages;")
        count = cur.fetchone()[0]
        assert count == 1, "init_db should not drop existing data"


def test_insert_message_appends(tmp_path: pathlib.Path):
    """Verify insert_message appends without deleting prior data."""
    db_path = tmp_path / "test.sqlite"
    init_db(db_path)
    
    msg1 = {
        "message": "first",
        "author": "A",
        "timestamp": "2025-01-01 00:00:00",
        "category": "x",
        "sentiment": 0.5,
        "keyword_mentioned": "k",
        "message_length": 5,
    }
    msg2 = {
        "message": "second",
        "author": "B",
        "timestamp": "2025-01-01 00:00:01",
        "category": "y",
        "sentiment": 0.7,
        "keyword_mentioned": "k2",
        "message_length": 6,
    }
    
    insert_message(msg1, db_path)
    insert_message(msg2, db_path)
    
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM streamed_messages;")
        count = cur.fetchone()[0]
        assert count == 2