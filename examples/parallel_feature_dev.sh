#!/bin/bash
# Example: Parallel Feature Development with Orchestra
#
# This script demonstrates how to use Orchestra to develop
# a complete authentication feature in parallel:
# - Agent 1: Backend API
# - Agent 2: Frontend UI
# - Agent 3: Tests

set -e

PROJECT_DIR="${1:-.}"

echo "=== Claude Orchestra: Parallel Feature Development Example ==="
echo "Project: $PROJECT_DIR"
echo ""

# Check if orchestra is installed
if ! command -v orchestra &> /dev/null; then
    echo "Error: orchestra CLI not found. Install with: pip install claude-orchestra"
    exit 1
fi

# Check if we're in a git repository
if [ ! -d "$PROJECT_DIR/.git" ]; then
    echo "Error: Not a git repository. Run this in your project root."
    exit 1
fi

cd "$PROJECT_DIR"

echo "Step 1: Initialize Orchestra in this project"
orchestra init || true
echo "✓ Orchestra initialized"
echo ""

echo "Step 2: Spawn 3 agents for parallel development"
echo "  - Agent 1: Backend authentication API with JWT"
echo "  - Agent 2: Frontend login/registration UI"
echo "  - Agent 3: Integration and unit tests"
echo ""

# Note: In actual usage, you would run:
# orchestra spawn \
#   "Implement REST API endpoints for user authentication. Support login with email/password, return JWT token, add refresh token rotation, implement logout endpoint. Use FastAPI and SQLAlchemy. Store users in database. Hash passwords with bcrypt." \
#   "Build responsive React login and registration pages. Include form validation, error messages, password strength indicator. Store JWT in secure httpOnly cookie. Handle token refresh automatically. Add remember-me functionality." \
#   "Write comprehensive tests for auth system. Test successful login/logout, invalid credentials, expired tokens, token refresh, password reset flow. Use pytest for backend, Jest for frontend. Target 90%+ coverage."

echo "To actually spawn agents, run:"
echo ""
echo "  orchestra spawn \\"
echo "    'Build REST API for user authentication with JWT tokens and refresh token rotation' \\"
echo "    'Create login and registration UI with form validation and error handling' \\"
echo "    'Write comprehensive tests for authentication flow with 90% coverage'"
echo ""

echo "Step 3: Monitor progress"
echo "  In terminal: orchestra status --watch"
echo "  Or web UI: orchestra web --port 8888"
echo ""

echo "Step 4: Collect results when agents are done"
echo "  orchestra collect"
echo ""

echo "Step 5: Review and merge"
echo "  Each agent's work is in a separate git branch (orchestra/task-*)"
echo "  Create pull requests from these branches for review"
echo ""

echo "=== Configuration Tips ==="
echo ""
echo "To customize behavior, edit ~/.config/claude-orchestra/config.json"
echo ""
echo "Recommended settings for this feature development:"
echo ""
cat << 'EOF'
{
  "default_parallel": 3,
  "max_parallel": 5,
  "heartbeat_interval": 30,
  "stale_threshold": 600,
  "bypass_permissions": [
    "Bash(git *)",
    "Bash(npm *)",
    "Bash(pip *)",
    "Read(*)",
    "Glob(*)",
    "Grep(*)",
    "Write(*)",
    "Edit(*)"
  ]
}
EOF

echo ""
echo "=== Success! ==="
echo "Your project is ready for parallel development with Orchestra."
echo "Run the spawn command above to get started!"
