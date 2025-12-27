#!/usr/bin/env python3
"""
Watchtower Windows - CLI Entry Point
Command-line interface for the productivity system.
"""

import asyncio
import sys
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from watchtower import __version__
from watchtower.core.config import (
    get_config,
    update_config,
    get_config_path,
    ensure_directories,
)
from watchtower.core.agent import (
    run_morning_briefing,
    process_card,
    check_energy,
    run_accountability_check,
    get_status,
    add_task_via_agent,
    process_journal,
    run_weekly_review,
    start_deep_work,
    process_health_data,
    health_coaching,
)
from watchtower.tools.productivity import (
    tool_add_task,
    tool_log_energy,
    tool_get_tasks,
    tool_get_avoided_tasks,
    tool_record_rest_day,
    tool_get_summary,
)

console = Console()

# Initialize directories on startup
ensure_directories()


def run_async(coro):
    """Run an async coroutine synchronously."""
    return asyncio.run(coro)


def print_header(title: str, style: str = "cyan"):
    """Print a styled header."""
    console.print(Panel(title, style=f"bold {style}", expand=False))


def print_error(message: str):
    """Print an error message."""
    console.print(f"[red]✗ {message}[/red]")


def print_success(message: str):
    """Print a success message."""
    console.print(f"[green]✓ {message}[/green]")


@click.group(invoke_without_command=True)
@click.version_option(version=__version__, prog_name="watchtower")
@click.pass_context
def main(ctx):
    """Watchtower Windows - Productivity system powered by Claude Agent SDK."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


# ============================================
# CORE COMMANDS
# ============================================


@main.command("brief", short_help="Generate morning briefing")
def cmd_brief():
    """Generate morning briefing with pattern analysis."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Generating morning briefing...", total=None)
        try:
            result = run_async(run_morning_briefing())
        except Exception as e:
            print_error(f"Failed to generate briefing: {e}")
            sys.exit(1)

    print_header("THE WATCHTOWER - Daily Briefing", "cyan")
    console.print(result.text)
    console.print()


@main.command("card", short_help="Process photographed index card")
@click.argument("image_path", type=click.Path(exists=True))
def cmd_card(image_path: str):
    """Process a photographed index card using vision AI."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Processing card image...", total=None)
        try:
            result = run_async(process_card(image_path))
        except Exception as e:
            print_error(f"Failed to process card: {e}")
            sys.exit(1)

    print_header("CARD PROCESSING COMPLETE", "yellow")
    console.print(result.text)
    console.print()


@main.command("energy", short_help="Log and analyze energy level")
@click.argument("level", required=False)
def cmd_energy(level: Optional[str]):
    """Log and analyze energy level (high/medium/low/depleted/recovery)."""
    if level:
        valid_levels = ["high", "medium", "low", "depleted", "recovery"]
        if level.lower() not in valid_levels:
            print_error(f"Invalid energy level. Choose from: {', '.join(valid_levels)}")
            sys.exit(1)

        result = tool_log_energy(level.lower())
        if result.success:
            print_success(result.message)
        else:
            print_error(result.message)
            sys.exit(1)
    else:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            progress.add_task("Analyzing energy patterns...", total=None)
            try:
                result = run_async(check_energy())
            except Exception as e:
                print_error(f"Failed to analyze energy: {e}")
                sys.exit(1)

        console.print(result.text)


@main.command("status", short_help="Quick status overview")
def cmd_status():
    """Get a quick status overview."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Getting status...", total=None)
        try:
            result = run_async(get_status())
        except Exception as e:
            print_error(f"Failed to get status: {e}")
            sys.exit(1)

    console.print(result.text)


@main.command("add", short_help="Add a new task")
@click.argument("task")
@click.option(
    "-p", "--priority",
    type=click.Choice(["deep", "standard", "light", "someday"], case_sensitive=False),
    default="standard",
    help="Task priority level",
)
def cmd_add(task: str, priority: str):
    """Add a new task to the system."""
    result = tool_add_task(task, priority)
    if result.success:
        print_success(result.message)
    else:
        print_error(result.message)
        sys.exit(1)


@main.command("journal", short_help="Process a journal entry")
@click.argument("content", required=False)
@click.option("-i", "--image", type=click.Path(exists=True), help="Path to handwritten journal image")
def cmd_journal(content: Optional[str], image: Optional[str]):
    """Process a journal entry (text or image)."""
    if not content and not image:
        print_error("Please provide journal content or an image path (-i)")
        sys.exit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Processing journal entry...", total=None)
        try:
            result = run_async(process_journal(content or "", image))
        except Exception as e:
            print_error(f"Failed to process journal: {e}")
            sys.exit(1)

    console.print(result.text)


