# Claude Orchestra Launch Materials

## 1. Twitter/X Thread (6 Tweets)

### Tweet 1 - Hook
```
Ever lost track of a Claude Code session you started yesterday?

You close your laptop, forget the project, and can't remember where you left off.

Your session history is buried in ~/.claude/projects/ - completely invisible.

We fixed this. (thread)
```

### Tweet 2 - Problem Expansion
```
The Claude orchestration space has exploded:

- claude-flow (11k stars) - enterprise-grade, Docker + databases
- claude-squad (5.5k stars) - Go binary, database-backed

Great tools. But installing Docker just to run 2-3 parallel agents?

We wanted something simpler.
```

### Tweet 3 - Solution
```
Introducing Claude Orchestra

The lightweight Claude orchestrator:
- pip install and go
- No Docker
- No databases
- No config files
- Just Python + git

1,800 lines of readable code you can actually understand.
```

### Tweet 4 - Differentiator (Session Discovery)
```
Our killer feature: Session Discovery

orchestra sessions --hours 24

Scans ~/.claude/projects/ and shows ALL your recent Claude Code sessions.

Resume any session. Never lose context again.

No other orchestrator does this.
```

### Tweet 5 - Demo
```
Quick demo:

pip install claude-orchestra
cd your-project
orchestra init
orchestra sessions  # what have I been working on?
orchestra spawn "add auth" "write tests" "fix perf"
orchestra web  # mobile-friendly dashboard

That's it. No YAML, no Docker Compose.
```

### Tweet 6 - Call to Action
```
We're the underdog. 0 stars vs 11k.

But if you want:
- Simple pip install
- Session discovery (unique to us)
- 2-5 parallel agents without DevOps overhead
- A codebase you can actually read

Try it:
pip install claude-orchestra

Star us: github.com/alanxurox/claude-orchestra
```

---

## 2. HackerNews "Show HN" Post

### Title Options

**Option A (Problem-focused):**
```
Show HN: Session discovery for Claude Code - find and resume any session
```

**Option B (Positioning):**
```
Show HN: Claude Orchestra - The pip-installable alternative to claude-flow
```

**Option C (Direct):**
```
Show HN: Lightweight multi-agent orchestration for Claude Code (no Docker)
```

### Body Copy

```
I built Claude Orchestra after getting frustrated with the existing orchestration options.

The market has great tools - claude-flow (11k stars) and claude-squad (5.5k stars) are both excellent. But they're built for teams with DevOps resources. claude-flow needs Docker and FalkorDB. claude-squad is a compiled Go binary.

I just wanted to run 2-3 Claude agents in parallel on weekend projects.

**What Claude Orchestra is:**

- pip install claude-orchestra (that's the whole setup)
- Spawn parallel agents with git worktree isolation
- Mobile-friendly web dashboard
- ~1,800 lines of Python you can read and modify

**Our actual differentiator - Session Discovery:**

Claude Code stores sessions in ~/.claude/projects/, but there's no way to browse them. Orchestra scans this directory and shows your recent sessions:

    orchestra sessions --hours 24

Resume any session instantly. Never lose context on what you were working on.

No other tool does this.

**When to use us vs. alternatives:**

Use claude-flow if you need enterprise SSO/RBAC or 50+ agents.
Use claude-squad if you need persistent agent memory across restarts.
Use Orchestra if you want pip-install simplicity and session discovery.

**Quick start:**

    pip install claude-orchestra
    orchestra init
    orchestra sessions  # see recent work
    orchestra spawn "task 1" "task 2"
    orchestra web  # dashboard

We're honest about being the lightweight alternative, not the most powerful. Happy to answer questions about the design tradeoffs.

GitHub: https://github.com/alanxurox/claude-orchestra
```

### Anticipated Questions and Answers

