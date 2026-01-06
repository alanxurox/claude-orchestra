"""FastAPI web server for the dashboard."""

import asyncio
from typing import List, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from ..core import Orchestrator

app = FastAPI(title="Claude Orchestra Dashboard")

# Global orchestrator instance
orchestrator = Orchestrator()


class SpawnRequest(BaseModel):
    """Request to spawn agents."""

    tasks: List[str]
    parallel: Optional[int] = 3
    use_worktrees: Optional[bool] = True


class AgentAction(BaseModel):
    """Request to act on an agent."""

    agent_id: str


# WebSocket connections for real-time updates
connections: List[WebSocket] = []


@app.get("/api/status")
async def get_status():
    """Get current orchestrator status."""
    return orchestrator.status()


@app.get("/api/sessions")
async def get_sessions(hours: float = 4.0):
    """Get recent sessions."""
    from ..core import SessionManager

    manager = SessionManager()
    sessions = manager.find_recent(hours=hours)
    return [
        {
            "session_id": s.session_id,
            "project_path": s.project_path,
            "modified_at": s.modified_at.isoformat(),
            "message_count": s.message_count,
            "last_prompt": s.last_prompt,
        }
        for s in sessions
    ]


@app.get("/api/worktrees")
async def get_worktrees():
    """Get active worktrees."""
    from ..core import WorktreeManager

    manager = WorktreeManager()
    worktrees = manager.list_active()
    return [
        {
            "branch": wt.branch,
            "task": wt.task,
            "path": str(wt.path),
            "is_active": wt.is_active,
        }
        for wt in worktrees
    ]


@app.post("/api/spawn")
async def spawn_agents(request: SpawnRequest):
    """Spawn new agents."""
    handles = orchestrator.spawn(
        tasks=request.tasks,
        parallel=request.parallel,
        use_worktrees=request.use_worktrees,
    )

    # Notify WebSocket clients
    await broadcast_status()

    return {
        "spawned": len(handles),
        "agents": [
            {
                "agent_id": h.agent_id,
                "task": h.task,
                "worktree": h.worktree.branch if h.worktree else None,
            }
            for h in handles
        ],
    }


@app.post("/api/agents/{agent_id}/pause")
async def pause_agent(agent_id: str):
    """Pause an agent."""
    success = orchestrator.pause(agent_id)
    await broadcast_status()
    return {"success": success}


@app.post("/api/agents/{agent_id}/resume")
async def resume_agent(agent_id: str):
    """Resume a paused agent."""
    handle = orchestrator.resume_agent(agent_id)
    await broadcast_status()
    return {"success": handle is not None}


@app.post("/api/cleanup")
async def cleanup_agents(all_agents: bool = False):
    """Clean up completed agents."""
    cleaned = orchestrator.cleanup(completed_only=not all_agents)
    await broadcast_status()
    return {"cleaned": cleaned}


@app.websocket("/ws/status")
async def websocket_status(websocket: WebSocket):
    """WebSocket for real-time status updates."""
    await websocket.accept()
    connections.append(websocket)

    try:
        # Send initial status
        await websocket.send_json(orchestrator.status())

        # Keep connection alive and send periodic updates
        while True:
            await asyncio.sleep(2)
            await websocket.send_json(orchestrator.status())
    except WebSocketDisconnect:
        connections.remove(websocket)
    except Exception:
        if websocket in connections:
            connections.remove(websocket)


async def broadcast_status():
    """Broadcast status to all WebSocket clients."""
    status = orchestrator.status()
    for connection in connections:
        try:
            await connection.send_json(status)
        except Exception:
            pass