@main.command("accountability", short_help="Deep pattern analysis")
def cmd_accountability():
    """Perform deep pattern analysis and coaching."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Running accountability check...", total=None)
        try:
            result = run_async(run_accountability_check())
        except Exception as e:
            print_error(f"Failed to run accountability check: {e}")
            sys.exit(1)

    print_header("ACCOUNTABILITY CHECK", "magenta")
    console.print(result.text)
    console.print()


# ============================================
# OPTIONAL MODULE COMMANDS
# ============================================


@main.command("weekly", short_help="Weekly intelligence review")
def cmd_weekly():
    """Generate a comprehensive weekly review."""
    config = get_config()
    if not config.modules.weekly_review:
        console.print("[yellow]Weekly review module is not enabled.[/yellow]")
        console.print("[dim]Enable it with: watchtower config --enable-weekly[/dim]")
        return

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Generating weekly review...", total=None)
        try:
            result = run_async(run_weekly_review())
        except Exception as e:
            print_error(f"Failed to generate weekly review: {e}")
            sys.exit(1)

    print_header("WEEKLY INTELLIGENCE REVIEW", "blue")
    console.print(result.text)
    console.print()


@main.command("work", short_help="Start a deep work session")
@click.argument("project")
def cmd_work(project: str):
    """Start a deep work session for a specific project."""
    config = get_config()
    if not config.modules.deep_work_sessions:
        console.print("[yellow]Deep work sessions module is not enabled.[/yellow]")
        console.print("[dim]Enable it with: watchtower config --enable-deepwork[/dim]")
        return

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Starting deep work session...", total=None)
        try:
            result = run_async(start_deep_work(project))
        except Exception as e:
            print_error(f"Failed to start session: {e}")
            sys.exit(1)

    print_header(f"DEEP WORK: {project.upper()}", "green")
    console.print(result.text)
    console.print()


@main.command("health", short_help="Process health/biometric data")
@click.argument("data_path", type=click.Path(exists=True))
def cmd_health(data_path: str):
    """Process health/biometric data from a file."""
    config = get_config()
    if not config.modules.health:
        console.print("[yellow]Health module is not enabled.[/yellow]")
        console.print("[dim]Enable it with: watchtower config --enable-health[/dim]")
        return

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Processing health data...", total=None)
        try:
            result = run_async(process_health_data(data_path))
        except Exception as e:
            print_error(f"Failed to process health data: {e}")
            sys.exit(1)

    console.print(result.text)


@main.command("coach", short_help="Health coaching Q&A")
@click.argument("question")
def cmd_coach(question: str):
    """Ask a health-related question."""
    config = get_config()
    if not config.modules.health:
        console.print("[yellow]Health module is not enabled.[/yellow]")
        console.print("[dim]Enable it with: watchtower config --enable-health[/dim]")
        return

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Consulting health coach...", total=None)
        try:
            result = run_async(health_coaching(question))
        except Exception as e:
            print_error(f"Failed to get coaching response: {e}")
            sys.exit(1)

    console.print(result.text)


# ============================================
# UTILITY COMMANDS
# ============================================


@main.command("tasks", short_help="List all tasks")
@click.option(
    "-p", "--priority",
    type=click.Choice(["deep", "standard", "light", "someday"], case_sensitive=False),
    help="Filter by priority",
)
def cmd_tasks(priority: Optional[str]):
    """List all active tasks."""
    result = tool_get_tasks(priority)
    console.print()
    console.print(result.message)
    console.print()


@main.command("avoided", short_help="Show avoided tasks")
def cmd_avoided():
    """Show tasks with avoidance patterns (rolled 3+ times)."""
    result = tool_get_avoided_tasks()
    console.print()
    console.print(result.message)
    console.print()


@main.command("rest", short_help="Record a rest day")
def cmd_rest():
    """Record a rest day and reset sprint counter."""
    result = tool_record_rest_day()
    if result.success:
        print_success(result.message)
    else:
        print_error(result.message)


@main.command("summary", short_help="Get data summary")
def cmd_summary():
    """Get a summary of productivity data."""
    result = tool_get_summary()
    console.print()
    console.print(result.message)
    console.print()


@main.command("config", short_help="View or modify configuration")
@click.option("--show", is_flag=True, help="Show current configuration")
@click.option("--path", is_flag=True, help="Show configuration file path")
@click.option("--enable-health", is_flag=True, help="Enable health module")
@click.option("--disable-health", is_flag=True, help="Disable health module")
@click.option("--enable-weekly", is_flag=True, help="Enable weekly review module")
@click.option("--disable-weekly", is_flag=True, help="Disable weekly review module")
@click.option("--enable-deepwork", is_flag=True, help="Enable deep work sessions module")
@click.option("--disable-deepwork", is_flag=True, help="Disable deep work sessions module")
@click.option("--set-timezone", type=str, help="Set timezone")
def cmd_config(
    show: bool,
    path: bool,
    enable_health: bool,
    disable_health: bool,
    enable_weekly: bool,
    disable_weekly: bool,
    enable_deepwork: bool,
    disable_deepwork: bool,
    set_timezone: Optional[str],
):
    """View or modify Watchtower configuration."""
    if path:
        console.print(f"[dim]Config file:[/dim] {get_config_path()}")
        return

    config = get_config()

    if enable_health:
        update_config({"modules": {"health": True}})
        print_success("Health module enabled")

    if disable_health:
        update_config({"modules": {"health": False}})
        console.print("[yellow]Health module disabled[/yellow]")

    if enable_weekly:
        update_config({"modules": {"weekly_review": True}})
        print_success("Weekly review module enabled")

    if disable_weekly:
        update_config({"modules": {"weekly_review": False}})
        console.print("[yellow]Weekly review module disabled[/yellow]")

    if enable_deepwork:
        update_config({"modules": {"deep_work_sessions": True}})
        print_success("Deep work sessions module enabled")

    if disable_deepwork:
        update_config({"modules": {"deep_work_sessions": False}})
        console.print("[yellow]Deep work sessions module disabled[/yellow]")

    if set_timezone:
        update_config({"system": {"timezone": set_timezone}})
        print_success(f"Timezone set to: {set_timezone}")

    # Show config if --show or no options provided
    if show or not any([
        enable_health, disable_health,
        enable_weekly, disable_weekly,
        enable_deepwork, disable_deepwork,
        set_timezone, path,
    ]):
        import json
        console.print("\n[bold]Current Configuration:[/bold]")
        console.print("[dim]" + "─" * 40 + "[/dim]")
        console.print(json.dumps(get_config().model_dump(), indent=2, default=str))


@main.command("help-full", short_help="Show detailed help")
def cmd_help_full():
    """Show detailed help with examples."""
    help_text = """
