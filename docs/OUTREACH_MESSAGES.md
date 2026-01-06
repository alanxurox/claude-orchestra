# First 10 Outreach Messages

*Personalized, ready-to-send messages for key targets*

---

## Principles

1. **Give before you ask** - Engage genuinely first, pitch later
2. **Be specific** - Reference their work directly
3. **Be brief** - Respect their time
4. **No mass templates** - Each message is personalized
5. **Don't lead with the pitch** - Lead with value or shared interest

---

## Target 1: Boris Cherny (@bcherny)

**Context:** Creator of Claude Code at Anthropic. His workflow reveal went viral.

**Strategy:** Do NOT pitch directly. Instead, build something that extends his workflow and share it publicly. If he notices organically, that's the win.

**Pre-Engagement (Tweet reply on his content):**
```
Fascinating approach to the 259 PR workflow. Question: do you track which sessions led to which PRs, or is it more ad-hoc?

I've been building a session discovery tool to browse ~/.claude/projects/ - helps me find where I left off on different branches.
```

**Note:** This is NOT a pitch. It's a genuine question with context about what you're building. If he responds, continue the conversation naturally. If he shows interest, share the link. Never force it.

---

## Target 2: Eduardo Lugo (@eduardojld)

**Context:** Wrote "Subagent Orchestration with Claude Code" on Medium

**Twitter DM (only after engaging publicly first):**
```
Hey Eduardo - loved your piece on subagent orchestration. The newsroom example was clever.

I've been working on something adjacent: a lightweight orchestrator with session discovery (finding sessions in ~/.claude/projects/). Different angle from your approach but same problem space.

Would be curious your thoughts if you have 5 min to check it out: [GitHub link]

No pressure either way - just thought you might find it interesting given your work in this area.
```

---

## Target 3: Carl Vellotti

**Context:** 55k followers, Claude Code tutorial creator, covers parallel agents

**Twitter DM (after engaging with 2-3 of his tutorials):**
```
Hey Carl - been watching your Claude Code content. Your parallel agents tutorial was especially useful.

Built something you might find interesting: a pip-installable orchestrator with session discovery. The session discovery piece scans ~/.claude/projects/ to find/resume any session - couldn't find another tool that does this.

If you ever need a topic for a video, happy to provide a demo/walkthrough. No expectations either way.

[GitHub link]
```

---

## Target 4: Reddit r/ClaudeCode Top Contributors

**Strategy:** Don't DM. Post publicly with technical depth. Engage in comments.

**Comment on "Looking for orchestration solutions" threads:**
```
Built something for this: claude-orchestra.

It's a lightweight alternative to claude-flow/claude-squad - no Docker, no databases, just pip install.

The unique feature is session discovery: `orchestra sessions --hours 24` scans ~/.claude/projects/ and shows all your recent Claude Code sessions. Resume any of them.

Not enterprise-grade, but if you want simplicity for 2-5 agents: https://github.com/alanxurox/claude-orchestra

Happy to answer questions about the implementation.
```

---

## Target 5: Discord Claude Developers - Power Users

**Strategy:** Be active first. Answer questions for a week. Then share.