**Q: How is this different from claude-flow?**
```
claude-flow is enterprise-grade: 64-agent orchestration, FalkorDB backend,
Docker infrastructure. Orchestra is the opposite - zero infrastructure,
pip install only, designed for 2-5 agents. We also have session discovery
(scanning ~/.claude/projects/) which claude-flow doesn't do.

Pick claude-flow for enterprise. Pick us for simplicity.
```

**Q: Why not just use tmux/screen with Claude Code?**
```
You could, but you lose:
1. Git worktree isolation (agents editing same files = conflicts)
2. Session discovery across projects
3. Dashboard for mobile monitoring
4. Centralized status/coordination

If you're running one agent, tmux is fine. For parallel work, you need isolation.
```

**Q: What's the catch? Why is this free/simple?**
```
No catch. It's 1,800 lines of Python. The "magic" is just:
1. Scanning ~/.claude/projects/ for JSONL files (session discovery)
2. Using git worktrees for isolation (native git feature)
3. FastAPI + WebSocket for the dashboard

We're not building a business. Just scratching our own itch.
```

**Q: How does this compare to Anthropic's official tools?**
```
Anthropic provides the Claude Agent SDK and CLI. Orchestra builds on top of
Claude Code (the CLI). We're not replacing Anthropic's tools - we're adding
orchestration and session discovery for developers using Claude Code.
```

**Q: Can it handle 50+ agents?**
```
Probably not well. We're designed for 2-8 agents. If you need massive
parallelism, use claude-flow - it's built for that scale with proper
infrastructure.
```

**Q: Why Python instead of Go/Rust like the alternatives?**
```
Most developers using Claude Code are building Python/JS projects.
pip install is the most accessible distribution method for our audience.
Plus, 1,800 lines of Python is easier to understand and modify than compiled binaries.
```

---

## 3. Slack/Discord Announcements

### Short Version (Company/Team Channel)

```
New tool for Claude Code users: Claude Orchestra

The lightweight orchestrator for running parallel Claude agents.

Key thing: Session Discovery - finally browse and resume your Claude Code sessions.

pip install claude-orchestra
orchestra sessions  # see recent sessions
orchestra spawn "task1" "task2"  # parallel agents

No Docker, no databases, just pip install.

GitHub: github.com/alanxurox/claude-orchestra
```

### Longer Version (Claude Code Community)

```
Hey everyone - sharing a tool I built for the community.

**Claude Orchestra** - The lightweight Claude orchestrator

I got frustrated that:
1. There was no way to see/resume my recent Claude Code sessions
2. Running parallel agents required Docker/databases (claude-flow, claude-squad)

So I built a simple alternative.

**Session Discovery (our unique feature):**
orchestra sessions --hours 24
^ Shows all your recent Claude Code sessions from ~/.claude/projects/
Resume any of them instantly.

**Parallel Agents:**
orchestra spawn "implement auth" "write tests" "optimize queries"
^ Each agent runs in a git worktree - isolated files, no conflicts.

**What makes us different:**
- pip install (no Docker, no databases)
- Session discovery (no other tool does this)
- 1,800 lines of readable Python
- Mobile-friendly web dashboard

**What we're NOT:**
- Not enterprise-grade (use claude-flow for that)
- Not for 50+ agents (designed for 2-8)
- Not the most powerful (we're the most accessible)

**Quick start:**
pip install claude-orchestra
orchestra init
orchestra sessions
orchestra web

We're the underdog at 0 stars vs claude-flow's 11k. But if you value simplicity and want session discovery, give us a try.

GitHub: github.com/alanxurox/claude-orchestra
PyPI: pypi.org/project/claude-orchestra

Happy to answer questions!
```

---

## 4. LinkedIn Post