# Serve static dashboard
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serve the dashboard HTML."""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claude Orchestra</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .status-running { background-color: #10b981; }
        .status-completed { background-color: #3b82f6; }
        .status-failed { background-color: #ef4444; }
        .status-stale { background-color: #f59e0b; }
        .status-paused { background-color: #8b5cf6; }
    </style>
</head>
<body class="bg-gray-900 text-white min-h-screen">
    <div class="container mx-auto px-4 py-8">
        <header class="mb-8">
            <h1 class="text-3xl font-bold">Claude Orchestra</h1>
            <p class="text-gray-400">Multi-agent orchestration dashboard</p>
        </header>

        <!-- Summary Cards -->
        <div id="summary" class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div class="bg-gray-800 rounded-lg p-4">
                <div class="text-2xl font-bold text-green-500" id="running-count">0</div>
                <div class="text-gray-400">Running</div>
            </div>
            <div class="bg-gray-800 rounded-lg p-4">
                <div class="text-2xl font-bold text-blue-500" id="completed-count">0</div>
                <div class="text-gray-400">Completed</div>
            </div>
            <div class="bg-gray-800 rounded-lg p-4">
                <div class="text-2xl font-bold text-red-500" id="failed-count">0</div>
                <div class="text-gray-400">Failed</div>
            </div>
            <div class="bg-gray-800 rounded-lg p-4">
                <div class="text-2xl font-bold text-yellow-500" id="stale-count">0</div>
                <div class="text-gray-400">Stale</div>
            </div>
        </div>

        <!-- Spawn Form -->
        <div class="bg-gray-800 rounded-lg p-4 mb-8">
            <h2 class="text-xl font-bold mb-4">Spawn Agents</h2>
            <form id="spawn-form" class="flex flex-col md:flex-row gap-4">
                <input type="text" id="tasks-input" placeholder="Task 1, Task 2, Task 3..."
                    class="flex-1 bg-gray-700 rounded px-4 py-2 text-white">
                <select id="parallel-select" class="bg-gray-700 rounded px-4 py-2">
                    <option value="1">1 parallel</option>
                    <option value="2">2 parallel</option>
                    <option value="3" selected>3 parallel</option>
                    <option value="5">5 parallel</option>
                </select>
                <button type="submit" class="bg-green-600 hover:bg-green-700 rounded px-6 py-2 font-bold">
                    Spawn
                </button>
            </form>
        </div>

        <!-- Agents Grid -->
        <div id="agents-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <!-- Agent cards will be inserted here -->
        </div>

        <!-- Recent Sessions -->
        <div class="mt-8">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-xl font-bold">Recent Sessions</h2>
                <button onclick="loadSessions()" class="text-gray-400 hover:text-white text-sm">
                    Refresh
                </button>
            </div>
            <div id="sessions-list" class="space-y-3">
                <!-- Session cards will be inserted here -->
                <div class="text-gray-500 text-center py-8">Loading sessions...</div>
            </div>
        </div>

        <!-- Resume Command Modal -->
        <div id="resume-modal" class="fixed inset-0 bg-black bg-opacity-50 hidden items-center justify-center z-50 p-4">
            <div class="bg-gray-800 rounded-lg p-6 max-w-lg w-full">
                <h3 class="text-lg font-bold mb-4">Resume Session</h3>
                <p class="text-gray-400 text-sm mb-3">Run this command in your terminal:</p>
                <div class="bg-gray-900 rounded p-3 font-mono text-sm break-all mb-4">
                    <code id="resume-command" class="text-green-400"></code>
                </div>
                <div class="flex gap-3">
                    <button onclick="copyResumeCommand()" class="flex-1 bg-green-600 hover:bg-green-700 rounded px-4 py-2 font-bold">
                        Copy Command
                    </button>
                    <button onclick="closeResumeModal()" class="flex-1 bg-gray-600 hover:bg-gray-700 rounded px-4 py-2">
                        Close
                    </button>
                </div>
                <p id="copy-feedback" class="text-green-400 text-sm mt-2 text-center hidden">Copied!</p>
            </div>
        </div>
    </div>

    <script>
        let ws;

        function connectWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            ws = new WebSocket(`${protocol}//${window.location.host}/ws/status`);

            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                updateDashboard(data);
            };

            ws.onclose = () => {
                setTimeout(connectWebSocket, 3000);
            };
        }

        function updateDashboard(data) {
            // Update summary counts
            document.getElementById('running-count').textContent = data.running;
            document.getElementById('completed-count').textContent = data.completed;
            document.getElementById('failed-count').textContent = data.failed;
            document.getElementById('stale-count').textContent = data.stale;

            // Update agents grid
            const grid = document.getElementById('agents-grid');
            grid.innerHTML = data.agents.map(agent => `
                <div class="bg-gray-800 rounded-lg p-4">
                    <div class="flex justify-between items-start mb-2">
                        <span class="font-mono text-sm text-gray-400">${agent.agent_id.slice(0, 8)}</span>
                        <span class="px-2 py-1 rounded text-xs status-${agent.status}">${agent.status}</span>
                    </div>
                    <h3 class="font-bold mb-2 truncate" title="${agent.task}">${agent.task}</h3>
                    <p class="text-sm text-gray-400 mb-3">${agent.current_activity || 'No activity'}</p>
                    <div class="flex gap-2">
                        ${agent.status === 'running' ? `
                            <button onclick="pauseAgent('${agent.agent_id}')"
                                class="bg-yellow-600 hover:bg-yellow-700 rounded px-3 py-1 text-sm">
                                Pause
                            </button>
                        ` : ''}
                        ${agent.status === 'paused' ? `
                            <button onclick="resumeAgent('${agent.agent_id}')"
                                class="bg-green-600 hover:bg-green-700 rounded px-3 py-1 text-sm">
                                Resume
                            </button>
                        ` : ''}
                    </div>
                </div>
            `).join('');
        }

        async function pauseAgent(agentId) {
            await fetch(`/api/agents/${agentId}/pause`, { method: 'POST' });
        }

        async function resumeAgent(agentId) {
            await fetch(`/api/agents/${agentId}/resume`, { method: 'POST' });
        }

        document.getElementById('spawn-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const tasksInput = document.getElementById('tasks-input');
            const tasks = tasksInput.value.split(',').map(t => t.trim()).filter(t => t);
            const parallel = parseInt(document.getElementById('parallel-select').value);

            if (tasks.length === 0) return;

            await fetch('/api/spawn', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ tasks, parallel }),
            });

            tasksInput.value = '';
        });

        // Initial connection
        connectWebSocket();

        // Sessions functionality
        async function loadSessions() {
            try {
                const response = await fetch('/api/sessions?hours=24');
                const sessions = await response.json();
                renderSessions(sessions);
            } catch (error) {
                document.getElementById('sessions-list').innerHTML = `
                    <div class="text-red-400 text-center py-8">Failed to load sessions</div>
                `;
            }
        }

        function renderSessions(sessions) {
            const list = document.getElementById('sessions-list');

            if (sessions.length === 0) {
                list.innerHTML = `
                    <div class="text-gray-500 text-center py-8">No recent sessions found</div>
                `;
                return;
            }

            list.innerHTML = sessions.map(session => {
                const projectName = session.project_path ? session.project_path.split('/').pop() : 'Unknown Project';
                const promptPreview = session.last_prompt
                    ? (session.last_prompt.length > 80 ? session.last_prompt.slice(0, 80) + '...' : session.last_prompt)
                    : 'No prompt';
                const timeAgo = formatTimeAgo(new Date(session.modified_at));

                return `
                    <div class="bg-gray-800 rounded-lg p-4">
                        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                            <div class="flex-1 min-w-0">
                                <div class="flex items-center gap-2 mb-1">
                                    <h3 class="font-bold truncate">${escapeHtml(projectName)}</h3>
                                    <span class="text-xs text-gray-500 whitespace-nowrap">${timeAgo}</span>
                                </div>
                                <p class="text-sm text-gray-400 truncate mb-1" title="${escapeHtml(session.last_prompt || '')}">${escapeHtml(promptPreview)}</p>
                                <div class="flex items-center gap-3 text-xs text-gray-500">
                                    <span>${session.message_count} messages</span>
                                    <span class="font-mono">${session.session_id.slice(0, 8)}...</span>
                                </div>
                            </div>
                            <button onclick="showResumeModal('${session.session_id}', '${escapeHtml(projectName)}')"
                                class="bg-green-600 hover:bg-green-700 rounded px-4 py-2 text-sm font-bold whitespace-nowrap">
                                Resume
                            </button>
                        </div>
                    </div>
                `;
            }).join('');
        }

        function formatTimeAgo(date) {
            const seconds = Math.floor((new Date() - date) / 1000);
            if (seconds < 60) return 'just now';
            const minutes = Math.floor(seconds / 60);
            if (minutes < 60) return `${minutes}m ago`;
            const hours = Math.floor(minutes / 60);
            if (hours < 24) return `${hours}h ago`;
            const days = Math.floor(hours / 24);
            return `${days}d ago`;
        }

        function escapeHtml(text) {
            if (!text) return '';
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        function showResumeModal(sessionId, projectName) {
            const command = `claude --resume ${sessionId}`;
            document.getElementById('resume-command').textContent = command;
            document.getElementById('resume-modal').classList.remove('hidden');
            document.getElementById('resume-modal').classList.add('flex');
            document.getElementById('copy-feedback').classList.add('hidden');
        }

        function closeResumeModal() {
            document.getElementById('resume-modal').classList.add('hidden');
            document.getElementById('resume-modal').classList.remove('flex');
        }

        async function copyResumeCommand() {
            const command = document.getElementById('resume-command').textContent;
            try {
                await navigator.clipboard.writeText(command);
                document.getElementById('copy-feedback').classList.remove('hidden');
                setTimeout(() => {
                    document.getElementById('copy-feedback').classList.add('hidden');
                }, 2000);
            } catch (err) {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = command;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                document.getElementById('copy-feedback').classList.remove('hidden');
                setTimeout(() => {
                    document.getElementById('copy-feedback').classList.add('hidden');
                }, 2000);
            }
        }

        // Close modal on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') closeResumeModal();
        });

        // Close modal on backdrop click
        document.getElementById('resume-modal').addEventListener('click', (e) => {
            if (e.target.id === 'resume-modal') closeResumeModal();
        });

        // Load sessions on page load
        loadSessions();
    </script>
</body>
</html>
"""
