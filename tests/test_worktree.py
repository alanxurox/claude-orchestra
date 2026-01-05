"""Tests for worktree management."""

import subprocess
import tempfile
from pathlib import Path

import pytest

from orchestra.core.worktree import Worktree, WorktreeManager


@pytest.fixture
def git_repo():
    """Create a temporary git repository."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = Path(tmpdir)

        # Initialize git repo
        subprocess.run(["git", "init"], cwd=repo, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@test.com"],
            cwd=repo,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test"],
            cwd=repo,
            capture_output=True,
        )

        # Create initial commit
        (repo / "README.md").write_text("# Test")
        subprocess.run(["git", "add", "."], cwd=repo, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial"],
            cwd=repo,
            capture_output=True,
        )

        yield repo


def test_create_worktree(git_repo):
    """Test creating a worktree."""
    manager = WorktreeManager(repo_path=git_repo)
    worktree = manager.create("test-task")

    assert worktree.path.exists()
    assert worktree.task == "test-task"
    assert worktree.branch == "orchestra/test-task"
    assert worktree.is_active


def test_list_worktrees(git_repo):
    """Test listing worktrees."""
    manager = WorktreeManager(repo_path=git_repo)

    # Create some worktrees
    manager.create("task-1")
    manager.create("task-2")

    worktrees = manager.list_active()
    assert len(worktrees) == 2

    tasks = {wt.task for wt in worktrees}
    assert "task-1" in tasks
    assert "task-2" in tasks


def test_get_worktree(git_repo):
    """Test getting a specific worktree."""
    manager = WorktreeManager(repo_path=git_repo)
    manager.create("my-task")

    worktree = manager.get_worktree("my-task")
    assert worktree is not None
    assert worktree.task == "my-task"

    # Non-existent worktree
    assert manager.get_worktree("nonexistent") is None


def test_remove_worktree(git_repo):
    """Test removing a worktree."""
    manager = WorktreeManager(repo_path=git_repo)
    worktree = manager.create("to-remove")

    assert worktree.path.exists()

    manager.remove(worktree)
    assert not worktree.path.exists()
