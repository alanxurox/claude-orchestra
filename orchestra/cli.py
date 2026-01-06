"""CLI commands for Claude Orchestra."""

import asyncio
import sys
from pathlib import Path
from typing import List

import click
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .config import OrchestraConfig
from .core import Orchestrator, SessionManager, WorktreeManager

console = Console()


@click.group()
@click.version_option()
def main():
    """Claude Orchestra - Multi-agent orchestration for Claude Code."""
    pass


@main.command()
@click.option("--force", is_flag=True, help="Overwrite existing config")
def init(force: bool):
    """Initialize Orchestra in the current project."""
    config_path = Path.cwd() / ".orchestra" / "config.json"

    if config_path.exists() and not force:
        console.print(
            "[yellow]Orchestra already initialized. Use --force to reinitialize.[/yellow]"
        )
        return

    config = OrchestraConfig()
    config.save(config_path)

    # Create worktrees directory
    worktrees_dir = Path.cwd() / config.worktree_dir
    worktrees_dir.mkdir(exist_ok=True)

    # Add to .gitignore
    gitignore = Path.cwd() / ".gitignore"
    ignore_entries = [config.worktree_dir, ".orchestra/"]

    if gitignore.exists():
        content = gitignore.read_text()
        for entry in ignore_entries:
            if entry not in content:
                with open(gitignore, "a") as f:
                    f.write(f"\n{entry}")
    else:
        gitignore.write_text("\n".join(ignore_entries) + "\n")

    console.print("[green]Orchestra initialized successfully![/green]")
    console.print(f"  Config: {config_path}")
    console.print(f"  Worktrees: {worktrees_dir}")


@main.command()
@click.option("--hours", default=4.0, help="Hours to look back")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def sessions(hours: float, as_json: bool):
    """List recent Claude Code sessions."""
    manager = SessionManager()
    recent = manager.find_recent(hours=hours)

    if as_json:
        import json

        data = [
            {
                "session_id": s.session_id,
                "project_path": s.project_path,
                "modified_at": s.modified_at.isoformat(),
                "message_count": s.message_count,
                "last_prompt": s.last_prompt,
            }
            for s in recent
        ]
        console.print_json(json.dumps(data))
        return

    if not recent:
        console.print(f"[yellow]No sessions found in the last {hours} hours[/yellow]")
        return

    table = Table(title=f"Sessions (last {hours}h)")
    table.add_column("Session ID", style="cyan")
    table.add_column("Project", style="blue")
    table.add_column("Messages", justify="right")
    table.add_column("Modified", style="green")
    table.add_column("Last Prompt", style="dim", max_width=40)

    for session in recent:
        project = Path(session.project_path).name if session.project_path else "unknown"
        modified = session.modified_at.strftime("%H:%M:%S")
        prompt = (session.last_prompt or "")[:40]

        table.add_row(
            session.session_id[:12] + "...",
            project,
            str(session.message_count),
            modified,
            prompt,
        )

    console.print(table)


@main.command()
@click.argument("tasks", nargs=-1, required=True)
@click.option("--parallel", "-p", default=3, help="Max parallel agents")
@click.option("--no-worktree", is_flag=True, help="Don't use worktrees")
def spawn(tasks: List[str], parallel: int, no_worktree: bool):
    """Spawn parallel agents for tasks."""
    if not tasks:
        console.print("[red]No tasks provided[/red]")
        return

    console.print(f"[bold]Spawning {min(len(tasks), parallel)} agents...[/bold]")

    orchestrator = Orchestrator()
    handles = orchestrator.spawn(
        tasks=list(tasks),
        parallel=parallel,
        use_worktrees=not no_worktree,
    )

    table = Table(title="Spawned Agents")
    table.add_column("Agent ID", style="cyan")
    table.add_column("Task", style="blue")
    table.add_column("Worktree", style="dim")

    for handle in handles:
        worktree = handle.worktree.branch if handle.worktree else "-"
        table.add_row(handle.agent_id, handle.task[:50], worktree)

    console.print(table)
    console.print("\n[green]Run 'orchestra status' to monitor progress[/green]")


