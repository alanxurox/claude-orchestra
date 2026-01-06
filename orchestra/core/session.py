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

    def search(self, query: str, hours: float = 168.0) -> List[dict]:
        """Search sessions for matching user prompts.

        Args:
            query: Search term to find in user prompts.
            hours: Number of hours to look back (default 168 = 1 week).

        Returns:
            List of dicts with session info and matching prompts.
        """
        if not self.projects_dir.exists():
            return []

        cutoff = datetime.now() - timedelta(hours=hours)
        results = []
        query_lower = query.lower()

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

                # Search session for matches
                match_result = self._search_session(
                    session_file, project_hash, modified_at, query_lower
                )
                if match_result:
                    results.append(match_result)

        # Sort by match count (most matches first), then by modification time
        results.sort(key=lambda r: (-r["match_count"], -r["modified_at"].timestamp()))
        return results

    def _search_session(
        self, session_path: Path, project_hash: str, modified_at: datetime, query: str
    ) -> Optional[dict]:
        """Search a session file for matching user prompts.

        Args:
            session_path: Path to the session JSONL file.
            project_hash: Hash of the project directory.
            modified_at: Modification timestamp.
            query: Lowercase search query.

        Returns:
            Dict with session info and matches, or None if no matches.
        """
        try:
            matches = []
            project_path = None

            with open(session_path, "r") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        msg = json.loads(line)

                        # Extract project path from init message
                        if msg.get("type") == "init":
                            project_path = msg.get("cwd")

                        # Search user prompts
                        if msg.get("role") == "user":
                            content = msg.get("content", "")
                            prompt_text = ""

                            if isinstance(content, str):
                                prompt_text = content
                            elif isinstance(content, list):
                                # Handle content blocks
                                for block in content:
                                    if isinstance(block, dict) and block.get("type") == "text":
                                        prompt_text = block.get("text", "")
                                        break

                            if prompt_text and query in prompt_text.lower():
                                matches.append(prompt_text[:200])

                    except json.JSONDecodeError:
                        continue

            if not matches:
                return None

            session_id = session_path.stem
            return {
                "session_id": session_id,
                "project_hash": project_hash,
                "project_path": project_path,
                "session_path": str(session_path),
                "modified_at": modified_at,
                "match_count": len(matches),
                "matching_prompts": matches,
                "sample_prompt": matches[0] if matches else None,
            }
        except Exception:
            return None

    def get_most_recent(self) -> Optional[Session]:
        """Get the most recently modified session.

        Returns:
            Session object or None if no sessions found.
        """
        # Look back far enough to find at least one session
        sessions = self.find_recent(hours=168.0)  # 1 week
        return sessions[0] if sessions else None

    def load_messages(self, session_id: str) -> List[dict]:
        """Load all messages from a session.

        Args:
            session_id: The session ID to load.

        Returns:
            List of message dicts with role and content.
        """
        session = self.get_session(session_id)
        if not session:
            return []

        messages = []
        try:
            with open(session.session_path, "r") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        msg = json.loads(line)
                        # Only include user/assistant messages
                        if msg.get("role") in ("user", "assistant"):
                            messages.append(msg)
                    except json.JSONDecodeError:
                        continue
        except Exception:
            return []

        return messages

    def export_to_markdown(self, session_id: str) -> Optional[str]:
        """Export a session to markdown format.

        Args:
            session_id: The session ID to export.

        Returns:
            Markdown string or None if session not found.
        """
        session = self.get_session(session_id)
        if not session:
            return None

        messages = self.load_messages(session_id)

        # Build markdown
        lines = []

        # Header with metadata
        lines.append(f"# Session Export: {session.session_id}")
        lines.append("")
        lines.append("## Metadata")
        lines.append("")
        lines.append(f"- **Session ID:** `{session.session_id}`")
        if session.project_path:
            lines.append(f"- **Project:** `{session.project_path}`")
        lines.append(f"- **Modified:** {session.modified_at.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"- **Message Count:** {session.message_count}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Conversation")
        lines.append("")

        # Messages
        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")

            # Format role header
            role_display = "User" if role == "user" else "Assistant"
            lines.append(f"### {role_display}")
            lines.append("")

            # Extract text content
            text_content = self._extract_content_text(content)
            if text_content:
                lines.append(text_content)
            lines.append("")

        return "\n".join(lines)

    def _extract_content_text(self, content) -> str:
        """Extract text from message content.

        Args:
            content: Content field (string or list of blocks).

        Returns:
            Extracted text content.
        """
        if isinstance(content, str):
            return content

        if isinstance(content, list):
            parts = []
            for block in content:
                if isinstance(block, dict):
                    block_type = block.get("type", "")
                    if block_type == "text":
                        parts.append(block.get("text", ""))
                    elif block_type == "tool_use":
                        # Format tool use as code block
                        tool_name = block.get("name", "unknown")
                        tool_input = block.get("input", {})
                        parts.append(f"**Tool: {tool_name}**")
                        if tool_input:
                            parts.append("```json")
                            parts.append(json.dumps(tool_input, indent=2))
                            parts.append("```")
                    elif block_type == "tool_result":
                        # Format tool result
                        result_content = block.get("content", "")
                        if result_content:
                            parts.append("**Tool Result:**")
                            parts.append("```")
                            if isinstance(result_content, str):
                                parts.append(result_content[:2000])  # Truncate long results
                            else:
                                parts.append(json.dumps(result_content, indent=2)[:2000])
                            parts.append("```")
                elif isinstance(block, str):
                    parts.append(block)
            return "\n".join(parts)

        return str(content)

    def check_health(self, hours: float = 168.0) -> dict:
        """Check health of sessions.

        Args:
            hours: Number of hours to look back for analysis.

        Returns:
            Dict with health report: storage_bytes, session_count,
            stale_sessions, orphaned_sessions, largest_sessions
        """
        if not self.projects_dir.exists():
            return {
                "storage_bytes": 0,
                "session_count": 0,
                "active_sessions": 0,
                "stale_sessions": [],
                "orphaned_sessions": [],
                "largest_sessions": [],
                "oldest_sessions": [],
            }

        now = datetime.now()
        cutoff = now - timedelta(hours=hours)
        stale_cutoff = now - timedelta(hours=48)  # Stale = no update in 48h

        total_bytes = 0
        all_sessions = []

        # Scan all project directories
        for project_dir in self.projects_dir.iterdir():
            if not project_dir.is_dir():
                continue

            project_hash = project_dir.name

            # Find all JSONL session files
            for session_file in project_dir.glob("*.jsonl"):
                try:
                    stat = session_file.stat()
                    file_size = stat.st_size
                    modified_at = datetime.fromtimestamp(stat.st_mtime)

                    # Only include sessions within the lookback period
                    if modified_at < cutoff:
                        continue

                    total_bytes += file_size

                    # Parse session for metadata
                    session = self._parse_session(session_file, project_hash, modified_at)
                    if session:
                        all_sessions.append({
                            "session": session,
                            "file_size": file_size,
                            "is_stale": modified_at < stale_cutoff,
                        })
                except Exception:
                    continue

        # Calculate counts
        session_count = len(all_sessions)
        active_count = sum(1 for s in all_sessions if not s["is_stale"])

        # Find stale sessions (no update in 48h)
        stale_sessions = [
            {
                "session_id": s["session"].session_id,
                "project_path": s["session"].project_path,
                "modified_at": s["session"].modified_at,
                "message_count": s["session"].message_count,
                "file_size": s["file_size"],
            }
            for s in all_sessions
            if s["is_stale"]
        ]
        # Sort by modified_at (oldest first)
        stale_sessions.sort(key=lambda x: x["modified_at"])

        # Find orphaned sessions (project path no longer exists)
        orphaned_sessions = []
        for s in all_sessions:
            session = s["session"]
            if session.project_path and not Path(session.project_path).exists():
                orphaned_sessions.append({
                    "session_id": session.session_id,
                    "project_path": session.project_path,
                    "modified_at": session.modified_at,
                    "message_count": session.message_count,
                    "file_size": s["file_size"],
                })

        # Find unusually large sessions (>1000 messages)
        large_sessions = [
            {
                "session_id": s["session"].session_id,
                "project_path": s["session"].project_path,
                "modified_at": s["session"].modified_at,
                "message_count": s["session"].message_count,
                "file_size": s["file_size"],
            }
            for s in all_sessions
            if s["session"].message_count > 1000
        ]
        # Sort by message count (largest first)
        large_sessions.sort(key=lambda x: -x["message_count"])

        # Find oldest sessions that could be cleaned up
        oldest_sessions = sorted(
            [
                {
                    "session_id": s["session"].session_id,
                    "project_path": s["session"].project_path,
                    "modified_at": s["session"].modified_at,
                    "message_count": s["session"].message_count,
                    "file_size": s["file_size"],
                }
                for s in all_sessions
            ],
            key=lambda x: x["modified_at"],
        )[:10]  # Top 10 oldest

        return {
            "storage_bytes": total_bytes,
            "session_count": session_count,
            "active_sessions": active_count,
            "stale_sessions": stale_sessions,
            "orphaned_sessions": orphaned_sessions,
            "largest_sessions": large_sessions[:10],  # Top 10 largest
            "oldest_sessions": oldest_sessions,
        }
