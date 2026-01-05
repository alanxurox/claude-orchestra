# Claude Orchestra

Multi-agent orchestration for Claude Code with git worktree isolation.

## Features

- **Session Discovery** - Find and resume recent Claude Code sessions
- **Worktree Isolation** - Each agent works in its own git worktree
- **Parallel Execution** - Run multiple agents simultaneously
- **Web Dashboard** - Mobile-friendly real-time monitoring
- **Permission Bypass** - Configure auto-approve for autonomous operation

## Installation

```bash
pip install claude-orchestra
```

Or install from source:

```bash
git clone https://github.com/morningguard/claude-orchestra
cd claude-orchestra
pip install -e ".[dev]"
```

## Quick Start

```bash
# Initialize in your project
cd my-project
orchestra init

# Find recent sessions
orchestra sessions --hours 4

# Spawn parallel agents
orchestra spawn "implement auth" "add tests" "fix performance"

# Monitor in terminal
orchestra status --watch

# Or launch web dashboard
orchestra web
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `orchestra init` | Initialize in current project |
| `orchestra sessions` | List recent Claude Code sessions |
| `orchestra spawn` | Spawn parallel agents for tasks |
| `orchestra status` | Show agent status |
| `orchestra collect` | Collect results from agents |
| `orchestra cleanup` | Clean up completed agents |
| `orchestra worktrees` | List active worktrees |
| `orchestra web` | Launch web dashboard |

## How It Works

### Git Worktree Isolation

Each agent runs in its own git worktree, providing:
- Isolated file state
- Independent branches
- No conflicts between agents
- Clean merge via PR

```
my-project/
├── .git/
├── src/
└── .worktrees/
    ├── task-implement-auth/    # Agent 1
    ├── task-add-tests/         # Agent 2
    └── task-fix-performance/   # Agent 3
```

### Session Discovery

Orchestra scans `~/.claude/projects/` to find recent sessions:

```bash
# Find sessions from last 4 hours
orchestra sessions --hours 4

# Output as JSON
orchestra sessions --json
```

### Web Dashboard

Launch a mobile-friendly dashboard:

```bash
orchestra web --port 8888
```

Features:
- Real-time status updates via WebSocket
- Spawn new agents
- Pause/resume agents
- View agent activity

## Configuration

Config file: `~/.config/claude-orchestra/config.json`

```json
{
  "default_parallel": 3,
  "max_parallel": 8,
  "worktree_dir": ".worktrees",
  "branch_prefix": "orchestra",
  "heartbeat_interval": 60,
  "stale_threshold": 300,
  "bypass_permissions": [
    "Bash(git *)",
    "Bash(npm *)",
    "Read(*)",
    "Write(*)"
  ]
}
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/status` | GET | Get orchestrator status |
| `/api/sessions` | GET | List recent sessions |
| `/api/worktrees` | GET | List active worktrees |
| `/api/spawn` | POST | Spawn new agents |
| `/api/agents/{id}/pause` | POST | Pause an agent |
| `/api/agents/{id}/resume` | POST | Resume an agent |
| `/api/cleanup` | POST | Clean up agents |
| `/ws/status` | WS | Real-time status updates |

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black orchestra/
ruff orchestra/
```

## Similar Projects

- [ccswarm](https://github.com/nwiizo/ccswarm) - Claude Code + git worktree (Go)
- [claude-flow](https://github.com/ruvnet/claude-flow) - Multi-agent orchestration platform
- [swarms](https://github.com/kyegomez/swarms) - Enterprise multi-agent framework

## License

MIT
