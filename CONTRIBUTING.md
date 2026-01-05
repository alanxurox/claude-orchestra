# Contributing to Claude Orchestra

Thank you for your interest in contributing to Claude Orchestra! This document provides guidelines for contributing.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful of others and follow standard open-source etiquette.

## How to Report Bugs

Found a bug? Please create a GitHub issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs. actual behavior
- Python version and OS
- Relevant error messages or logs

## How to Request Features

Have an idea? Open a GitHub issue with:
- Clear use case explaining the problem it solves
- Example of how you'd use the feature
- Any alternative approaches you've considered

## Development Setup

### Prerequisites
- Python 3.10, 3.11, or 3.12
- Git (for worktree testing)
- Claude Code CLI (for integration testing)

### Local Development

```bash
# Clone the repository
git clone https://github.com/alanxurox/claude-orchestra.git
cd claude-orchestra

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Verify installation
orchestra --help
```

## Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=orchestra tests/

# Run specific test
pytest tests/test_session.py::test_find_recent_sessions

# Run tests matching pattern
pytest -k "worktree" tests/
```

## Code Style

We use automated tools to maintain code quality:

```bash
# Format code with black
black orchestra/ tests/

# Check code with ruff
ruff check orchestra/ tests/

# Both together
black . && ruff check .
```

These are run automatically in CI/CD. Please run locally before committing.

## Making Changes

1. **Create a branch**: `git checkout -b feature/your-feature-name`
2. **Make changes**: Implement your feature or fix
3. **Add tests**: Write tests for new functionality
4. **Run checks**:
   ```bash
   pytest tests/
   black .
   ruff check .
   ```
5. **Commit**: Use clear commit messages
6. **Push**: Push to your fork
7. **Create PR**: Submit a pull request to `main` branch

### Commit Message Guidelines

- Use imperative mood ("add feature" not "added feature")
- Keep first line under 50 characters
- Reference issues: "Fixes #123"
- Example: `Add session resume functionality (Fixes #42)`

## Pull Request Guidelines

- Link to related GitHub issue
- Describe what changed and why
- Include any breaking changes
- Ensure all tests pass
- Keep PRs focused on one feature/fix

## Development Workflow

```
Feature Branch → Local Testing → Tests Pass → PR → Code Review → Merge to Main → Release
```

## Testing Guidelines

- Write tests for new features
- Ensure existing tests pass
- Test both happy path and edge cases
- Use fixtures for common test setup
- Mock external dependencies (subprocess calls, file I/O)

## Documentation

When adding features:
1. Update code docstrings
2. Update relevant documentation files (CLAUDE.md, README.md, or docs/)
3. Add examples if it's a user-facing feature

## Project Structure

```
orchestra/
├── __init__.py          # Package version
├── cli.py               # Click CLI commands
├── config.py            # Configuration management
├── core/                # Core orchestration logic
│   ├── session.py       # Session discovery
│   ├── worktree.py      # Git worktree management
│   ├── agent.py         # Agent orchestration
│   └── state.py         # State persistence
└── dashboard/           # Web dashboard
    ├── server.py        # FastAPI server
    └── static/          # Frontend assets

tests/
├── test_session.py      # Session discovery tests
└── test_worktree.py     # Git worktree tests
```

## Getting Help

- GitHub Discussions or Issues for questions
- Check existing issues before opening new ones
- Review CLAUDE.md for architecture details

## Release Process

Releases are created via git tags `v*.*.*`. After merge to main:

1. Update CHANGELOG.md
2. Create git tag: `git tag v0.x.y`
3. Push tag: `git push origin v0.x.y`
4. GitHub Actions automatically publishes to PyPI

## License

By contributing to Claude Orchestra, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Claude Orchestra!
