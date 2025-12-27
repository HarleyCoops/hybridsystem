"""
Watchtower Windows - Productivity Tools
Tools for task management and productivity tracking.
"""

from datetime import datetime
from typing import Optional

from watchtower.core.config import get_config, get_category_name
from watchtower.core.state import (
    load_tasks,
    save_tasks,
    add_task as state_add_task,
    complete_task,
    roll_forward_task,
    find_task,
    get_tasks_by_priority,
    get_avoided_tasks,
    log_energy as state_log_energy,
    get_today_entry,
    update_today_entry,
    add_field_report,
    get_sprint_status,
    record_rest_day as state_record_rest_day,
    start_session,
    end_session,
    analyze_patterns,
    get_data_summary,
)
from watchtower.types import (
    TaskPriority,
    EnergyLevel,
    SessionType,
    ToolResponse,
    Task,
)


# ============================================
# TASK MANAGEMENT TOOLS
# ============================================


def tool_add_task(
    content: str,
    priority: str = "standard",
    notes: Optional[str] = None,
) -> ToolResponse:
    """Add a new task to the system."""
    try:
        priority_enum = TaskPriority(priority.lower())
    except ValueError:
        return ToolResponse(
            success=False,
            message=f"Invalid priority: {priority}. Choose from: deep, standard, light, someday",
        )

    try:
        task = state_add_task(content, priority_enum, [notes] if notes else None)
        category_name = get_category_name(priority)

        return ToolResponse(
            success=True,
            message=f'Task added to {category_name}: "{content}"',
            data={"task_id": task.id, "priority": priority, "category": category_name},
        )
    except Exception as e:
        return ToolResponse(
            success=False,
            message=f"Failed to add task: {e}",
        )


def tool_complete_task(task_id_or_content: str) -> ToolResponse:
    """Mark a task as completed."""
    try:
        task = find_task(task_id_or_content)

        if not task:
            return ToolResponse(
                success=False,
                message=f'Task not found: "{task_id_or_content}"',
            )

        if task.completed_at:
            return ToolResponse(
                success=False,
                message=f'Task already completed: "{task.content}"',
            )

        complete_task(task.id)

        # Update today's entry
        entry = get_today_entry()
        tasks_completed = entry.tasks_completed.copy()
        tasks_completed.append(task.id)
        update_today_entry({"tasks_completed": tasks_completed})

        return ToolResponse(
            success=True,
            message=f'Completed: "{task.content}"',
            data={"task_id": task.id, "completed_at": datetime.now().isoformat()},
        )
    except Exception as e:
        return ToolResponse(
            success=False,
            message=f"Failed to complete task: {e}",
        )


def tool_roll_forward_task(task_id_or_content: str) -> ToolResponse:
    """Roll forward an incomplete task."""
    try:
        task = find_task(task_id_or_content)

        if not task:
            return ToolResponse(
                success=False,
                message=f'Task not found: "{task_id_or_content}"',
            )

        updated = roll_forward_task(task.id)
        if not updated:
            return ToolResponse(
                success=False,
                message="Failed to roll forward task",
            )

        # Update today's entry
        entry = get_today_entry()
        tasks_rolled = entry.tasks_rolled_forward.copy()
        tasks_rolled.append(task.id)
        update_today_entry({"tasks_rolled_forward": tasks_rolled})

        is_avoided = updated.roll_forward_count >= 3

        if is_avoided:
            message = f'⚠️ AVOIDANCE PATTERN: "{task.content}" has been rolled forward {updated.roll_forward_count} times'
        else:
            message = f'Rolled forward: "{task.content}" ({updated.roll_forward_count}x)'

        return ToolResponse(
            success=True,
            message=message,
            data={
                "task_id": task.id,
                "roll_count": updated.roll_forward_count,
                "is_avoidance_pattern": is_avoided,
            },
        )
    except Exception as e:
        return ToolResponse(
            success=False,
            message=f"Failed to roll forward task: {e}",
        )