@main.command()
@click.option("--watch", "-w", is_flag=True, help="Watch mode with live updates")
def status(watch: bool):
    """Show agent status."""
    orchestrator = Orchestrator()

    def render_status():
        status_data = orchestrator.status()

        # Summary panel
        summary = Text()
        summary.append(f"Running: {status_data['running']} ", style="green")
        summary.append(f"Completed: {status_data['completed']} ", style="blue")
        summary.append(f"Failed: {status_data['failed']} ", style="red")
        summary.append(f"Stale: {status_data['stale']}", style="yellow")

        # Agents table
        table = Table()
        table.add_column("ID", style="cyan", width=10)
        table.add_column("Task", style="blue", max_width=40)
        table.add_column("Status", width=10)
        table.add_column("Activity", style="dim", max_width=30)
        table.add_column("Heartbeat", style="dim")

        for agent in status_data["agents"]:
            status_style = {
                "running": "green",
                "completed": "blue",
                "failed": "red",
                "stale": "yellow",
                "paused": "magenta",
            }.get(agent["status"], "white")

            heartbeat = ""
            if agent.get("last_heartbeat"):
                from datetime import datetime

                hb = datetime.fromisoformat(agent["last_heartbeat"])
                heartbeat = hb.strftime("%H:%M:%S")

            table.add_row(
                agent["agent_id"][:8],
                (agent["task"] or "")[:40],
                Text(agent["status"], style=status_style),
                (agent.get("current_activity") or "-")[:30],
                heartbeat,
            )

        return Panel.fit(
            table,
            title="Agents",
            border_style="blue",
        )

    if watch:
        with Live(render_status(), refresh_per_second=1, console=console) as live:
            try:
                while True:
                    live.update(render_status())
                    import time

                    time.sleep(1)
            except KeyboardInterrupt:
                pass
    else:
        console.print(render_status())


@main.command()
@click.option("--wait", "-w", is_flag=True, help="Wait for all agents to complete")
def collect(wait: bool):
    """Collect results from agents."""
    orchestrator = Orchestrator()

    async def do_collect():
        results = await orchestrator.collect()
        return results

    if wait:
        console.print("[bold]Waiting for agents to complete...[/bold]")

    results = asyncio.run(do_collect())

    if not results:
        console.print("[yellow]No agents to collect from[/yellow]")
        return

    table = Table(title="Agent Results")
    table.add_column("Agent ID", style="cyan")
    table.add_column("Task", style="blue")
    table.add_column("Status")
    table.add_column("Duration", justify="right")

    for agent_id, result in results.items():
        status_style = "green" if result.success else "red"
        status_text = "Success" if result.success else "Failed"

        table.add_row(
            agent_id[:8],
            result.task[:40],
            Text(status_text, style=status_style),
            f"{result.duration_seconds:.1f}s",
        )

    console.print(table)


@main.command()
@click.option("--all", "cleanup_all", is_flag=True, help="Clean up all agents, not just completed")
def cleanup(cleanup_all: bool):
    """Clean up completed agents and worktrees."""
    orchestrator = Orchestrator()
    cleaned = orchestrator.cleanup(completed_only=not cleanup_all)

    console.print(f"[green]Cleaned up {cleaned} agent(s)[/green]")


@main.command()
def worktrees():
    """List active worktrees."""
    manager = WorktreeManager()
    active = manager.list_active()

    if not active:
        console.print("[yellow]No active worktrees[/yellow]")
        return

    table = Table(title="Active Worktrees")
    table.add_column("Branch", style="cyan")
    table.add_column("Task", style="blue")
    table.add_column("Path", style="dim")

    for wt in active:
        table.add_row(wt.branch, wt.task, str(wt.path))

    console.print(table)


