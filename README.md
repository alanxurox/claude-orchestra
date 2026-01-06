# Claude Orchestra

[![Tests](https://github.com/alanxurox/claude-orchestra/actions/workflows/tests.yml/badge.svg)](https://github.com/alanxurox/claude-orchestra/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**The lightweight Claude orchestrator.** No Docker, no databases, no complex setup. Just `pip install` and go.

Multi-agent orchestration for Claude Code with git worktree isolation.

## Features

- **Session Discovery** - Find and resume recent Claude Code sessions
- **Worktree Isolation** - Each agent works in its own git worktree
- **Parallel Execution** - Run multiple agents simultaneously
- **Web Dashboard** - Mobile-friendly real-time monitoring
- **Permission Bypass** - Configure auto-approve for autonomous operation

## Why Claude Orchestra?

The Claude orchestration space has matured with powerful tools like claude-flow and claude-squad. So why build another one?

**Because most developers don't need enterprise infrastructure.** They need to run a few Claude agents in parallel without spending an hour on setup.

| What you get | What you don't need |
|--------------|---------------------|
| No Docker required | Container orchestration |
| No external databases | Redis/Postgres setup |
| Just `pip install claude-orchestra` | YAML configuration files |
| Session discovery (find and resume your Claude sessions) | Manual session tracking |
| Mobile-friendly dashboard | Desktop-only interfaces |
| ~1.8k lines of readable Python | Complex abstractions |

**Our bet:** If you want to run 2-5 agents on a weekend project, you shouldn't need to learn Kubernetes first.

## Installation

```bash
pip install claude-orchestra
```

Or install from source:

```bash
git clone https://github.com/alanxurox/claude-orchestra
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

We're honest about the competition. These projects are excellent, and you should consider them:

| Project | Stars | Best For |
|---------|-------|----------|
| [claude-flow](https://github.com/ruvnet/claude-flow) | ~11k | Enterprise-grade orchestration. Docker-based infrastructure with databases, queues, and advanced features. Choose this if you need SSO/RBAC, persistent memory, or are orchestrating 50+ agents. |
| [claude-squad](https://github.com/smtg-ai/claude-squad) | ~5.5k | Team-oriented workflows. Go-based with multi-tool support and database backing. Great for teams needing shared agent state across restarts. |
| [ccswarm](https://github.com/nwiizo/ccswarm) | - | Rust-native, high-performance. If you need maximum throughput and are comfortable with Rust tooling. |
| [Auto-Claude](https://github.com/anthropics/anthropic-cookbook) | - | Built on Claude Agent SDK. Strong QA loops and testing workflows. |

**When to choose claude-orchestra:**
- You want to run 2-5 agents without infrastructure setup
- You want to discover/resume Claude Code sessions from mobile
- You prefer ~1.8k lines of readable Python you can understand and modify
- You don't want to install Docker or configure databases

**When to choose alternatives:**
- You need enterprise SSO/RBAC (use claude-flow)
- You need persistent agent memory across restarts (use claude-squad)
- You're orchestrating 50+ agents (use claude-flow)
- You need maximum performance (use ccswarm)

## License

MIT
