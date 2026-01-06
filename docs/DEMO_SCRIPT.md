# Claude Orchestra Demo Scripts

Production-ready scripts for video demos. Fast-paced, developer-focused, no fluff.

---

## 60-Second Demo Script

### Target Audience
Developers who already use Claude Code and juggle multiple agent sessions.

### Script

| Time | Section | Voice-Over | Screen |
|------|---------|------------|--------|
| **0-3s** | Hook | "Ever lost track of a Claude Code conversation?" | Black screen, text fades in |
| **3-10s** | Hook cont. | "That brilliant refactoring session from Tuesday? Gone. That auth fix? Who knows which terminal." | Quick cuts: multiple terminal windows, confused scrolling |
| **10-15s** | Problem | "Claude Code is powerful. But managing multiple sessions?" | Show 4+ terminal windows with different Claude sessions |
| **15-25s** | Problem cont. | "It's chaos. No search. No history. No way to find what you need." | Frantically switching between terminals, scrolling up endlessly |
| **25-30s** | Solution intro | "Meet Claude Orchestra." | Clean terminal, type: `pip install claude-orchestra` |
| **30-35s** | Solution | "One command. All your sessions." | Type: `orchestra sessions` - show clean session list |
| **35-40s** | Key feature | "Search across everything." | Type: `orchestra search "authentication bug"` - results appear |
| **40-45s** | Key feature | "Spawn parallel agents in seconds." | Type: `orchestra spawn "refactor auth" "write tests" "update docs"` |
| **45-50s** | Magic moment | "Session discovery finds sessions you forgot existed." | Type: `orchestra discover` - watch it find 12 hidden sessions |
| **50-55s** | Magic cont. | "Even crashed ones. Even from last month." | Highlight recovered sessions with timestamps |
| **55-58s** | CTA | "Claude Orchestra. Because your conversations matter." | Logo + GitHub URL |
| **58-60s** | CTA | "pip install claude-orchestra. Link in description." | `pip install claude-orchestra` in large text |

### Production Notes
- Use a dark terminal theme (Dracula or similar)
- Keep typing speed fast but readable (~80 WPM)
- Add subtle keyboard sounds
- Background music: upbeat electronic, low volume

---

## 3-Minute Tutorial Script

### Overview
Deep dive tutorial for developers ready to adopt Claude Orchestra.

---

### Segment 1: Installation (0:00 - 0:25)

**Voice-Over:**
> "Let's get Claude Orchestra running in under 30 seconds. Python 3.10 or higher, that's it."

**Terminal Commands:**
```bash
# Show on screen with typing animation
pip install claude-orchestra

# Verify installation
orchestra --version
# Output: claude-orchestra 0.1.0
```

**Screen Notes:**
- Start with empty terminal
- Show pip installation completing (speed up if needed)
- Flash version number confirmation

**Timing Breakdown:**
- 0:00-0:05 - Intro sentence
- 0:05-0:15 - pip install (can speed up)
- 0:15-0:25 - Version check, transition

---

### Segment 2: Session Discovery (0:25 - 0:55)

**Voice-Over:**
> "First, let's find your sessions. orchestra sessions shows everything Claude Code has running."

**Terminal Commands:**
```bash
orchestra sessions
```

**Expected Output:**
```
CLAUDE ORCHESTRA - Session Manager
===================================

Active Sessions (3):
  [1] abc123  2 min ago   ~/projects/api      "Working on auth middleware"
  [2] def456  15 min ago  ~/projects/frontend "React component refactor"
  [3] ghi789  1 hour ago  ~/projects/cli      "CLI argument parsing"

Recent Sessions (12):
  [4] jkl012  Yesterday   ~/projects/api      "Database migration"
  [5] mno345  2 days ago  ~/projects/tests    "Integration test suite"
  ...

Use 'orchestra attach <id>' to reconnect
```

**Voice-Over (continued):**
> "Active sessions at the top. Recent history below. Every conversation, organized."

**Screen Notes:**
- Highlight the session list appearing
- Briefly hover over the "2 min ago" timestamp
- Show the working directory column

**Timing Breakdown:**
- 0:25-0:30 - Intro to sessions command
- 0:30-0:45 - Show output, let it breathe
- 0:45-0:55 - Explain the layout

---

### Segment 3: Search Across Sessions (0:55 - 1:25)

**Voice-Over:**
> "But here's where it gets powerful. Search across ALL your conversations."

**Terminal Commands:**
```bash
orchestra search "authentication"
```

**Expected Output:**
```
SEARCH RESULTS: "authentication"
================================

Found 7 matches across 3 sessions:

[abc123] ~/projects/api - 2 min ago
  Line 142: "Let's add JWT authentication to the middleware"
  Line 289: "The authentication flow should check refresh tokens"

[jkl012] ~/projects/api - Yesterday
  Line 45: "Fixed authentication bypass vulnerability"
  Line 67: "Added rate limiting to authentication endpoints"

[pqr678] ~/projects/api - Last week
  Line 12: "Started implementing OAuth2 authentication"
  ...

Use 'orchestra attach <id>' to jump to session
```

**Voice-Over (continued):**
> "Seven matches. Three sessions. Including that security fix from last week you completely forgot about."

**Terminal Commands (continued):**
```bash
# Jump directly to a result
orchestra attach jkl012
```

**Screen Notes:**
- Type search query with slight pause for effect
- Highlight the match from "Last week"
- Show the attach command reconnecting

**Timing Breakdown:**
- 0:55-1:00 - Set up the search feature
- 1:00-1:15 - Show search results
- 1:15-1:25 - Demonstrate attach, transition

