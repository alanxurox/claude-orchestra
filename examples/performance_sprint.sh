#!/bin/bash
# Example: Performance Optimization Sprint with Orchestra
#
# This script demonstrates how to use Orchestra to run a performance
# optimization sprint with parallel agents working on different aspects:
# - Agent 1: Database query profiling
# - Agent 2: Caching implementation
# - Agent 3: Code refactoring for performance

set -e

PROJECT_DIR="${1:-.}"

echo "=== Claude Orchestra: Performance Optimization Sprint ==="
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

echo "Step 1: Find recent work to build upon"
echo "Listing sessions from the last 4 hours..."
echo ""

orchestra sessions --hours 4 || echo "No recent sessions found (that's okay)"
echo ""

echo "Step 2: Spawn parallel optimization agents"
echo "  - Agent 1: Profile and identify performance bottlenecks"
echo "  - Agent 2: Implement caching strategies"
echo "  - Agent 3: Refactor hot paths for speed"
echo ""

echo "To spawn the agents, run:"
echo ""
echo "  orchestra spawn \\"
echo "    'Profile the application to identify performance bottlenecks. Use profilers like cProfile or flamegraph. Measure database query times, API response times, and function execution times. Generate a detailed report of the top 10 slowest operations.' \\"
echo "    'Implement caching to improve performance. Add Redis caching for expensive queries, implement HTTP caching headers, add memoization for expensive computations. Measure performance improvement before and after.' \\"
echo "    'Refactor the application code for performance. Optimize loops and algorithms, reduce unnecessary allocations, batch database operations, implement lazy loading. Use profiling data to guide optimizations.'"
echo ""

echo "Step 3: Monitor progress with web dashboard"
echo ""
echo "  orchestra web --port 8888"
echo ""
echo "  Then visit: http://localhost:8888"
echo "  Dashboard shows real-time agent status and allows you to:"
echo "    - Watch agents working in parallel"
echo "    - Pause/resume agents as needed"
echo "    - View agent output and activity"
echo ""

echo "Step 4: Analyze results"
echo "  After agents complete, run: orchestra collect"
echo "  Review the work in separate branches: orchestra worktrees"
echo ""

echo "Step 5: Create PRs and merge improvements"
echo "  Each agent's work is isolated in a git worktree"
echo "  Create PRs from orchestra/* branches for review"
echo "  Benchmark and measure performance improvements"
echo ""

echo "=== Performance Sprint Best Practices ==="
echo ""
echo "1. Baseline: Measure performance before changes"
echo "   - Record query times, response times, memory usage"
echo ""
echo "2. Targeted Optimizations: Focus on actual bottlenecks"
echo "   - Use profilers to identify hot spots"
echo "   - Don't optimize prematurely"
echo ""
echo "3. Incremental: Merge improvements gradually"
echo "   - Each agent's work in separate branch"
echo "   - Test each optimization independently"
echo ""
echo "4. Measure Results: Verify improvements"
echo "   - Compare metrics before/after"
echo "   - Run performance tests after merge"
echo ""

echo "=== Recommended Configuration ==="
echo ""
cat << 'EOF'
{
  "default_parallel": 3,
  "max_parallel": 4,
  "heartbeat_interval": 45,
  "stale_threshold": 900,
  "bypass_permissions": [
    "Bash(git *)",
    "Bash(pip *)",
    "Read(*)",
    "Glob(*)",
    "Grep(*)",
    "Edit(*)"
  ]
}
EOF

echo ""
echo "=== Get Started ==="
echo "Run the spawn command above, then monitor with: orchestra status --watch"