[bold cyan]WATCHTOWER - Windows Productivity System[/bold cyan]
[dim]Powered by Claude Agent SDK[/dim]

[bold]DAILY WORKFLOW[/bold]
[dim]──────────────────────────────────────────────────[/dim]

  [yellow]Morning (5 min):[/yellow]
    watchtower brief          Generate daily briefing
    → Write top 3-5 tasks on physical index card

  [yellow]During the Day:[/yellow]
    watchtower add "task"     Quick capture new tasks
    watchtower energy high    Log energy level
    watchtower status         Quick status check

  [yellow]Evening (5 min):[/yellow]
    watchtower card photo.jpg Process completed card
    → Photos your handwritten card for OCR

[bold]TASK MANAGEMENT[/bold]
[dim]──────────────────────────────────────────────────[/dim]

  watchtower add "task" -p deep       High-focus task
  watchtower add "task" -p standard   Normal energy (default)
  watchtower add "task" -p light      Low energy / easy win
  watchtower add "task" -p someday    Future possibility

  watchtower tasks                    List all active tasks
  watchtower tasks -p deep            Filter by priority
  watchtower avoided                  Show avoidance patterns

[bold]PATTERN ANALYSIS[/bold]
[dim]──────────────────────────────────────────────────[/dim]

  watchtower accountability   Deep pattern analysis
  watchtower weekly           Weekly intelligence review
  watchtower summary          Quick data summary

[bold]ENERGY & SPRINT[/bold]
[dim]──────────────────────────────────────────────────[/dim]

  Energy levels: high, medium, low, depleted, recovery

  watchtower energy high      Log high energy
  watchtower rest             Record rest day

[bold]OPTIONAL MODULES[/bold]
[dim]──────────────────────────────────────────────────[/dim]

  watchtower work "project"   Start deep work session
  watchtower health data.pdf  Process health data
  watchtower coach "question" Health coaching Q&A

[bold]CONFIGURATION[/bold]
[dim]──────────────────────────────────────────────────[/dim]

  watchtower config --show    View current config
  watchtower config --path    Show config file location

  Enable/disable modules:
    --enable-health, --disable-health
    --enable-weekly, --disable-weekly
    --enable-deepwork, --disable-deepwork

[dim]For more info: https://github.com/your-repo/watchtower-windows[/dim]
"""
    console.print(help_text)


if __name__ == "__main__":
    main()
