"""Tests for session discovery."""

import json
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from orchestra.core.session import Session, SessionManager


@pytest.fixture
def temp_projects_dir():
    """Create a temporary projects directory with test sessions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        projects_dir = Path(tmpdir)

        # Create a fake project with sessions
        project_hash = "abc123"
        project_dir = projects_dir / project_hash
        project_dir.mkdir()

        # Recent session
        recent_session = project_dir / "session-recent.jsonl"
        recent_session.write_text(
            json.dumps({"type": "init", "cwd": "/test/project"}) + "\n"
            + json.dumps({"role": "user", "content": "Hello"}) + "\n"
            + json.dumps({"role": "assistant", "content": "Hi!"}) + "\n"
        )

        # Old session (modified to be old)
        old_session = project_dir / "session-old.jsonl"
        old_session.write_text(
            json.dumps({"type": "init", "cwd": "/test/old"}) + "\n"
        )
        # Set modification time to 1 week ago
        old_time = datetime.now() - timedelta(days=7)
        import os
        os.utime(old_session, (old_time.timestamp(), old_time.timestamp()))

        yield projects_dir


def test_find_recent_sessions(temp_projects_dir):
    """Test finding recent sessions."""
    manager = SessionManager(projects_dir=temp_projects_dir)
    sessions = manager.find_recent(hours=1)

    assert len(sessions) == 1
    assert sessions[0].session_id == "session-recent"
    assert sessions[0].message_count == 3
    assert sessions[0].project_path == "/test/project"


def test_find_no_sessions_in_empty_dir():
    """Test with empty directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = SessionManager(projects_dir=Path(tmpdir))
        sessions = manager.find_recent(hours=1)
        assert len(sessions) == 0


def test_session_metadata():
    """Test Session dataclass."""
    session = Session(
        session_id="test-123",
        project_hash="abc",
        project_path="/test",
        session_path=Path("/tmp/test.jsonl"),
        modified_at=datetime.now(),
        message_count=5,
        last_prompt="Hello world",
    )

    assert session.session_id == "test-123"
    assert session.message_count == 5
    assert session.status == "unknown"
