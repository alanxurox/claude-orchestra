# CLAUDE.md - Claude Orchestra

## Strategic Direction

**Positioning:** "The lightweight Claude orchestrator" - no Docker, no databases, just `pip install`.

We operate in a competitive space with established players, but we've identified a clear gap: developers who want orchestration without the complexity. While others build enterprise-grade infrastructure, we build tools that just work.

**Our bet:** Most developers don't need Kubernetes-level orchestration. They need to run a few Claude agents in parallel without spending an hour on setup.

**Core principles:**
- **Simplicity over features** - Every feature must justify its complexity cost
- **Python-native** - No external dependencies beyond pip packages
- **Mobile-first dashboard** - Check on your agents from your phone
- **Zero config start** - Works out of the box, customize later

---

## Competitive Landscape

The Claude orchestration space has matured rapidly:

| Project | Stars | Approach |
|---------|-------|----------|
| claude-flow | ~11k | Full-featured, Docker-based infrastructure |
| claude-squad | ~5.5k | Team-oriented, database-backed |
| **claude-orchestra** | - | Lightweight, pip-only, session-aware |

**Why we exist despite the competition:**

1. **Session Discovery** - Our killer feature. We scan `~/.claude/projects/` to find and resume your existing Claude Code sessions. No other orchestrator does this. You can pick up exactly where you left off, or monitor sessions you started manually.

2. **Zero Infrastructure** - No Docker. No Postgres. No Redis. No YAML files. Just `pip install claude-orchestra && orchestra web`.

3. **Git-Native Isolation** - We use git worktrees for agent isolation. It's a pattern every developer already understands, and it creates natural PR boundaries.

**Who should use alternatives:**
- Need enterprise SSO/RBAC? Use claude-flow
- Need persistent agent memory across restarts? Use claude-squad
- Need to orchestrate 50+ agents? Use claude-flow

**Who should use us:**
- Want to run 2-5 agents on a project without setup hassle
- Want to monitor/resume Claude Code sessions from mobile
- Prefer understanding your tools over configuring them

---

## Commands

```bash
pip install -e ".[dev]"     # Install with dev deps
pytest                       # Run tests
orchestra --help             # CLI help
orchestra sessions           # List recent sessions
orchestra spawn              # Spawn parallel agents
orchestra status             # Show agent status
orchestra web                # Launch web dashboard
```

## What This Is

**Claude Orchestra** - The lightweight multi-agent orchestrator for Claude Code. No Docker, no databases, no complex setup. Just `pip install` and go.

**Core insight:** Most developers don't need enterprise orchestration. They need to run a few Claude agents in parallel without fighting infrastructure.

**What makes us different:**
- **Session discovery (our killer feature)** - Scan `~/.claude/projects/` to find, monitor, and resume any Claude Code session. Start a session manually, check on it from your phone later.
- **Worktree isolation** - Each agent works in a separate git worktree. No file conflicts, natural PR boundaries.
- **Zero dependencies** - Pure Python, pip-installable, works immediately.
- **Mobile-first dashboard** - Real-time monitoring designed for phones first, desktops second.
- **Permission bypass** - Configure auto-approve for autonomous operation when you trust the task.

---

## Architecture

```
orchestra/
├── cli.py              # Click CLI entry point
├── config.py           # Configuration management
├── core/
│   ├── session.py      # Session discovery & management
│   ├── worktree.py     # Git worktree operations
│   ├── agent.py        # Agent execution wrapper
│   └── state.py        # State persistence
└── dashboard/
    ├── server.py       # FastAPI web server
    ├── ws.py           # WebSocket handlers
    └── static/         # React SPA
```

### Key Classes

**SessionManager** (`core/session.py`)
- `find_recent(hours)` - Scan ~/.claude/projects/ for recent sessions
- `get_metadata(session_id)` - Parse JSONL for session info
- `resume(session_id, prompt)` - Resume session via Claude CLI

**WorktreeManager** (`core/worktree.py`)
- `create(branch, task)` - Create isolated worktree
- `list_active()` - List all worktrees
- `cleanup()` - Remove merged worktrees

**Orchestrator** (`core/agent.py`)
- `spawn(tasks, parallel)` - Start multiple agents
- `status()` - Get all agent statuses
- `collect()` - Gather results from agents

---

## Session Storage

Claude Code stores sessions at:
```
~/.claude/projects/<project-hash>/<session-id>.jsonl
```

Each JSONL file contains message history. We scan by modification time to find recent sessions.

---

## Git Worktree Pattern

```bash
# Main repo
/project/
├── .git/
├── src/
└── ...

# Worktrees created by orchestra
/project/.worktrees/
├── task-auth-refactor/    # Branch: orchestra/auth-refactor
├── task-perf-optimize/    # Branch: orchestra/perf-optimize
└── task-test-coverage/    # Branch: orchestra/test-coverage
```

Each worktree:
- Has its own branch (`orchestra/<task-name>`)
- Has isolated file state
- Can run Claude Code independently
- Creates PR when done (not direct merge)

---

## Configuration

Default config at `~/.config/claude-orchestra/config.json`:

```json
{
  "claude_projects_dir": "~/.claude/projects",
  "worktree_dir": ".worktrees",
  "default_parallel": 3,
  "heartbeat_interval": 60,
  "bypass_permissions": [
    "Bash(git *)",
    "Bash(npm *)",
    "Read(*)",
    "Glob(*)",
    "Grep(*)"
  ],
  "dashboard_port": 8888
}
```

---

## Development

### Adding a new CLI command

```python
# In cli.py
@main.command()
@click.argument("task")
def my_command(task: str):
    """Description of command."""
    # Implementation
```

### Adding a new API endpoint

```python
# In dashboard/server.py
@app.get("/api/my-endpoint")
async def my_endpoint():
    return {"status": "ok"}
```

### Testing

```bash
pytest tests/                    # All tests
pytest tests/test_session.py    # Single file
pytest -k "test_find"           # Pattern match
```

---

## Key Files

| File | Purpose |
|------|---------|
| `orchestra/cli.py` | CLI entry point |
| `orchestra/core/session.py` | Session discovery |
| `orchestra/core/worktree.py` | Git worktree management |
| `orchestra/core/agent.py` | Agent orchestration |
| `orchestra/dashboard/server.py` | Web API server |
| `orchestra/dashboard/static/index.html` | Dashboard SPA |
