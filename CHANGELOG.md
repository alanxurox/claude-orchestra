# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-05

### Added
- **Multi-agent orchestration**: Spawn multiple Claude Code agents in parallel for autonomous task execution
- **Git worktree isolation**: Each agent works in its own isolated git worktree to prevent file conflicts
- **Session discovery**: Automatically find and resume recent Claude Code sessions
- **Web dashboard**: Real-time monitoring of agent status and execution via FastAPI + WebSockets
  - Mobile-responsive design
  - Live agent status updates every 2 seconds
  - Spawn, pause, and manage agents from UI
- **CLI commands**:
  - `orchestra init` - Initialize project for orchestration
  - `orchestra sessions` - List recent Claude Code sessions
  - `orchestra spawn` - Launch parallel agents with tasks
  - `orchestra status` - Show real-time agent status
  - `orchestra collect` - Gather agent results
  - `orchestra cleanup` - Remove completed agents and worktrees
  - `orchestra worktrees` - List active worktrees
  - `orchestra web` - Launch web dashboard
- **Configuration management**: Customizable settings via JSON config file
  - Permission bypass patterns for autonomous operation
  - Parallel execution limits
  - Worktree directory configuration
- **State persistence**: JSON-based state tracking for resuming interrupted operations

### Features
- Zero-conflict merging: Each agent's work is in separate branch, enabling clean PR-based integration
- Subprocess-based agent execution: Spawn independent Claude Code CLI processes
- Async-native architecture: FastAPI with WebSocket support for real-time updates
- Session resume capability: Continue interrupted work with new directives

### Known Limitations
- No database: Uses JSON file for state persistence
- No inter-agent communication: Agents work independently
- No result aggregation: Results collected manually
- Limited error recovery: Failed processes need manual intervention
- Dashboard is embedded: Static files served from Python, not separate frontend

## [Unreleased]

### Planned for v0.2.0
- Integration tests for complete workflows
- Command-line test framework integration
- Agent-to-agent communication protocol
- Result aggregation and filtering
- Performance optimizations
- Comprehensive documentation site
- Docker image for easy deployment
- Dashboard persistence and analytics history
