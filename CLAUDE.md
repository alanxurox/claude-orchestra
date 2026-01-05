# CLAUDE.md - Claude Orchestra

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

**Claude Orchestra** - Multi-agent orchestration tool for Claude Code with git worktree isolation.

**Core insight:** Parallel AI agents need isolated working directories to avoid conflicts. Git worktrees provide this isolation naturally.

**Key features:**
- Session discovery - Find and resume recent Claude Code sessions
- Worktree isolation - Each agent works in separate git worktree
- Parallel execution - Run multiple agents on different tasks simultaneously
- Web dashboard - Mobile-friendly real-time monitoring
- Permission bypass - Configure auto-approve for autonomous operation

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
