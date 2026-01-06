"""Tests for CLI commands."""

import json
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import pytest
from click.testing import CliRunner

from orchestra.cli import main


@pytest.fixture
def runner():
    """Create a CLI test runner."""
    return CliRunner()


@pytest.fixture
def temp_projects_dir():
    """Create a temporary projects directory with test sessions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        projects_dir = Path(tmpdir)

        # Create a fake project with sessions
        project_hash = "abc123"
        project_dir = projects_dir / project_hash
        project_dir.mkdir()

        # Session with searchable content
        session1 = project_dir / "session-auth-work.jsonl"
        session1.write_text(
            json.dumps({"type": "init", "cwd": "/test/myproject"})
            + "\n"
            + json.dumps({"role": "user", "content": "Help me fix the authentication bug"})
            + "\n"
            + json.dumps({"role": "assistant", "content": "I'll help you with that."})
            + "\n"
            + json.dumps({"role": "user", "content": "Also update the auth middleware"})
            + "\n"
        )

        # Another session
        session2 = project_dir / "session-refactor.jsonl"
        session2.write_text(
            json.dumps({"type": "init", "cwd": "/test/another"})
            + "\n"
            + json.dumps({"role": "user", "content": "Refactor the database layer"})
            + "\n"
            + json.dumps({"role": "assistant", "content": "Sure, let me help."})
            + "\n"
        )

        yield projects_dir


@pytest.fixture
def empty_projects_dir():
    """Create an empty temporary projects directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


# =============================================================================
# Analytics Command Tests
# =============================================================================


class TestAnalyticsCommand:
    """Tests for the analytics command."""

    def test_analytics_with_empty_sessions(self, runner, empty_projects_dir, monkeypatch):
        """Test analytics command with no sessions."""
        from orchestra.core import session

        monkeypatch.setattr(
            session, "get_config",
            lambda: type("Config", (), {"claude_projects_dir": empty_projects_dir})()
        )

        result = runner.invoke(main, ["analytics", "--hours", "24"])

        assert result.exit_code == 0
        assert "No sessions found" in result.output

    def test_analytics_json_output(self, runner, temp_projects_dir, monkeypatch):
        """Test analytics command with JSON output format."""
        from orchestra.core import session

        monkeypatch.setattr(
            session, "get_config",
            lambda: type("Config", (), {"claude_projects_dir": temp_projects_dir})()
        )

        result = runner.invoke(main, ["analytics", "--hours", "24", "--json"])

        assert result.exit_code == 0

        # Parse JSON output
        output_data = json.loads(result.output)

        # Check required fields in JSON response
        assert "period_hours" in output_data
        assert "total_sessions" in output_data
        assert "total_messages" in output_data
        assert "avg_messages_per_session" in output_data
        assert "projects" in output_data

        # Verify data types
        assert isinstance(output_data["period_hours"], (int, float))
        assert isinstance(output_data["total_sessions"], int)
        assert isinstance(output_data["total_messages"], int)
        assert isinstance(output_data["avg_messages_per_session"], (int, float))
        assert isinstance(output_data["projects"], dict)


# =============================================================================
# Search Command Tests
# =============================================================================


class TestSearchCommand:
    """Tests for the search command."""

    def test_search_with_no_results(self, runner, temp_projects_dir, monkeypatch):
        """Test search command when no sessions match the query."""
        from orchestra.core import session

        monkeypatch.setattr(
            session, "get_config",
            lambda: type("Config", (), {"claude_projects_dir": temp_projects_dir})()
        )

        result = runner.invoke(main, ["search", "nonexistent-term-xyz"])

        assert result.exit_code == 0
        assert "No sessions found matching" in result.output

    def test_search_result_structure(self, runner, temp_projects_dir, monkeypatch):
        """Test search command result structure with JSON output."""
        from orchestra.core import session

        monkeypatch.setattr(
            session, "get_config",
            lambda: type("Config", (), {"claude_projects_dir": temp_projects_dir})()
        )

        result = runner.invoke(main, ["search", "auth", "--json"])

        assert result.exit_code == 0

        # Parse JSON output
        output_data = json.loads(result.output)

        # Should find at least one result (the session with "authentication" content)
        assert isinstance(output_data, list)
        assert len(output_data) > 0

        # Check structure of first result
        first_result = output_data[0]
        assert "session_id" in first_result
        assert "project_path" in first_result
        assert "modified_at" in first_result
        assert "match_count" in first_result
        assert "sample_prompt" in first_result

        # Verify match count is positive
        assert first_result["match_count"] > 0


# =============================================================================
# Export Command Tests
# =============================================================================


class TestExportCommand:
    """Tests for the export command."""

    def test_export_with_invalid_session_id(self, runner, temp_projects_dir, monkeypatch):
        """Test export command with a non-existent session ID."""
        from orchestra.core import session

        monkeypatch.setattr(
            session, "get_config",
            lambda: type("Config", (), {"claude_projects_dir": temp_projects_dir})()
        )

        result = runner.invoke(main, ["export", "nonexistent-session-id"])

        assert result.exit_code == 1
        assert "Session not found" in result.output

    def test_export_last_flag_with_sessions(self, runner, temp_projects_dir, monkeypatch):
        """Test export command with --last flag when sessions exist."""
        from orchestra.core import session

        monkeypatch.setattr(
            session, "get_config",
            lambda: type("Config", (), {"claude_projects_dir": temp_projects_dir})()
        )

        result = runner.invoke(main, ["export", "--last"])

        assert result.exit_code == 0
        # Should contain markdown export format
        assert "# Session Export:" in result.output
        assert "## Metadata" in result.output
        assert "## Conversation" in result.output

    def test_export_last_flag_with_no_sessions(self, runner, empty_projects_dir, monkeypatch):
        """Test export command with --last flag when no sessions exist."""
        from orchestra.core import session

        monkeypatch.setattr(
            session, "get_config",
            lambda: type("Config", (), {"claude_projects_dir": empty_projects_dir})()
        )

        result = runner.invoke(main, ["export", "--last"])

        assert result.exit_code == 1
        assert "No sessions found" in result.output

    def test_export_requires_session_id_or_last_flag(self, runner, temp_projects_dir, monkeypatch):
        """Test export command requires either session ID or --last flag."""
        from orchestra.core import session

        monkeypatch.setattr(
            session, "get_config",
            lambda: type("Config", (), {"claude_projects_dir": temp_projects_dir})()
        )

        result = runner.invoke(main, ["export"])

        assert result.exit_code == 1
        assert "Please provide a session ID or use --last" in result.output
