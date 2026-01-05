# Claude Orchestra Quick Start

Get up and running with Claude Orchestra in 5 minutes.

## Installation

```bash
pip install claude-orchestra
```

Verify installation:

```bash
orchestra --version
```

## Example 1: Parallel Feature Development

Run 3 agents in parallel to develop different parts of a feature:

```bash
# Navigate to your project
cd my-project

# Initialize orchestra
orchestra init

# Spawn 3 agents working on different tasks
orchestra spawn \
  "implement user authentication REST API with JWT tokens" \
  "build user registration UI with form validation" \
  "write integration tests for authentication flow"

# Watch progress in real-time
orchestra status --watch

# Collect results when done
orchestra collect
```

**What happens:**
- Agent 1 works on REST API in `.worktrees/task-1/`
- Agent 2 works on UI in `.worktrees/task-2/`
- Agent 3 works on tests in `.worktrees/task-3/`
- Each agent has isolated file system via git worktree
- Progress visible in terminal with colored output
- When done, results are in separate branches ready for PRs

## Example 2: Performance Optimization Sprint

Run multiple optimization agents in parallel:

```bash
# Find recent work
orchestra sessions --hours 2

# Spawn optimization agents
orchestra spawn \
  "profile database queries with timing and identify N+1 problems" \
  "optimize the discovered queries and add caching layer" \
  "refactor request handlers to batch database calls"

# Monitor with web dashboard
orchestra web --port 8888
# Visit http://localhost:8888 in browser
```

**Features in dashboard:**
- Real-time agent status (running, completed, failed)
- Summary cards showing agent counts by status
- Agent spawn interface
- Pause/resume controls
- WebSocket updates every 2 seconds

## Example 3: Open Source Maintenance

Automate multiple bug fixes simultaneously:

```bash
# List recent sessions to resume if needed
orchestra sessions --json

# Spawn agents for different issues
orchestra spawn \
  "fix issue #42: add error handling for invalid input" \
  "fix issue #47: improve documentation for API endpoint" \
  "fix issue #51: add type hints to utility functions"

# Check status periodically
orchestra status

# Collect and review results
orchestra collect
```

## Configuration

Customize Orchestra behavior by editing `~/.config/claude-orchestra/config.json`:

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
    "Glob(*)",
    "Grep(*)",
    "Write(*)",
    "Edit(*)"
  ]
}
```

**Key settings:**
- `default_parallel`: Number of agents to spawn by default (1-8)
- `max_parallel`: Maximum agents allowed to run
- `bypass_permissions`: Operations auto-approved for autonomous agents
- `stale_threshold`: Mark agent as stale after N seconds of inactivity

## Common Commands

```bash
# Initialize orchestration in current project
orchestra init

# List recent Claude Code sessions
orchestra sessions --hours 4
orchestra sessions --json

# Spawn agents with specific tasks
orchestra spawn "task 1" "task 2" "task 3"

# Show agent status (updates every 2s)
orchestra status --watch

# Launch web dashboard
orchestra web --port 8888

# Collect results from completed agents
orchestra collect

# List active worktrees
orchestra worktrees

# Clean up completed agents
orchestra cleanup

# Get help
orchestra --help
orchestra spawn --help
```

## Workflow: From Spawn to Merge

```
1. orchestra spawn "task 1" "task 2"
   └─ Creates .worktrees/task-1/ and .worktrees/task-2/
   └─ Branches: orchestra/task-1, orchestra/task-2

2. orchestra status --watch
   └─ Monitor progress in terminal
   └─ Or use: orchestra web

3. orchestra collect
   └─ Gather results, show status
   └─ Agent branches ready for pull requests

4. Create PRs from orchestra/task-* branches
   └─ Review and merge when ready
   └─ Each agent's work isolated and testable

5. orchestra cleanup
   └─ Remove completed worktrees and branches
   └─ Clean up state
```

## Troubleshooting

**Q: Agents not spawning?**
- Ensure Claude Code CLI is installed: `claude --version`
- Check session directory: `ls ~/.claude/projects/`

**Q: Dashboard not loading?**
- Verify port is available: `lsof -i :8888`
- Try different port: `orchestra web --port 9999`

**Q: Worktrees not cleaned up?**
- Manual cleanup: `git worktree list` and `git worktree remove <path>`

**Q: Need to resume an interrupted agent?**
- Find the session: `orchestra sessions --json`
- Create new agent with directive to continue work

## Next Steps

- Read [CLAUDE.md](../CLAUDE.md) for architecture details
- Check [CONTRIBUTING.md](../CONTRIBUTING.md) for development setup
- Explore CLI help: `orchestra --help`
- Join the community for questions and feedback
