# Launch Day Posts - Ready to Copy/Paste

*Last updated: January 2026*

---

## 1. HackerNews Show HN (Priority #1)

**When:** Monday morning EST (best performance)

**Title:**
```
Show HN: Session discovery for Claude Code - find and resume any session
```

**Body (copy exactly):**
```
I built Claude Orchestra after getting frustrated with the existing orchestration options.

The market has great tools - claude-flow (11k stars) and claude-squad (5.5k stars) are both excellent. But they're built for teams with DevOps resources. claude-flow needs Docker and FalkorDB. claude-squad is a compiled Go binary.

I just wanted to run 2-3 Claude agents in parallel on weekend projects.

What Claude Orchestra is:

- pip install claude-orchestra (that's the whole setup)
- Spawn parallel agents with git worktree isolation
- Mobile-friendly web dashboard
- ~1,800 lines of Python you can read and modify

Our actual differentiator - Session Discovery:

Claude Code stores sessions in ~/.claude/projects/, but there's no way to browse them. Orchestra scans this directory and shows your recent sessions:

    orchestra sessions --hours 24

Resume any session instantly. Never lose context on what you were working on. No other tool does this.

When to use us vs. alternatives:

- Use claude-flow if you need enterprise SSO/RBAC or 50+ agents.
- Use claude-squad if you need persistent agent memory across restarts.
- Use Orchestra if you want pip-install simplicity and session discovery.

Quick start:

    pip install claude-orchestra
    orchestra init
    orchestra sessions  # see recent work
    orchestra spawn "task 1" "task 2"
    orchestra web  # dashboard

We're honest about being the lightweight alternative, not the most powerful. Happy to answer questions about the design tradeoffs.

GitHub: https://github.com/alanxurox/claude-orchestra
```

---

## 2. Reddit r/ClaudeCode (Priority #2)

**When:** Evening/weekend for better engagement

**Title:**
```
[Tool] Session Discovery for Claude Code - find and resume any session + parallel agents
```

**Body:**
```
Hey r/ClaudeCode! Sharing something I built for the community.

**The problem I had:**
1. Lost track of Claude Code sessions constantly - they're buried in ~/.claude/projects/
2. Wanted to run 2-3 parallel agents without Docker/database setup

**What I built:**

`claude-orchestra` - the lightweight Claude orchestrator

**Session Discovery (unique feature):**

    orchestra sessions --hours 24

Scans ~/.claude/projects/ and shows ALL your recent sessions. Resume any of them. Never lose context again.

**Parallel Agents:**

    orchestra spawn "implement auth" "write tests" "optimize queries"

Each agent runs in a git worktree - isolated files, no conflicts.

**What makes it different:**
- pip install (no Docker, no databases, no YAML)
- Session discovery (no other tool does this)
- 1,800 lines of readable Python
- Mobile-friendly web dashboard

**What it's NOT:**
- Not enterprise-grade (use claude-flow for that - 11k stars, excellent tool)
- Not for 50+ agents (designed for 2-8)
- Not the most powerful (we're the most accessible)

**Quick start:**

    pip install claude-orchestra
    orchestra init
    orchestra sessions
    orchestra web

**Links:**
- GitHub: https://github.com/alanxurox/claude-orchestra
- Docs: See README for full API

Happy to answer questions and take feedback. Built this for my own workflow but hoping others find it useful.
```

---

## 3. Reddit r/ClaudeAI (Priority #3)

**When:** Same day as r/ClaudeCode post

**Title:**
```
Built a tool to find and resume your Claude Code sessions + run parallel agents (no Docker)
```