---

### Segment 4: Parallel Agents (1:25 - 1:55)

**Voice-Over:**
> "Now the fun part. Spawn multiple Claude agents working in parallel."

**Terminal Commands:**
```bash
orchestra spawn "refactor the auth module" "write unit tests for auth" "update API documentation"
```

**Expected Output:**
```
SPAWNING PARALLEL AGENTS
========================

[1/3] Starting: "refactor the auth module"
      Session: spawn-a1b2c3 | Directory: ~/projects/api
      Status: RUNNING

[2/3] Starting: "write unit tests for auth"
      Session: spawn-d4e5f6 | Directory: ~/projects/api
      Status: RUNNING

[3/3] Starting: "update API documentation"
      Session: spawn-g7h8i9 | Directory: ~/projects/api
      Status: RUNNING

All agents running. Use 'orchestra monitor' to watch progress.
```

**Voice-Over (continued):**
> "Three agents. Three tasks. All working simultaneously. Check on them anytime."

**Terminal Commands (continued):**
```bash
orchestra monitor
```

**Screen Notes:**
- Split screen showing 3 terminals (optional)
- Show the spawn command with dramatic pause before output
- Flash to monitor view briefly

**Timing Breakdown:**
- 1:25-1:30 - Intro parallel agents
- 1:30-1:45 - Spawn command and output
- 1:45-1:55 - Monitor command, transition

---

### Segment 5: Web Dashboard (1:55 - 2:25)

**Voice-Over:**
> "Want to check your agents from your phone? One command."

**Terminal Commands:**
```bash
orchestra web
```

**Expected Output:**
```
CLAUDE ORCHESTRA WEB DASHBOARD
==============================

Starting server on http://localhost:8080
Network URL: http://192.168.1.42:8080

Scan QR code or open URL on any device:

    [QR CODE APPEARS HERE]

Press Ctrl+C to stop server
```

**Voice-Over (continued):**
> "Mobile-friendly dashboard. Check status, search sessions, even attach to conversations from anywhere on your network."

**Screen Notes:**
- Show QR code appearing in terminal
- Cut to phone/tablet showing the web interface
- Quick tour: session list, search bar, status indicators
- Show a session being viewed on mobile

**Timing Breakdown:**
- 1:55-2:00 - Intro web feature
- 2:00-2:10 - Show command output with QR
- 2:10-2:25 - Mobile device demo

---

### Segment 6: Export & Wrap-up (2:25 - 3:00)

**Voice-Over:**
> "Need to save a conversation? Export to markdown instantly."

**Terminal Commands:**
```bash
orchestra export --last
```

**Expected Output:**
```
EXPORTING SESSION
=================

Session: abc123
Exported to: ./claude-session-abc123-2024-01-15.md

Preview:
---
# Claude Code Session: Auth Middleware
Date: 2024-01-15 14:32:00
Directory: ~/projects/api
---

## User
Let's add JWT authentication to the middleware...

## Claude
I'll help you implement JWT authentication...
```

**Voice-Over (continued):**
> "Clean markdown. Ready for documentation, PRs, or your notes."

**Terminal Commands (optional):**
```bash
# Export specific session
orchestra export abc123 --output auth-refactor.md

# Export with full context
orchestra export --last --full
```

**Voice-Over (wrap-up):**
> "That's Claude Orchestra. Find sessions. Search everything. Run parallel agents. Access from anywhere. Export when you need it."

**Final Screen:**
```
pip install claude-orchestra

GitHub: github.com/[your-org]/claude-orchestra
Docs:   claude-orchestra.dev

Star the repo. Ship faster.
```

**Timing Breakdown:**
- 2:25-2:30 - Intro export
- 2:30-2:40 - Show export output
- 2:40-2:50 - Quick additional export options
- 2:50-3:00 - Wrap-up, CTA, end screen

---

## Production Checklist

### Before Recording
- [ ] Clean terminal history
- [ ] Set terminal font size to 18pt+
- [ ] Use dark theme with high contrast
- [ ] Pre-create mock session data for demos
- [ ] Test all commands work as expected
- [ ] Close unnecessary applications

### Recording Tips
- Record at 1080p minimum, 4K preferred
- Capture system audio for keyboard sounds
- Record voice-over separately for clean audio
- Leave 2-second pauses between segments for editing

### Post-Production
- Add subtle zoom on key commands
- Use lower-thirds for command explanations
- Add chapter markers for YouTube
- Include closed captions

---

## Thumbnail Concepts

**60-Second Video:**
- Split image: chaos (multiple terminals) vs. order (Orchestra UI)
- Text overlay: "FIND ANY CLAUDE SESSION"
- Bright accent color on Orchestra side

**3-Minute Tutorial:**
- Terminal screenshot with `orchestra sessions` output
- Text overlay: "FULL TUTORIAL"
- Badge: "3 MIN"

---

## Call-to-Action Templates

**End Screen (Video):**
```
Ready to orchestrate?

pip install claude-orchestra

[GitHub Icon] Star on GitHub
[Subscribe Icon] Subscribe for more dev tools
```

**Description Template:**
```
Claude Orchestra - Session management for Claude Code power users.

Install: pip install claude-orchestra
GitHub: [link]
Docs: [link]

Timestamps:
0:00 - Installation
0:25 - Finding Sessions
0:55 - Search
1:25 - Parallel Agents
1:55 - Web Dashboard
2:25 - Export

#ClaudeCode #AI #DeveloperTools
```
