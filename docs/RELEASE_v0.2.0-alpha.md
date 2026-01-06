# Release Notes: v0.2.0-alpha

**Title:** v0.2.0-alpha: Session Intelligence

## The Lightweight Claude Orchestrator - Now with Session Intelligence

This alpha release establishes claude-orchestra as **the** tool for discovering, monitoring, and resuming Claude Code sessions.

### New Features

**Session Discovery Commands:**
- `orchestra sessions` - Find recent Claude Code sessions
- `orchestra analytics` - Session usage statistics by project
- `orchestra search` - Full-text search across all sessions
- `orchestra export` - Export sessions to markdown
- `orchestra health` - Session storage health check

**Web Dashboard Enhancements:**
- "Recent Sessions" panel with one-click resume
- Copy-to-clipboard for resume commands
- Mobile-optimized session cards

### Why Session Discovery Matters

No other orchestrator does this. You can:
- Find that session you started yesterday
- Resume from your phone while away from your desk
- Search across all your Claude conversations
- Monitor storage health and clean up old sessions

### Installation

```bash
pip install claude-orchestra==0.2.0a1
```

Or install from source:
```bash
git clone https://github.com/alanxurox/claude-orchestra
cd claude-orchestra
pip install -e ".[dev]"
```

### Quick Start

```bash
orchestra init
orchestra sessions --hours 24
orchestra search "authentication"
orchestra web
```

### Full Changelog

See [CHANGELOG.md](https://github.com/alanxurox/claude-orchestra/blob/main/CHANGELOG.md)

---

**Positioning:** The lightweight Claude orchestrator. No Docker, no databases, just `pip install`.

**Key differentiator:** Session discovery - find and resume ANY Claude Code session.

---

## To Create Release Manually

```bash
gh release create v0.2.0-alpha \
  --title "v0.2.0-alpha: Session Intelligence" \
  --notes-file docs/RELEASE_v0.2.0-alpha.md \
  --prerelease
```
