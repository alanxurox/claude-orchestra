# Claude Orchestra: The Lightweight Alternative

## The Landscape

Let's be honest: **Claude Code orchestration is a crowded space**. Tools like claude-flow (11k+ stars), claude-squad (5k+ stars), ccswarm, and even AWS's official CLI Agent Orchestrator already exist. They're battle-tested. They work.

So why does Claude Orchestra exist?

## The Problem We Solve

After trying the existing tools, we found a common pattern:

- **claude-flow**: Enterprise-grade, 64-agent support, but requires FalkorDB and complex setup
- **claude-squad**: Production-ready Go binary, but opaque if you need to customize
- **ccswarm**: Rust-native, fast, but requires Rust toolchain knowledge

These are excellent tools for teams with DevOps support. But what about the solo developer who just wants to:
1. See their recent Claude sessions in one place
2. Spin up 2-3 parallel agents without reading 50 pages of docs
3. Watch progress from their phone while grabbing coffee

## Our Actual Differentiators

### 1. Session Discovery (Our Killer Feature)

```bash
orchestra sessions --hours 24
```

This scans `~/.claude/projects/` to find and display your recent Claude Code sessions. No other tool does this. Resume any session instantly. Never lose context again.

### 2. Zero-Dependency Simplicity

```bash
pip install claude-orchestra
orchestra spawn "build auth" "write tests"
```

That's it. No Docker. No databases. No config files. Just Python and git.

### 3. Lightweight by Design

- **1,800 lines** of clean Python (vs. 10k+ in enterprise alternatives)
- **Pure Python** - modify it, extend it, understand it
- **Mobile-friendly dashboard** - check agent status from anywhere

### 4. Python-Native

If your stack is Python, Orchestra fits naturally. No Go binaries, no Rust compilation, no Node.js runtime. Just `pip install` and go.

## What We Use

Like other tools in this space, we use **git worktrees** for agent isolation. This isn't unique - ccswarm and claude-squad use them too. It's simply the right solution: each agent gets an isolated working directory, no file conflicts, clean PR-based merges.

## When to Choose Orchestra

| Choose Orchestra if... | Choose Alternatives if... |
|------------------------|---------------------------|
| You want `pip install` simplicity | You need 10+ parallel agents |
| You want to see/resume recent sessions | You need enterprise auth & audit |
| You prefer readable Python code | You need maximum performance |
| You're a solo dev or small team | You have dedicated DevOps |
| You want a mobile-friendly dashboard | You need CLI-only operation |

## The Build

| Phase | What |
|-------|------|
| Core | Session discovery from ~/.claude/projects/ |
| CLI | 8 commands, Click-based, zero-config |
| Dashboard | FastAPI + WebSockets, mobile-responsive |
| Isolation | Git worktree management, auto-cleanup |

**Stack**: Python 3.10+, Click, FastAPI, Rich, Git

## Quick Start

```bash
# Install
pip install claude-orchestra

# See your recent sessions (the feature nobody else has)
orchestra sessions

# Spawn parallel agents
orchestra spawn "implement auth" "write tests" "optimize queries"

# Watch from anywhere
orchestra web  # Opens mobile-friendly dashboard
```

## The Vision

We're not trying to be the most powerful orchestrator. We're trying to be the **most accessible** one.

- **v0.1** - Works today: spawn, status, sessions, dashboard
- **v0.2** - Result aggregation, agent communication
- **v1.0** - The go-to lightweight orchestrator for Python developers

## One-Liner

> "Claude Orchestra is the lightweight, pip-installable alternative for developers who want multi-agent orchestration without the enterprise complexity - plus the only tool that discovers and resumes your existing Claude sessions."

## Try It

```bash
pip install claude-orchestra
orchestra sessions  # See what you've been working on
orchestra spawn "your first parallel task"
```

---

**TL;DR**: In a market with powerful enterprise orchestrators, we chose simplicity. Session discovery you can't get elsewhere. Zero-config setup. 1,800 lines you can actually read. For developers who want parallel Claude agents without the overhead.