def tool_get_tasks(priority: Optional[str] = None) -> ToolResponse:
    """Get tasks by priority/category."""
    try:
        config = get_config()

        if priority:
            try:
                priority_enum = TaskPriority(priority.lower())
                tasks = get_tasks_by_priority(priority_enum)
            except ValueError:
                return ToolResponse(
                    success=False,
                    message=f"Invalid priority: {priority}",
                )
        else:
            tasks = [t for t in load_tasks() if t.completed_at is None]

        grouped: dict[str, list[Task]] = {
            "deep": [],
            "standard": [],
            "light": [],
            "someday": [],
        }

        for task in tasks:
            grouped[task.priority.value].append(task)

        def format_tasks(task_list: list[Task]) -> list[str]:
            return [
                f"• {t.content}" + (f" [rolled {t.roll_forward_count}x]" if t.roll_forward_count > 0 else "")
                for t in task_list
            ]

        if priority:
            priority_enum = TaskPriority(priority.lower())
            category_name = get_category_name(priority)
            formatted = format_tasks(grouped[priority_enum.value])
            message = f"{category_name}:\n" + ("\n".join(formatted) if formatted else "No tasks")
        else:
            sections = []
            for p in ["deep", "standard", "light", "someday"]:
                if grouped[p]:
                    category_name = get_category_name(p)
                    formatted = format_tasks(grouped[p])
                    sections.append(f"{category_name}:\n" + "\n".join(formatted))
            message = "\n\n".join(sections) if sections else "No active tasks"

        return ToolResponse(
            success=True,
            message=message,
            data={"tasks": [t.model_dump() for t in tasks], "count": len(tasks)},
        )
    except Exception as e:
        return ToolResponse(
            success=False,
            message=f"Failed to get tasks: {e}",
        )


def tool_get_avoided_tasks() -> ToolResponse:
    """Get tasks that have been rolled forward 3+ times."""
    try:
        avoided = get_avoided_tasks()

        if not avoided:
            return ToolResponse(
                success=True,
                message="No avoidance patterns detected. Great job staying on top of tasks!",
                data={"tasks": [], "count": 0},
            )

        config = get_config()
        sorted_tasks = sorted(avoided, key=lambda t: t.roll_forward_count, reverse=True)

        lines = [
            f'• "{t.content}" - rolled {t.roll_forward_count}x ({get_category_name(t.priority.value)})'
            for t in sorted_tasks
        ]

        return ToolResponse(
            success=True,
            message="⚠️ Avoidance Patterns Detected:\n" + "\n".join(lines),
            data={"tasks": [t.model_dump() for t in avoided], "count": len(avoided)},
        )
    except Exception as e:
        return ToolResponse(
            success=False,
            message=f"Failed to get avoided tasks: {e}",
        )


# ============================================
# ENERGY TRACKING TOOLS
# ============================================


def tool_log_energy(level: str, context: Optional[str] = None) -> ToolResponse:
    """Log an energy reading."""
    try:
        level_enum = EnergyLevel(level.lower())
    except ValueError:
        valid = ", ".join(e.value for e in EnergyLevel)
        return ToolResponse(
            success=False,
            message=f"Invalid energy level: {level}. Choose from: {valid}",
        )

    try:
        reading = state_log_energy(level_enum, context)
        sprint = get_sprint_status()

        recommendations = {
            EnergyLevel.HIGH: "Perfect time for deep work!",
            EnergyLevel.MEDIUM: "Good for standard tasks.",
            EnergyLevel.LOW: "Focus on light tasks or take a break.",
            EnergyLevel.DEPLETED: "Consider stopping for today. Rest is productive.",
            EnergyLevel.RECOVERY: "Take it easy. Gentle tasks only.",
        }

        recommendation = recommendations[level_enum]

        if sprint.status.value == "danger":
            recommendation += f" ⚠️ Sprint day {sprint.current_day} - consider a rest day soon."

        return ToolResponse(
            success=True,
            message=f"Energy logged: {level}. {recommendation}",
            data={
                "reading": reading.model_dump(),
                "sprint_day": sprint.current_day,
                "sprint_status": sprint.status.value,
            },
        )
    except Exception as e:
        return ToolResponse(
            success=False,
            message=f"Failed to log energy: {e}",
        )


# ============================================
# SPRINT & SESSION TOOLS
# ============================================


def tool_get_sprint_status() -> ToolResponse:
    """Get current sprint status."""
    try:
        sprint = get_sprint_status()
        config = get_config()

        message = f"Sprint Day {sprint.current_day}"

        if sprint.status.value == "danger":
            message += f" ⚠️ DANGER - You've worked {sprint.current_day} consecutive days. Take a rest day!"
        elif sprint.status.value == "warning":
            days_until_danger = config.sprint.danger_day - sprint.current_day
            message += f" ⚡ Warning - Day {sprint.current_day}. Rest day recommended within {days_until_danger} days."
        else:
            message += f" ✓ Healthy sprint (warning at day {config.sprint.warning_day})"

        if sprint.last_rest_day:
            message += f"\nLast rest day: {sprint.last_rest_day}"

        return ToolResponse(
            success=True,
            message=message,
            data=sprint.model_dump(),
        )
    except Exception as e:
        return ToolResponse(
            success=False,
            message=f"Failed to get sprint status: {e}",
        )