**After establishing presence (in #claude-code channel):**
```
Hey all - been lurking for a while, wanted to share something I built.

**Claude Orchestra** - session discovery + parallel agents

Main feature: `orchestra sessions` scans ~/.claude/projects/ and shows all your recent sessions. Couldn't find another tool that does this, so I built it.

Also does parallel agents with git worktree isolation.

pip install claude-orchestra

https://github.com/alanxurox/claude-orchestra

It's lightweight (no Docker/databases) - designed for solo devs running 2-5 agents, not enterprise. Happy to take feedback!
```

---

## Target 6: Cursor AI Discord Community

**Strategy:** Position as complementary to Cursor workflow

**Message in #showcase or #tools:**
```
For those using Cursor + Claude Code together:

Built a session manager called claude-orchestra. Main feature: browse and resume Claude Code sessions from ~/.claude/projects/.

Why this matters for Cursor users:
- Terminal Claude Code sessions from within Cursor
- Track which sessions were in which projects
- Resume interrupted work easily

pip install claude-orchestra
orchestra sessions --hours 24

GitHub: https://github.com/alanxurox/claude-orchestra

Works alongside Cursor, not a replacement. Let me know if you try it!
```

---

## Target 7: AI Foundations YouTube Channel

**Email (if contact available) or Twitter DM:**
```
Hi [Name],

I follow your YouTube channel - your practical AI workflow content is great.

Built a tool your audience might find useful: claude-orchestra - a pip-installable orchestrator for Claude Code with session discovery.

The session discovery feature scans ~/.claude/projects/ to find/resume any Claude Code session. No other tool does this.

If you're ever looking for content topics, I'd be happy to:
- Provide a demo walkthrough
- Write a script outline
- Answer any questions about the implementation

No pressure either way. Just thought it might fit your practical workflow format.

GitHub: https://github.com/alanxurox/claude-orchestra

Best,
[Name]
```

---

## Target 8: Dev.to/Hashnode Writers

**Strategy:** Cross-post a technical article, not a pitch

**Article title:**
```
Building Session Discovery for Claude Code: Scanning ~/.claude/projects/
```

**Article approach:**
- 80% educational content about how Claude Code stores sessions
- 20% introduction of your tool as the solution
- Include code snippets, architecture decisions
- End with link to GitHub

---

## Target 9: Indie Hackers Forum

**Post in relevant thread or new post:**
```
Title: Built a session manager for Claude Code (my weekend project → useful tool)

Body:
Hey IH!

Been using Claude Code heavily for my projects. Got frustrated losing track of sessions - they're stored in ~/.claude/projects/ but there's no way to browse them.

Built a tool to fix it: claude-orchestra

**Session Discovery:**
orchestra sessions --hours 24
→ Shows all recent Claude Code sessions, resume any of them

**Parallel Agents:**
orchestra spawn "task 1" "task 2"
→ Each runs in git worktree, no conflicts

**Stats:**
- ~1,800 lines of Python
- pip install, no Docker
- Designed for solo devs running 2-5 agents

Not trying to compete with claude-flow (11k stars) - they're enterprise-grade. This is the lightweight alternative.

GitHub: https://github.com/alanxurox/claude-orchestra

Would love feedback from other devs using Claude Code!
```

---

## Target 10: HackerNews (via Show HN)

**See LAUNCH_READY.md for full post**

**Follow-up comments to prepare:**

When asked "How is this different from X?":
```
Great question. claude-flow is excellent for enterprise - 64 agents, FalkorDB backend, Docker infrastructure.

We're the opposite end:
1. pip install only (no Docker)
2. Session discovery (unique - no other tool scans ~/.claude/projects/)
3. Designed for 2-8 agents, not enterprise scale

Pick based on your needs. If you need enterprise features, use claude-flow. If you want simplicity and session discovery, try us.
```

When asked about technical implementation:
```
Happy to go deep:

1. Session discovery: We scan ~/.claude/projects/ for JSONL files. Each session is a separate file with full message history. Parse for metadata (project path, last prompt, message count).

2. Agent isolation: Git worktrees. Native git feature - each agent gets its own working tree and branch. No file conflicts, natural PR boundaries.

3. Dashboard: FastAPI + WebSocket for real-time updates. Designed mobile-first because I check on agents from my phone.

~1,800 lines total. Happy to answer specific questions about any component.
```

---

## General Templates

### When Someone Shows Interest

```
Thanks for checking it out! Let me know if you run into any issues - actively fixing things this week.

If you have feature requests, GitHub issues are the best place: [link]
```

### When Asked for Comparison

```
Honest take: [competitor] is excellent for [their use case].

We focused on:
- pip-only install (no infrastructure)
- Session discovery (unique feature)
- 2-8 agents (not enterprise scale)

Use what fits your workflow. Both are open source!
```

### When Getting Criticism

```
Fair point. We're definitely not the right tool for [their concern].

If you need [enterprise feature], claude-flow is probably better for your use case.

We're intentionally lightweight - tradeoff for simplicity.
```

---

## Timing Guide

| Target | When | Notes |
|--------|------|-------|
| Boris Cherny | After launch gains traction | Organic only, never pitch |
| Eduardo Lugo | After 2-3 public engagements | DM with specific reference |
| Carl Vellotti | After engaging with content | Offer collaboration, not ask |
| r/ClaudeCode | Evening/weekend | Technical depth matters |
| Discord | After 1 week of participation | Build reputation first |
| YouTube creators | After HN traction | Email with materials ready |
| Dev.to | Any time | Cross-post educational content |
| Indie Hackers | After some external validation | Mention HN reception if good |
| HackerNews | Monday morning EST | Primary launch channel |
