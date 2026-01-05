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


if __name__ == "__main__":
    main()