**Body:**
```
For those using Claude Code (the CLI), I built a lightweight orchestrator.

**The pitch:** Ever close your laptop and forget what Claude session you were working on? Sessions are stored in ~/.claude/projects/ but there's no way to browse them. Until now.

**Session Discovery:**

    pip install claude-orchestra
    orchestra sessions --hours 24

Shows all your recent Claude Code sessions. Click to resume. Never lose context.

**Parallel Agents:**

    orchestra spawn "task 1" "task 2" "task 3"

Each agent works in a git worktree - isolated file state, no conflicts.

**Why I built this:**

The existing tools (claude-flow with 11k stars, claude-squad with 5.5k stars) are excellent but need Docker and databases. I wanted something simpler for weekend projects.

**What it's good for:**
- Solo developers running 2-5 parallel agents
- Finding/resuming old sessions
- Mobile monitoring (web dashboard)

**What it's NOT good for:**
- Enterprise (use claude-flow)
- 50+ agents (use claude-flow)
- Persistent memory across restarts (use claude-squad)

GitHub: https://github.com/alanxurox/claude-orchestra

Honest positioning: we're the lightweight alternative. Happy to take feedback!
```

---

## 4. Twitter Thread (Priority #4)

**When:** US business hours, after HN post goes live

**Tweet 1:**
```
Ever lost track of a Claude Code session you started yesterday?

You close your laptop, forget the project, and can't remember where you left off.

Your session history is buried in ~/.claude/projects/ - completely invisible.

We fixed this. 🧵
```

**Tweet 2:**
```
The Claude orchestration space has exploded:

- claude-flow (11k stars) - enterprise-grade, Docker + databases
- claude-squad (5.5k stars) - Go binary, database-backed

Great tools. But installing Docker just to run 2-3 parallel agents?

We wanted something simpler.
```

**Tweet 3:**
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

**Tweet 4:**
```
Our killer feature: Session Discovery

orchestra sessions --hours 24

Scans ~/.claude/projects/ and shows ALL your recent Claude Code sessions.

Resume any session. Never lose context again.

No other orchestrator does this.
```

**Tweet 5:**
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

**Tweet 6:**
```
We're the underdog. 0 stars vs 11k.

But if you want:
- Simple pip install
- Session discovery (unique to us)
- 2-5 parallel agents without DevOps overhead
- A codebase you can actually read

Try it:
pip install claude-orchestra

github.com/alanxurox/claude-orchestra
```

---

## 5. Discord - Claude Developers Server

**Channel:** #showcase or #claude-code

**Message:**
```
Hey everyone! Built something for the Claude Code community.

**Claude Orchestra** - session discovery + parallel agents

The unique feature: `orchestra sessions --hours 24` scans ~/.claude/projects/ and shows ALL your recent Claude Code sessions. Resume any of them instantly.

Also does parallel agents with git worktree isolation (no file conflicts).

Why I built it: claude-flow and claude-squad are great but need Docker/databases. I wanted something simpler for weekend projects.

What it's good for:
- Finding/resuming Claude Code sessions (unique feature)
- Running 2-5 parallel agents
- Mobile monitoring

pip install claude-orchestra

GitHub: https://github.com/alanxurox/claude-orchestra

Happy to answer questions! Built this for my own workflow.
```

---

## Launch Day Checklist

### Pre-Launch (Day Before)

- [ ] Run `pytest` - all tests passing
- [ ] Verify `pip install claude-orchestra` works (test in clean env)
- [ ] Check README renders correctly on GitHub
- [ ] Verify demo commands work: `orchestra sessions`, `orchestra web`
- [ ] Screenshots ready for social posts

### Launch Day (Monday)

**Morning (EST):**
- [ ] Post to HackerNews (Show HN)
- [ ] Monitor HN for questions, respond quickly and genuinely
- [ ] Don't ask anyone to upvote (HN detects this)

**Afternoon:**
- [ ] Post Twitter thread (after HN gains traction)
- [ ] Engage with any replies/quotes

**Evening:**
- [ ] Post to r/ClaudeCode
- [ ] Post to r/ClaudeAI
- [ ] Monitor and respond to all comments

### Post-Launch (Week 1)

- [ ] Respond to ALL GitHub issues within 24 hours
- [ ] Thank everyone who stars or contributes
- [ ] Post Discord announcement
- [ ] Write a follow-up blog post if HN does well

---

## Key Reminders

1. **Be genuine** - don't use marketing language
2. **Be humble** - acknowledge competitors are excellent
3. **Be responsive** - reply to every comment quickly
4. **Be honest** - admit limitations ("not for 50+ agents")
5. **Don't ask for upvotes** - ever

The unique angle is **Session Discovery**. Lead with that problem.