```
Excited to share a developer productivity tool I've been working on.

**The Problem:**
AI coding assistants like Claude Code are powerful, but orchestrating multiple agents in parallel requires complex infrastructure - Docker, databases, configuration files. Plus, there's no easy way to find and resume your previous sessions.

**The Solution:**
Claude Orchestra - a lightweight orchestrator that's just `pip install` and go.

Key features:
- Session Discovery: Finally browse and resume your Claude Code sessions
- Parallel Execution: Spawn multiple agents with git worktree isolation
- Zero Setup: No Docker, no databases, no YAML configs
- Mobile Dashboard: Check on your agents from your phone

**Why it matters for developer productivity:**
Instead of spending an hour setting up infrastructure, you can have parallel AI agents working on your codebase in 2 minutes:

pip install claude-orchestra
orchestra spawn "implement auth" "add tests" "fix performance"

Each agent works in isolation, creates its own PR when done, and you monitor everything from a simple dashboard.

**The honest positioning:**
This isn't competing with enterprise tools like claude-flow (11k GitHub stars). It's the lightweight alternative for developers who want simplicity over features.

If you're using Claude Code for development and want to run parallel agents without the overhead, check it out:
github.com/alanxurox/claude-orchestra

#DeveloperProductivity #AI #Python #OpenSource #Claude
```

---

## 5. Key Messages

### One-Liner

```
Claude Orchestra is the pip-installable orchestrator with session discovery -
run parallel Claude agents without Docker, databases, or config files.
```

### Elevator Pitch (30 seconds)

```
"You know how Claude Code sessions just disappear into ~/.claude/projects/ with
no way to find them later? And running multiple agents in parallel requires
Docker and database setup?

Claude Orchestra fixes both. It's a pip-installable Python tool that:
1. Discovers all your recent Claude sessions so you can resume them
2. Spawns parallel agents with git worktree isolation
3. Provides a mobile-friendly dashboard

No Docker, no databases. Just 'pip install claude-orchestra' and you're running
parallel agents in 2 minutes. We're the lightweight alternative for developers
who don't need enterprise infrastructure."
```

### Feature Bullets

**Core Features:**
- Session Discovery - Scan ~/.claude/projects/ to find and resume any Claude Code session
- Parallel Agents - Spawn 2-8 agents working simultaneously on different tasks
- Git Worktree Isolation - Each agent has isolated file state, no conflicts
- Mobile Dashboard - Real-time monitoring designed for phones first
- Permission Bypass - Configure auto-approve for autonomous operation

**What Sets Us Apart:**
- Zero Infrastructure - No Docker, no databases, no Redis
- pip Install - `pip install claude-orchestra` is the entire setup
- Session Discovery - Unique feature no other orchestrator has
- Readable Codebase - 1,800 lines of Python you can understand and modify
- Honest Positioning - We know we're the lightweight alternative, not the most powerful

**When to Choose Us:**
- Running 2-5 parallel agents on a project
- Want to discover/resume Claude Code sessions
- Prefer simplicity over enterprise features
- Want to understand and modify your tools
- Don't want to set up Docker/databases for a weekend project

**When to Choose Alternatives:**
- Need enterprise SSO/RBAC (use claude-flow)
- Need persistent agent memory across restarts (use claude-squad)
- Orchestrating 50+ agents (use claude-flow)
- Need maximum performance (use ccswarm)

---

## Quick Reference

| Asset | Key Hook |
|-------|----------|
| Twitter | "Ever lost track of a Claude Code session?" |
| HN | "pip-installable alternative, session discovery unique to us" |
| Discord | "Session discovery - finally browse your Claude Code sessions" |
| LinkedIn | "Developer productivity - parallel agents in 2 minutes" |

| Competitor | Their Strength | Our Counter |
|------------|---------------|-------------|
| claude-flow (11k stars) | Enterprise, 64 agents | We're simple, no Docker |
| claude-squad (5.5k stars) | Team features, persistence | We're pip-only, session discovery |

| Our Unique Angle | Why It Matters |
|------------------|----------------|
| Session Discovery | No other tool finds/resumes Claude sessions |
| pip-only install | 2 minutes to running, not 2 hours |
| 1,800 lines | You can read and modify the code |
| Mobile dashboard | Check agents from your phone |
