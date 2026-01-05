"""Session discovery and management for Claude Code sessions."""

import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

from ..config import get_config


@dataclass
class Session:
    """Represents a Claude Code session."""

    session_id: str
    project_hash: str
    project_path: Optional[str]
    session_path: Path
    modified_at: datetime
    message_count: int
    last_prompt: Optional[str] = None
    status: str = "unknown"  # unknown, running, completed, stale


class SessionManager:
    """Manages Claude Code session discovery and operations."""

    def __init__(self, projects_dir: Optional[Path] = None):
        """Initialize session manager.

        Args:
            projects_dir: Path to Claude projects directory.
                         Defaults to ~/.claude/projects/
        """
        self.projects_dir = projects_dir or get_config().claude_projects_dir

    def find_recent(self, hours: float = 2.0) -> List[Session]:
        """Find sessions modified within the last N hours.

        Args:
            hours: Number of hours to look back.

        Returns:
            List of Session objects sorted by modification time (newest first).
        """
        if not self.projects_dir.exists():
            return []

        cutoff = datetime.now() - timedelta(hours=hours)
        sessions = []

        # Scan all project directories
        for project_dir in self.projects_dir.iterdir():
            if not project_dir.is_dir():
                continue

            project_hash = project_dir.name

            # Find all JSONL session files
            for session_file in project_dir.glob("*.jsonl"):
                stat = session_file.stat()
                modified_at = datetime.fromtimestamp(stat.st_mtime)

                if modified_at < cutoff:
                    continue

                # Parse session metadata
                session = self._parse_session(session_file, project_hash, modified_at)
                if session:
                    sessions.append(session)

        # Sort by modification time (newest first)
        sessions.sort(key=lambda s: s.modified_at, reverse=True)
        return sessions

    def _parse_session(
        self, session_path: Path, project_hash: str, modified_at: datetime
    ) -> Optional[Session]:
        """Parse a session JSONL file for metadata.

        Args:
            session_path: Path to the session JSONL file.
            project_hash: Hash of the project directory.
            modified_at: Modification timestamp.

        Returns:
            Session object or None if parsing fails.
        """
        try:
            message_count = 0
            last_prompt = None
            project_path = None

            with open(session_path, "r") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        msg = json.loads(line)
                        message_count += 1

                        # Extract project path from init message
                        if msg.get("type") == "init":
                            project_path = msg.get("cwd")

                        # Track last user prompt
                        if msg.get("role") == "user":
                            content = msg.get("content", "")
                            if isinstance(content, str):
                                last_prompt = content[:100]
                            elif isinstance(content, list):
                                # Handle content blocks
                                for block in content:
                                    if isinstance(block, dict) and block.get("type") == "text":
                                        last_prompt = block.get("text", "")[:100]
                                        break
                    except json.JSONDecodeError:
                        continue

            session_id = session_path.stem
            return Session(
                session_id=session_id,
                project_hash=project_hash,
                project_path=project_path,
                session_path=session_path,
                modified_at=modified_at,
                message_count=message_count,
                last_prompt=last_prompt,
            )
        except Exception:
            return None

    def get_session(self, session_id: str) -> Optional[Session]:
        """Get a specific session by ID.

        Args:
            session_id: The session ID to find.

        Returns:
            Session object or None if not found.
        """
        for project_dir in self.projects_dir.iterdir():
            if not project_dir.is_dir():
                continue

            session_path = project_dir / f"{session_id}.jsonl"
            if session_path.exists():
                stat = session_path.stat()
                modified_at = datetime.fromtimestamp(stat.st_mtime)
                return self._parse_session(session_path, project_dir.name, modified_at)

        return None

    def resume(self, session_id: str, prompt: Optional[str] = None) -> subprocess.Popen:
        """Resume a session with optional new prompt.

        Args:
            session_id: The session ID to resume.
            prompt: Optional prompt to send.

        Returns:
            Subprocess handle.
        """
        cmd = ["claude", "--resume", session_id]
        if prompt:
            cmd.extend(["--print", prompt])

        return subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def continue_last(self, prompt: Optional[str] = None) -> subprocess.Popen:
        """Continue the most recent session.

        Args:
            prompt: Optional prompt to send.

        Returns:
            Subprocess handle.
        """
        cmd = ["claude", "--continue"]
        if prompt:
            cmd.extend(["--print", prompt])

        return subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
