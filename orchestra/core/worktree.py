"""Git worktree management for isolated agent execution."""

import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from ..config import get_config


@dataclass
class Worktree:
    """Represents a git worktree."""

    path: Path
    branch: str
    task: str
    created_at: datetime
    is_active: bool = True
    session_id: Optional[str] = None


class WorktreeManager:
    """Manages git worktrees for parallel agent execution."""

    def __init__(self, repo_path: Optional[Path] = None, worktree_dir: Optional[str] = None):
        """Initialize worktree manager.

        Args:
            repo_path: Path to the git repository. Defaults to current directory.
            worktree_dir: Directory name for worktrees. Defaults to config value.
        """
        self.repo_path = repo_path or Path.cwd()
        self.worktree_dir = worktree_dir or get_config().worktree_dir
        self.branch_prefix = get_config().branch_prefix

    @property
    def worktrees_root(self) -> Path:
        """Get the root directory for worktrees."""
        return self.repo_path / self.worktree_dir

    def create(self, task: str, base_branch: Optional[str] = None) -> Worktree:
        """Create a new worktree for a task.

        Args:
            task: Task name (used for branch naming).
            base_branch: Branch to base off. Defaults to current branch.

        Returns:
            Worktree object.

        Raises:
            RuntimeError: If worktree creation fails.
        """
        # Sanitize task name for branch
        safe_task = task.lower().replace(" ", "-").replace("/", "-")[:50]
        branch_name = f"{self.branch_prefix}/{safe_task}"
        worktree_path = self.worktrees_root / f"task-{safe_task}"

        # Create worktrees directory if needed
        self.worktrees_root.mkdir(parents=True, exist_ok=True)

        # Get base branch if not specified
        if base_branch is None:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
            )
            base_branch = result.stdout.strip() or "main"

        # Create the worktree with new branch
        try:
            subprocess.run(
                ["git", "worktree", "add", "-b", branch_name, str(worktree_path), base_branch],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError:
            # Branch might already exist, try without -b
            subprocess.run(
                ["git", "worktree", "add", str(worktree_path), branch_name],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )

        return Worktree(
            path=worktree_path,
            branch=branch_name,
            task=task,
            created_at=datetime.now(),
            is_active=True,
        )

    def list_active(self) -> List[Worktree]:
        """List all active worktrees.

        Returns:
            List of Worktree objects.
        """
        result = subprocess.run(
            ["git", "worktree", "list", "--porcelain"],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
        )

        worktrees = []
        current_path = None
        current_branch = None

        for line in result.stdout.split("\n"):
            if line.startswith("worktree "):
                current_path = Path(line.split(" ", 1)[1])
            elif line.startswith("branch refs/heads/"):
                current_branch = line.split("refs/heads/", 1)[1]

                # Only include orchestra worktrees
                if current_branch and current_branch.startswith(self.branch_prefix + "/"):
                    task = current_branch.split("/", 1)[1]
                    worktrees.append(
                        Worktree(
                            path=current_path,
                            branch=current_branch,
                            task=task,
                            created_at=datetime.now(),  # Would need file stat for real time
                            is_active=True,
                        )
                    )

        return worktrees

    def get_worktree(self, task: str) -> Optional[Worktree]:
        """Get a worktree by task name.

        Args:
            task: The task name to find.

        Returns:
            Worktree object or None if not found.
        """
        safe_task = task.lower().replace(" ", "-").replace("/", "-")[:50]
        for wt in self.list_active():
            if wt.task == safe_task:
                return wt
        return None

    def cleanup(self, merged_only: bool = True) -> int:
        """Remove worktrees that are no longer needed.

        Args:
            merged_only: If True, only remove worktrees whose branches are merged.

        Returns:
            Number of worktrees removed.
        """
        removed = 0
        worktrees = self.list_active()

        for wt in worktrees:
            should_remove = False

            if merged_only:
                # Check if branch is merged into main
                result = subprocess.run(
                    ["git", "branch", "--merged", "main"],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                )
                merged_branches = [b.strip().lstrip("* ") for b in result.stdout.split("\n")]
                should_remove = wt.branch in merged_branches
            else:
                should_remove = True

            if should_remove:
                self.remove(wt)
                removed += 1

        return removed

    def remove(self, worktree: Worktree) -> None:
        """Remove a specific worktree.

        Args:
            worktree: The worktree to remove.
        """
        # Remove worktree
        subprocess.run(
            ["git", "worktree", "remove", str(worktree.path), "--force"],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
        )

        # Optionally delete the branch
        subprocess.run(
            ["git", "branch", "-D", worktree.branch],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
        )

    def prune(self) -> None:
        """Prune stale worktree metadata."""
        subprocess.run(
            ["git", "worktree", "prune"],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
        )
