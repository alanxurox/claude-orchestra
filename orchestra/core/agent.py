"""Agent orchestration with Claude Code."""

import asyncio
import subprocess
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..config import get_config
from .session import SessionManager
from .state import AgentState, StateManager
from .worktree import Worktree, WorktreeManager


@dataclass
class AgentHandle:
    """Handle to a running agent."""

    agent_id: str
    process: subprocess.Popen
    worktree: Optional[Worktree]
    task: str


@dataclass
class AgentResult:
    """Result from an agent execution."""

    agent_id: str
    task: str
    success: bool
    output: str
    error: Optional[str] = None
    duration_seconds: float = 0.0


class Orchestrator:
    """Orchestrates multiple Claude Code agents."""

    def __init__(
        self,
        repo_path: Optional[Path] = None,
        state_manager: Optional[StateManager] = None,
        worktree_manager: Optional[WorktreeManager] = None,
        session_manager: Optional[SessionManager] = None,
    ):
        """Initialize orchestrator.

        Args:
            repo_path: Path to the git repository.
            state_manager: Optional StateManager instance.
            worktree_manager: Optional WorktreeManager instance.
            session_manager: Optional SessionManager instance.
        """
        self.repo_path = repo_path or Path.cwd()
        self.state = state_manager or StateManager()
        self.worktrees = worktree_manager or WorktreeManager(repo_path)
        self.sessions = session_manager or SessionManager()
        self.config = get_config()
        self._handles: Dict[str, AgentHandle] = {}

    def spawn(
        self,
        tasks: List[str],
        parallel: Optional[int] = None,
        use_worktrees: bool = True,
    ) -> List[AgentHandle]:
        """Spawn agents for multiple tasks.

        Args:
            tasks: List of task descriptions/prompts.
            parallel: Max parallel agents. Defaults to config value.
            use_worktrees: Whether to create worktrees for isolation.

        Returns:
            List of AgentHandle objects.
        """
        parallel = parallel or self.config.default_parallel
        parallel = min(parallel, self.config.max_parallel)

        handles = []
        for i, task in enumerate(tasks[:parallel]):
            handle = self._spawn_single(task, use_worktrees)
            handles.append(handle)
            self._handles[handle.agent_id] = handle

        return handles

    def _spawn_single(self, task: str, use_worktrees: bool = True) -> AgentHandle:
        """Spawn a single agent for a task.

        Args:
            task: Task description/prompt.
            use_worktrees: Whether to create a worktree.

        Returns:
            AgentHandle object.
        """
        agent_id = str(uuid.uuid4())[:8]
        worktree = None
        cwd = self.repo_path

        if use_worktrees:
            worktree = self.worktrees.create(task)
            cwd = worktree.path

        # Build command with bypass permissions
        cmd = ["claude", "--print", task, "--dangerously-skip-permissions"]

        # Add allowlist for common operations
        for pattern in self.config.bypass_permissions:
            cmd.extend(["--allowedTools", pattern])

        # Start the process
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Track state
        agent_state = AgentState(
            agent_id=agent_id,
            session_id=None,  # Will be captured from output
            worktree_path=str(worktree.path) if worktree else None,
            task=task,
            status="running",
            started_at=datetime.now(),
            last_heartbeat=datetime.now(),
        )
        self.state.add_agent(agent_state)

        return AgentHandle(
            agent_id=agent_id,
            process=process,
            worktree=worktree,
            task=task,
        )

    async def collect(self, handles: Optional[List[AgentHandle]] = None) -> Dict[str, AgentResult]:
        """Collect results from agents.

        Args:
            handles: List of handles to collect from. Defaults to all running.

        Returns:
            Dictionary of agent_id to AgentResult.
        """
        if handles is None:
            handles = list(self._handles.values())

        results = {}

        for handle in handles:
            result = await self._collect_single(handle)
            results[handle.agent_id] = result

        return results

    async def _collect_single(self, handle: AgentHandle) -> AgentResult:
        """Collect result from a single agent.

        Args:
            handle: The agent handle.

        Returns:
            AgentResult object.
        """
        start_time = datetime.now()

        # Wait for process to complete
        stdout, stderr = await asyncio.get_event_loop().run_in_executor(
            None, handle.process.communicate
        )

        duration = (datetime.now() - start_time).total_seconds()
        success = handle.process.returncode == 0

        # Update state
        agent_state = self.state.get_agent(handle.agent_id)
        if agent_state:
            agent_state.status = "completed" if success else "failed"
            agent_state.result = stdout[:1000] if stdout else None
            agent_state.error_message = stderr if not success else None
            self.state.save()

        # Clean up handle
        if handle.agent_id in self._handles:
            del self._handles[handle.agent_id]

        return AgentResult(
            agent_id=handle.agent_id,
            task=handle.task,
            success=success,
            output=stdout or "",
            error=stderr if not success else None,
            duration_seconds=duration,
        )

    def status(self) -> Dict[str, Any]:
        """Get status of all agents.

        Returns:
            Dictionary with status information.
        """
        # Mark stale agents
        self.state.mark_stale_agents(self.config.stale_threshold)

        agents = self.state.list_agents()

        return {
            "total": len(agents),
            "running": len([a for a in agents if a.status == "running"]),
            "completed": len([a for a in agents if a.status == "completed"]),
            "failed": len([a for a in agents if a.status == "failed"]),
            "stale": len([a for a in agents if a.status == "stale"]),
            "agents": [a.to_dict() for a in agents],
        }

    def pause(self, agent_id: str) -> bool:
        """Pause an agent.

        Args:
            agent_id: The agent ID to pause.

        Returns:
            True if paused successfully.
        """
        handle = self._handles.get(agent_id)
        if handle and handle.process.poll() is None:
            handle.process.terminate()
            agent_state = self.state.get_agent(agent_id)
            if agent_state:
                agent_state.status = "paused"
                self.state.save()
            return True
        return False

    def resume_agent(self, agent_id: str) -> Optional[AgentHandle]:
        """Resume a paused agent.

        Args:
            agent_id: The agent ID to resume.

        Returns:
            New AgentHandle or None if can't resume.
        """
        agent_state = self.state.get_agent(agent_id)
        if not agent_state or agent_state.status != "paused":
            return None

        # Re-spawn with same task
        handle = self._spawn_single(
            agent_state.task,
            use_worktrees=bool(agent_state.worktree_path),
        )

        # Transfer ID
        self.state.remove_agent(agent_id)
        agent_state.agent_id = handle.agent_id
        agent_state.status = "running"
        agent_state.started_at = datetime.now()
        self.state.add_agent(agent_state)

        return handle

    def cleanup(self, completed_only: bool = True) -> int:
        """Clean up completed agents and worktrees.

        Args:
            completed_only: Only clean up completed/failed agents.

        Returns:
            Number of agents cleaned up.
        """
        cleaned = 0
        agents = self.state.list_agents()

        for agent in agents:
            should_clean = not completed_only or agent.status in ("completed", "failed")

            if should_clean:
                # Remove worktree if exists
                if agent.worktree_path:
                    worktree = self.worktrees.get_worktree(agent.task)
                    if worktree:
                        self.worktrees.remove(worktree)

                self.state.remove_agent(agent.agent_id)
                cleaned += 1

        return cleaned