def tool_record_rest_day() -> ToolResponse:
    """Record a rest day and reset sprint counter."""
    try:
        state_record_rest_day()
        return ToolResponse(
            success=True,
            message="🌙 Rest day recorded. Sprint counter reset. Enjoy your recovery!",
            data={"rest_day": datetime.now().strftime("%Y-%m-%d")},
        )
    except Exception as e:
        return ToolResponse(
            success=False,
            message=f"Failed to record rest day: {e}",
        )


def tool_start_session(
    session_type: str,
    context: Optional[dict] = None,
) -> ToolResponse:
    """Start a productivity session."""
    try:
        type_enum = SessionType(session_type.lower())
    except ValueError:
        valid = ", ".join(e.value for e in SessionType)
        return ToolResponse(
            success=False,
            message=f"Invalid session type: {session_type}. Choose from: {valid}",
        )

    try:
        session = start_session(type_enum)

        return ToolResponse(
            success=True,
            message=f"Session started: {session_type}",
            data={"session_id": session.id, "started_at": session.started_at.isoformat()},
        )
    except Exception as e:
        return ToolResponse(
            success=False,
            message=f"Failed to start session: {e}",
        )


def tool_end_session() -> ToolResponse:
    """End the current session."""
    try:
        end_session()
        return ToolResponse(
            success=True,
            message="Session ended.",
        )
    except Exception as e:
        return ToolResponse(
            success=False,
            message=f"Failed to end session: {e}",
        )


# ============================================
# FIELD REPORTS
# ============================================


def tool_add_field_report(report: str) -> ToolResponse:
    """Add a field report (quick capture)."""
    try:
        add_field_report(report)
        return ToolResponse(
            success=True,
            message=f'Field report logged: "{report}"',
            data={"timestamp": datetime.now().strftime("%H:%M")},
        )
    except Exception as e:
        return ToolResponse(
            success=False,
            message=f"Failed to add field report: {e}",
        )


# ============================================
# ANALYSIS TOOLS
# ============================================


def tool_get_pattern_analysis() -> ToolResponse:
    """Get comprehensive pattern analysis."""
    try:
        patterns = analyze_patterns()
        config = get_config()

        lines = ["## Pattern Analysis\n"]

        # Avoidance patterns
        if patterns.avoidance_patterns:
            lines.append("### ⚠️ Avoidance Patterns")
            for p in patterns.avoidance_patterns:
                category = get_category_name(p.category.value)
                lines.append(f'• "{p.task_content}" - {p.roll_count}x rolls ({category})')
            lines.append("")

        # Energy trends
        lines.append("### Energy Trends (7 days)")
        for t in patterns.energy_trends:
            bar = "█" * round(t.average_level)
            lines.append(f"• {t.period}: {bar} {t.average_level:.1f}/5")
        lines.append("")

        # Completion rate
        lines.append(f"### Completion Rate: {patterns.completion_rate * 100:.0f}%\n")

        # Burnout risk
        risk_emoji = {"low": "✓", "medium": "⚡", "high": "⚠️"}
        lines.append(f"### Burnout Risk: {risk_emoji[patterns.burnout_risk.value]} {patterns.burnout_risk.value}")

        return ToolResponse(
            success=True,
            message="\n".join(lines),
            data=patterns.model_dump(),
        )
    except Exception as e:
        return ToolResponse(
            success=False,
            message=f"Failed to get pattern analysis: {e}",
        )


def tool_get_summary() -> ToolResponse:
    """Get overall data summary."""
    try:
        summary = get_data_summary()
        sprint = get_sprint_status()
        entry = get_today_entry()

        lines = [
            "## Watchtower Status\n",
            f"**Sprint:** Day {sprint.current_day} ({sprint.status.value})",
            f"**Active Tasks:** {summary['active_tasks']}",
            f"**Completed Today:** {len(entry.tasks_completed)}",
            f"**Rolled Today:** {len(entry.tasks_rolled_forward)}",
            f"**7-Day Completion:** {summary['completion_rate']}",
            f"**Burnout Risk:** {summary['burnout_risk']}",
        ]

        if summary["avoided_tasks"] > 0:
            lines.append(f"\n⚠️ **{summary['avoided_tasks']} tasks** showing avoidance patterns")

        return ToolResponse(
            success=True,
            message="\n".join(lines),
            data=summary,
        )
    except Exception as e:
        return ToolResponse(
            success=False,
            message=f"Failed to get summary: {e}",
        )