@main.command()
@click.option("--hours", default=24.0, help="Hours to look back (default 24)")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def analytics(hours: float, as_json: bool):
    """Show session analytics and insights."""
    from collections import defaultdict

    manager = SessionManager()
    sessions = manager.find_recent(hours=hours)

    # Calculate analytics
    total_sessions = len(sessions)
    total_messages = sum(s.message_count for s in sessions)
    avg_messages = total_messages / total_sessions if total_sessions > 0 else 0

    # Group sessions by project
    projects = defaultdict(list)
    for session in sessions:
        project_name = Path(session.project_path).name if session.project_path else "unknown"
        projects[project_name].append(session)

    # Find most active project
    most_active_project = None
    most_active_count = 0
    for project_name, project_sessions in projects.items():
        if len(project_sessions) > most_active_count:
            most_active_count = len(project_sessions)
            most_active_project = project_name

    if as_json:
        import json

        data = {
            "period_hours": hours,
            "total_sessions": total_sessions,
            "total_messages": total_messages,
            "avg_messages_per_session": round(avg_messages, 2),
            "most_active_project": {
                "name": most_active_project,
                "session_count": most_active_count,
            } if most_active_project else None,
            "projects": {
                name: {
                    "session_count": len(sess_list),
                    "total_messages": sum(s.message_count for s in sess_list),
                    "sessions": [
                        {
                            "session_id": s.session_id,
                            "message_count": s.message_count,
                            "modified_at": s.modified_at.isoformat(),
                        }
                        for s in sess_list
                    ],
                }
                for name, sess_list in projects.items()
            },
        }
        console.print_json(json.dumps(data))
        return

    if not sessions:
        console.print(f"[yellow]No sessions found in the last {hours} hours[/yellow]")
        return

    # Summary table
    summary_table = Table(title=f"Session Analytics (last {hours}h)", box=None)
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="green", justify="right")

    summary_table.add_row("Total Sessions", str(total_sessions))
    summary_table.add_row("Total Messages", str(total_messages))
    summary_table.add_row("Avg Messages/Session", f"{avg_messages:.1f}")
    if most_active_project:
        summary_table.add_row("Most Active Project", f"{most_active_project} ({most_active_count} sessions)")

    console.print(summary_table)
    console.print()

    # Projects breakdown table
    projects_table = Table(title="Sessions by Project")
    projects_table.add_column("Project", style="blue")
    projects_table.add_column("Sessions", justify="right")
    projects_table.add_column("Messages", justify="right")
    projects_table.add_column("Avg Msgs", justify="right", style="dim")

    # Sort projects by session count (descending)
    sorted_projects = sorted(projects.items(), key=lambda x: len(x[1]), reverse=True)

    for project_name, project_sessions in sorted_projects:
        session_count = len(project_sessions)
        message_count = sum(s.message_count for s in project_sessions)
        avg_msgs = message_count / session_count if session_count > 0 else 0

        projects_table.add_row(
            project_name,
            str(session_count),
            str(message_count),
            f"{avg_msgs:.1f}",
        )

    console.print(projects_table)


