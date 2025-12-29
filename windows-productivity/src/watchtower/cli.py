#!/usr/bin/env python3
"""
Watchtower Windows - CLI Entry Point
Command-line interface for the productivity system.
"""

import asyncio
import sys
import shutil
import winreg
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
from watchtower.utils.windows import (
    create_scheduled_task,
    remove_scheduled_task,
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


@main.command("schedule", short_help="Configure daily briefing schedule")
@click.option("--enable", type=str, help="Enable daily briefing at HH:MM (e.g., '08:00')")
@click.option("--disable", is_flag=True, help="Disable daily briefing schedule")
def cmd_schedule(enable: Optional[str], disable: bool):
    """Configure the Windows Task Scheduler for daily briefings."""
    if enable:
        # Validate time format
        try:
            hours, minutes = map(int, enable.split(":"))
            if not (0 <= hours <= 23 and 0 <= minutes <= 59):
                raise ValueError
        except ValueError:
            print_error("Invalid time format. Use HH:MM (24-hour style), e.g., '08:00'")
            sys.exit(1)

        # Get path to executable
        # If running as script: python -m watchtower
        # If installed: watchtower
        exe = sys.executable
        # We assume the module is installed (or editable) and accessible via 'watchtower' command
        # Ideally, we find the 'watchtower.exe' in Scripts, but invoking via python -m is safer for dev
        # However, Task Scheduler needs a specific command.
        # Let's try to locate the 'watchtower' command if on path.
        
        import shutil
        watchtower_cmd = shutil.which("watchtower")
        
        if watchtower_cmd:
            cmd = f'"{watchtower_cmd}" brief'
        else:
            # Fallback for dev environment: run via python module
            # We need the full path to the module/script
            # Assuming CWD is root of repo, but task scheduler changes dir.
            # Safest is to rely on installed package. 
            print_error("Could not find 'watchtower' command on PATH. Please ensure the package is installed.")
            console.print("[dim]Tip: pip install -e .[/dim]")
            sys.exit(1)

        with Progress(
             SpinnerColumn(),
             TextColumn("[progress.description]{task.description}"),
             console=console,
             transient=True,
        ) as progress:
             progress.add_task("Configuring Windows Task Scheduler...", total=None)
             success = run_async(create_scheduled_task(
                 name="Watchtower Morning Briefing",
                 command=cmd,
                 time=enable,
                 days=["MON", "TUE", "WED", "THU", "FRI"] # Standard work week default
             ))

        if success:
            print_success(f"Daily briefing scheduled for {enable} (Mon-Fri)")
            console.print("[dim]Task: 'Watchtower Morning Briefing' created in Task Scheduler[/dim]")
        else:
            print_error("Failed to create scheduled task.")

    elif disable:
        with Progress(
             SpinnerColumn(),
             TextColumn("[progress.description]{task.description}"),
             console=console,
             transient=True,
        ) as progress:
             progress.add_task("Removing scheduled task...", total=None)
             success = run_async(remove_scheduled_task("Watchtower Morning Briefing"))

        if success:
            print_success("Daily briefing schedule removed")
        else:
            print_error("Failed to remove scheduled task (or it didn't exist).")
    
    else:
        click.echo(ctx.get_help())


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



@main.command("install-menus", short_help="Install Windows context menus")
def cmd_install_menus():
    """Install 'Process as Card' context menu for images."""
    watchtower_cmd = shutil.which("watchtower")
    if not watchtower_cmd:
        print_error("Could not find 'watchtower' command. Is it installed?")
        print_error("Try: pip install -e .")
        return

    # Helper to clean path for registry
    exe_path = f'"{watchtower_cmd}"'

    try:
        # Create key for Background (Directory) - maybe later
        # Create key for Images
        # HKCU\Software\Classes\SystemFileAssociations\image\shell\WatchtowerCard
        
        # We use HKCU to avoid admin requirement
        base_path = r"Software\Classes\SystemFileAssociations\image\shell"
        
        # 1. Process Card
        key_path = f"{base_path}\\WatchtowerCard"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "Process with Watchtower (Card)")
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, watchtower_cmd) # Use exe icon

        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"{key_path}\\command") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, f'{exe_path} card "%1"')
            
        # 2. Process Journal
        key_path = f"{base_path}\\WatchtowerJournal"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "Process with Watchtower (Journal)")
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, watchtower_cmd)

        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"{key_path}\\command") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, f'{exe_path} journal -i "%1"')

        print_success("Windows context menus installed!")
        console.print("[dim]Right-click an image to see 'Process with Watchtower' options.[/dim]")
        # Notify explorer to refresh? hard to do from python without user logoff, but commonly works immediately for HKCU keys
        
    except Exception as e:
        print_error(f"Failed to install registry keys: {e}")

@main.command("uninstall-menus", short_help="Remove Windows context menus")
def cmd_uninstall_menus():
    """Remove Watchtower context menus."""
    try:
        base_path = r"Software\Classes\SystemFileAssociations\image\shell"
        
        # Helper to delete recursively
        def delete_key(key, sub_key):
            try:
                open_key = winreg.OpenKey(key, sub_key, 0, winreg.KEY_ALL_ACCESS)
                info = winreg.QueryInfoKey(open_key)
                for i in range(0, info[0]):
                    # If it has subkeys, delete them first
                    sub = winreg.EnumKey(open_key, 0)
                    delete_key(open_key, sub)
                winreg.DeleteKey(key, sub_key)
            except WindowsError:
                pass

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, base_path, 0, winreg.KEY_ALL_ACCESS) as key:
            delete_key(key, "WatchtowerCard")
            delete_key(key, "WatchtowerJournal")
            
        print_success("Context menus removed.")

    except Exception as e:
        print_error(f"Error removing keys (they might not exist): {e}")


if __name__ == "__main__":
    main()
