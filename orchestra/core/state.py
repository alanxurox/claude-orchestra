"""State persistence for orchestrator."""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from ..config import get_config


@dataclass
class AgentState:
    """State of a single agent."""

    agent_id: str
    session_id: Optional[str]
    worktree_path: Optional[str]
    task: str
    status: str  # pending, running, completed, failed, stale
    started_at: Optional[datetime] = None
    last_heartbeat: Optional[datetime] = None
    progress: float = 0.0
    current_activity: Optional[str] = None
    error_message: Optional[str] = None
    result: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "agent_id": self.agent_id,
            "session_id": self.session_id,
            "worktree_path": self.worktree_path,
            "task": self.task,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "last_heartbeat": self.last_heartbeat.isoformat() if self.last_heartbeat else None,
            "progress": self.progress,
            "current_activity": self.current_activity,
            "error_message": self.error_message,
            "result": self.result,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AgentState":
        """Create from dictionary."""
        return cls(
            agent_id=data["agent_id"],
            session_id=data.get("session_id"),
            worktree_path=data.get("worktree_path"),
            task=data["task"],
            status=data["status"],
            started_at=datetime.fromisoformat(data["started_at"]) if data.get("started_at") else None,
            last_heartbeat=datetime.fromisoformat(data["last_heartbeat"]) if data.get("last_heartbeat") else None,
            progress=data.get("progress", 0.0),
            current_activity=data.get("current_activity"),
            error_message=data.get("error_message"),
            result=data.get("result"),
        )


@dataclass
class OrchestratorState:
    """Global orchestrator state."""

    agents: Dict[str, AgentState] = field(default_factory=dict)
    last_updated: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "agents": {k: v.to_dict() for k, v in self.agents.items()},
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "OrchestratorState":
        """Create from dictionary."""
        agents = {k: AgentState.from_dict(v) for k, v in data.get("agents", {}).items()}
        last_updated = datetime.fromisoformat(data["last_updated"]) if data.get("last_updated") else None
        return cls(agents=agents, last_updated=last_updated)


class StateManager:
    """Manages persistent state for the orchestrator."""

    def __init__(self, state_file: Optional[Path] = None):
        """Initialize state manager.

        Args:
            state_file: Path to state file. Defaults to config value.
        """
        self.state_file = state_file or get_config().state_file
        self._state: Optional[OrchestratorState] = None

    @property
    def state(self) -> OrchestratorState:
        """Get current state, loading if needed."""
        if self._state is None:
            self._state = self.load()
        return self._state

    def load(self) -> OrchestratorState:
        """Load state from file.

        Returns:
            OrchestratorState object.
        """
        if self.state_file.exists():
            try:
                with open(self.state_file) as f:
                    data = json.load(f)
                return OrchestratorState.from_dict(data)
            except (json.JSONDecodeError, KeyError):
                pass
        return OrchestratorState()

    def save(self) -> None:
        """Save state to file."""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state.last_updated = datetime.now()

        with open(self.state_file, "w") as f:
            json.dump(self.state.to_dict(), f, indent=2)

    def add_agent(self, agent: AgentState) -> None:
        """Add or update an agent in state.

        Args:
            agent: The agent state to add.
        """
        self.state.agents[agent.agent_id] = agent
        self.save()

    def remove_agent(self, agent_id: str) -> None:
        """Remove an agent from state.

        Args:
            agent_id: The agent ID to remove.
        """
        if agent_id in self.state.agents:
            del self.state.agents[agent_id]
            self.save()

    def get_agent(self, agent_id: str) -> Optional[AgentState]:
        """Get an agent by ID.

        Args:
            agent_id: The agent ID to find.

        Returns:
            AgentState or None if not found.
        """
        return self.state.agents.get(agent_id)

    def list_agents(self, status: Optional[str] = None) -> List[AgentState]:
        """List all agents, optionally filtered by status.

        Args:
            status: Filter by status if provided.

        Returns:
            List of AgentState objects.
        """
        agents = list(self.state.agents.values())
        if status:
            agents = [a for a in agents if a.status == status]
        return agents

    def update_heartbeat(self, agent_id: str, activity: Optional[str] = None) -> None:
        """Update an agent's heartbeat.

        Args:
            agent_id: The agent ID.
            activity: Optional current activity description.
        """
        agent = self.get_agent(agent_id)
        if agent:
            agent.last_heartbeat = datetime.now()
            if activity:
                agent.current_activity = activity
            self.save()

    def mark_stale_agents(self, threshold_seconds: int = 300) -> List[str]:
        """Mark agents as stale if no recent heartbeat.

        Args:
            threshold_seconds: Seconds without heartbeat to consider stale.

        Returns:
            List of agent IDs marked as stale.
        """
        now = datetime.now()
        stale_ids = []

        for agent in self.list_agents(status="running"):
            if agent.last_heartbeat:
                age = (now - agent.last_heartbeat).total_seconds()
                if age > threshold_seconds:
                    agent.status = "stale"
                    stale_ids.append(agent.agent_id)

        if stale_ids:
            self.save()

        return stale_ids