def _format_bytes(size_bytes: int) -> str:
    """Format bytes as human-readable string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


@main.command()
@click.option("--hours", default=168.0, help="Hours to look back (default: 168 = 1 week)")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def health(hours: float, as_json: bool):
    """Check health of Claude sessions and storage.

    Shows storage usage, active vs stale sessions, and identifies
    sessions that could be cleaned up.

    Examples:

        orchestra health

        orchestra health --hours 720

        orchestra health --json
    """
    manager = SessionManager()
    report = manager.check_health(hours=hours)

    if as_json:
        import json

        # Convert datetimes to ISO format for JSON
        def serialize(obj):
            if hasattr(obj, "isoformat"):
                return obj.isoformat()
            return obj

        json_report = {
            "storage_bytes": report["storage_bytes"],
            "storage_human": _format_bytes(report["storage_bytes"]),
            "session_count": report["session_count"],
            "active_sessions": report["active_sessions"],
            "stale_session_count": len(report["stale_sessions"]),
            "orphaned_session_count": len(report["orphaned_sessions"]),
            "large_session_count": len(report["largest_sessions"]),
            "stale_sessions": [
                {
                    "session_id": s["session_id"],
                    "project_path": s["project_path"],
                    "modified_at": serialize(s["modified_at"]),
                    "message_count": s["message_count"],
                    "file_size": s["file_size"],
                }
                for s in report["stale_sessions"]
            ],
            "orphaned_sessions": [
                {
                    "session_id": s["session_id"],
                    "project_path": s["project_path"],
                    "modified_at": serialize(s["modified_at"]),
                    "message_count": s["message_count"],
                    "file_size": s["file_size"],
                }
                for s in report["orphaned_sessions"]
            ],
            "largest_sessions": [
                {
                    "session_id": s["session_id"],
                    "project_path": s["project_path"],
                    "modified_at": serialize(s["modified_at"]),
                    "message_count": s["message_count"],
                    "file_size": s["file_size"],
                }
                for s in report["largest_sessions"]
            ],
            "oldest_sessions": [
                {
                    "session_id": s["session_id"],
                    "project_path": s["project_path"],
                    "modified_at": serialize(s["modified_at"]),
                    "message_count": s["message_count"],
                    "file_size": s["file_size"],
                }
                for s in report["oldest_sessions"]
            ],
        }
        console.print_json(json.dumps(json_report))
        return

    # Summary section
    stale_count = len(report["stale_sessions"])
    summary_table = Table(title=f"Session Health Report (last {hours}h)", box=None)
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="green", justify="right")

    summary_table.add_row("Total Storage", _format_bytes(report["storage_bytes"]))
    summary_table.add_row("Total Sessions", str(report["session_count"]))
    summary_table.add_row("Active Sessions", str(report["active_sessions"]))
    summary_table.add_row("Stale Sessions (>48h)", str(stale_count))
    summary_table.add_row("Orphaned Sessions", str(len(report["orphaned_sessions"])))
    summary_table.add_row("Large Sessions (>1000 msgs)", str(len(report["largest_sessions"])))

    console.print(summary_table)

    # Large sessions warning
    if report["largest_sessions"]:
        console.print()
        large_table = Table(title="Large Sessions (>1000 messages)")
        large_table.add_column("Session ID", style="cyan")
        large_table.add_column("Project", style="blue")
        large_table.add_column("Messages", justify="right", style="yellow")
        large_table.add_column("Size", justify="right")
        large_table.add_column("Modified", style="dim")

        for s in report["largest_sessions"]:
            project = Path(s["project_path"]).name if s["project_path"] else "unknown"
            modified = s["modified_at"].strftime("%Y-%m-%d %H:%M")
            large_table.add_row(
                s["session_id"][:12] + "...",
                project,
                str(s["message_count"]),
                _format_bytes(s["file_size"]),
                modified,
            )

        console.print(large_table)

    # Orphaned sessions
    if report["orphaned_sessions"]:
        console.print()
        orphan_table = Table(title="Orphaned Sessions (project no longer exists)")
        orphan_table.add_column("Session ID", style="cyan")
        orphan_table.add_column("Original Project", style="red")
        orphan_table.add_column("Messages", justify="right")
        orphan_table.add_column("Size", justify="right")

        for s in report["orphaned_sessions"]:
            orphan_table.add_row(
                s["session_id"][:12] + "...",
                s["project_path"] or "unknown",
                str(s["message_count"]),
                _format_bytes(s["file_size"]),
            )

        console.print(orphan_table)

    # Oldest sessions that could be cleaned up
    if report["oldest_sessions"]:
        console.print()
        oldest_table = Table(title="Oldest Sessions (cleanup candidates)")
        oldest_table.add_column("Session ID", style="cyan")
        oldest_table.add_column("Project", style="blue")
        oldest_table.add_column("Messages", justify="right")
        oldest_table.add_column("Size", justify="right")
        oldest_table.add_column("Modified", style="dim")

        for s in report["oldest_sessions"]:
            project = Path(s["project_path"]).name if s["project_path"] else "unknown"
            modified = s["modified_at"].strftime("%Y-%m-%d %H:%M")
            oldest_table.add_row(
                s["session_id"][:12] + "...",
                project,
                str(s["message_count"]),
                _format_bytes(s["file_size"]),
                modified,
            )

        console.print(oldest_table)

    # Summary tips
    if stale_count > 0 or report["orphaned_sessions"]:
        console.print()
        console.print("[dim]Tip: Stale and orphaned sessions can be safely deleted from ~/.claude/projects/[/dim]")


@main.command()
@click.argument("query")
@click.option("--hours", default=168, help="Hours to look back (default: 168 = 1 week)")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def search(query: str, hours: int, as_json: bool):
    """Search sessions for matching prompts.

    Find sessions where user prompts contain the search term.
    Perfect for finding "that conversation from last week about auth".

    Examples:

        orchestra search "authentication"

        orchestra search "bug fix" --hours 48

        orchestra search "refactor" --json
    """
    manager = SessionManager()
    results = manager.search(query=query, hours=float(hours))

    if as_json:
        import json

        data = [
            {
                "session_id": r["session_id"],
                "project_path": r["project_path"],
                "modified_at": r["modified_at"].isoformat(),
                "match_count": r["match_count"],
                "sample_prompt": r["sample_prompt"],
            }
            for r in results
        ]
        console.print_json(json.dumps(data))
        return

    if not results:
        console.print(
            f"[yellow]No sessions found matching '{query}' in the last {hours} hours[/yellow]"
        )
        return

    table = Table(title=f"Sessions matching '{query}' (last {hours}h)")
    table.add_column("Session ID", style="cyan")
    table.add_column("Project", style="blue")
    table.add_column("Matches", justify="right", style="green")
    table.add_column("Modified", style="dim")
    table.add_column("Sample Prompt", style="white", max_width=50)

    for result in results:
        project = Path(result["project_path"]).name if result["project_path"] else "unknown"
        modified = result["modified_at"].strftime("%Y-%m-%d %H:%M")
        sample = (result["sample_prompt"] or "")[:50]
        if len(result["sample_prompt"] or "") > 50:
            sample += "..."

        table.add_row(
            result["session_id"][:12] + "...",
            project,
            str(result["match_count"]),
            modified,
            sample,
        )

    console.print(table)
    console.print(
        f"\n[dim]Found {len(results)} session(s). "
        f"Use 'claude --resume <session_id>' to continue a session.[/dim]"
    )


@main.command()
@click.option("--port", "-p", default=8888, help="Port to run on")
@click.option("--host", "-h", default="0.0.0.0", help="Host to bind to")
def web(port: int, host: str):
    """Launch web dashboard."""
    console.print(f"[bold]Starting web dashboard at http://{host}:{port}[/bold]")
    console.print("[dim]Press Ctrl+C to stop[/dim]")

    try:
        import uvicorn

        from .dashboard.server import app

        uvicorn.run(app, host=host, port=port, log_level="warning")
    except ImportError:
        console.print("[red]Error: uvicorn not installed. Run: pip install uvicorn[/red]")
        sys.exit(1)


@main.command()
@click.argument("session_id", required=False)
@click.option("--last", is_flag=True, help="Export the most recent session")
@click.option("--output", "-o", type=click.Path(), help="Output file (default: stdout)")
def export(session_id: str, last: bool, output: str):
    """Export a session to markdown format.

    Export session conversations to clean, readable markdown for backup or sharing.

    Examples:

        orchestra export abc123def --output session.md

        orchestra export --last

        orchestra export abc123def > session.md
    """
    manager = SessionManager()

    # Determine which session to export
    if last:
        session = manager.get_most_recent()
        if not session:
            console.print("[red]No sessions found[/red]")
            sys.exit(1)
        target_id = session.session_id
    elif session_id:
        target_id = session_id
    else:
        console.print("[red]Please provide a session ID or use --last[/red]")
        console.print("[dim]Use 'orchestra sessions' to list available sessions[/dim]")
        sys.exit(1)

    # Export to markdown
    markdown = manager.export_to_markdown(target_id)

    if not markdown:
        console.print(f"[red]Session not found: {target_id}[/red]")
        sys.exit(1)

    # Output
    if output:
        output_path = Path(output)
        output_path.write_text(markdown)
        console.print(f"[green]Exported to {output_path}[/green]")
    else:
        # Write to stdout (bypass rich console for clean output)
        print(markdown)


if __name__ == "__main__":
    main()
