"""Configuration management for Claude Orchestra."""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class OrchestraConfig:
    """Configuration for Claude Orchestra."""

    # Session discovery
    claude_projects_dir: Path = field(default_factory=lambda: Path.home() / ".claude" / "projects")

    # Worktree settings
    worktree_dir: str = ".worktrees"
    branch_prefix: str = "orchestra"

    # Parallel execution
    default_parallel: int = 3
    max_parallel: int = 8

    # Heartbeat and monitoring
    heartbeat_interval: int = 60  # seconds
    stale_threshold: int = 300  # 5 minutes

    # Permission bypass patterns
    bypass_permissions: List[str] = field(
        default_factory=lambda: [
            "Bash(git *)",
            "Bash(npm *)",
            "Bash(npx *)",
            "Read(*)",
            "Glob(*)",
            "Grep(*)",
            "Write(*)",
            "Edit(*)",
        ]
    )

    # Dashboard
    dashboard_host: str = "0.0.0.0"
    dashboard_port: int = 8888

    # State persistence
    state_file: Path = field(
        default_factory=lambda: Path.home() / ".config" / "claude-orchestra" / "state.json"
    )

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "OrchestraConfig":
        """Load config from file or use defaults."""
        if config_path is None:
            config_path = Path.home() / ".config" / "claude-orchestra" / "config.json"

        if config_path.exists():
            with open(config_path) as f:
                data = json.load(f)
            return cls(
                **{
                    k: Path(v) if k.endswith("_dir") or k == "state_file" else v
                    for k, v in data.items()
                }
            )
        return cls()

    def save(self, config_path: Optional[Path] = None) -> None:
        """Save config to file."""
        if config_path is None:
            config_path = Path.home() / ".config" / "claude-orchestra" / "config.json"

        config_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "claude_projects_dir": str(self.claude_projects_dir),
            "worktree_dir": self.worktree_dir,
            "branch_prefix": self.branch_prefix,
            "default_parallel": self.default_parallel,
            "max_parallel": self.max_parallel,
            "heartbeat_interval": self.heartbeat_interval,
            "stale_threshold": self.stale_threshold,
            "bypass_permissions": self.bypass_permissions,
            "dashboard_host": self.dashboard_host,
            "dashboard_port": self.dashboard_port,
            "state_file": str(self.state_file),
        }

        with open(config_path, "w") as f:
            json.dump(data, f, indent=2)


# Global config instance
_config: Optional[OrchestraConfig] = None


def get_config() -> OrchestraConfig:
    """Get the global config instance."""
    global _config
    if _config is None:
        _config = OrchestraConfig.load()
    return _config


def set_config(config: OrchestraConfig) -> None:
    """Set the global config instance."""
    global _config
    _config = config
