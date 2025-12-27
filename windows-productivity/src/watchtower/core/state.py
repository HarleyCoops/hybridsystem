"""
Watchtower Windows - State Management
Handles persistent state for tasks, sessions, and productivity tracking.
"""

import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from watchtower.core.config import get_config, get_data_dir
from watchtower.types import (
    Task,
    TaskPriority,
    DailyEntry,
    EnergyReading,
    EnergyLevel,
    SprintStatus,
    SprintStatusLevel,
    Session,
    SessionType,
    PatternAnalysis,
    AvoidancePattern,
    EnergyTrend,
    CategoryBalance,
    BurnoutRisk,
)


def generate_id() -> str:
    """Generate a unique ID."""
    return f"{int(datetime.now().timestamp())}-{uuid.uuid4().hex[:8]}"


def get_state_path(filename: str) -> Path:
    """Get path to a state file."""
    return get_data_dir() / filename


def load_json(filename: str, default: dict | list) -> dict | list:
    """Load JSON data from a state file."""
    path = get_state_path(filename)
    if not path.exists():
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return default


def save_json(filename: str, data: dict | list) -> None:
    """Save JSON data to a state file."""
    path = get_state_path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)


# ============================================
# TASK MANAGEMENT
# ============================================


def load_tasks() -> list[Task]:
    """Load all tasks from storage."""
    data = load_json("tasks.json", {"tasks": []})
    return [Task.model_validate(t) for t in data.get("tasks", [])]


def save_tasks(tasks: list[Task]) -> None:
    """Save tasks to storage."""
    save_json("tasks.json", {
        "tasks": [t.model_dump() for t in tasks],
        "last_updated": datetime.now().isoformat(),
    })


def add_task(
    content: str,
    priority: TaskPriority = TaskPriority.STANDARD,
    notes: Optional[list[str]] = None
) -> Task:
    """Add a new task."""
    tasks = load_tasks()
    new_task = Task(
        id=generate_id(),
        content=content,
        priority=priority,
        created_at=datetime.now(),
        notes=notes or [],
    )
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task


def complete_task(task_id: str) -> Optional[Task]:
    """Mark a task as completed."""
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            task.completed_at = datetime.now()
            save_tasks(tasks)
            return task
    return None


def roll_forward_task(task_id: str) -> Optional[Task]:
    """Roll forward an incomplete task."""
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            task.roll_forward_count += 1
            task.notes.append(f"Rolled forward on {datetime.now().strftime('%Y-%m-%d')}")
            save_tasks(tasks)
            return task
    return None


def find_task(identifier: str) -> Optional[Task]:
    """Find a task by ID or content match."""
    tasks = load_tasks()

    # Try exact ID match first
    for task in tasks:
        if task.id == identifier:
            return task

    # Try content match
    identifier_lower = identifier.lower()
    for task in tasks:
        if identifier_lower in task.content.lower():
            return task

    return None


def get_tasks_by_priority(priority: TaskPriority) -> list[Task]:
    """Get active tasks by priority."""
    return [t for t in load_tasks() if t.priority == priority and t.completed_at is None]


def get_avoided_tasks(min_roll_count: int = 3) -> list[Task]:
    """Get tasks that have been rolled forward multiple times."""
    return [
        t for t in load_tasks()
        if t.roll_forward_count >= min_roll_count and t.completed_at is None
    ]


# ============================================
# DAILY ENTRIES
# ============================================


def load_daily_entries() -> dict[str, DailyEntry]:
    """Load all daily entries."""
    data = load_json("daily.json", {"entries": {}})
    entries = {}
    for date, entry_data in data.get("entries", {}).items():
        entries[date] = DailyEntry.model_validate(entry_data)
    return entries


def save_daily_entries(entries: dict[str, DailyEntry]) -> None:
    """Save daily entries."""
    save_json("daily.json", {
        "entries": {date: entry.model_dump() for date, entry in entries.items()}
    })


def get_today_entry() -> DailyEntry:
    """Get or create today's entry."""
    today = datetime.now().strftime("%Y-%m-%d")
    entries = load_daily_entries()

    if today not in entries:
        sprint = get_sprint_status()
        entries[today] = DailyEntry(
            date=today,
            sprint_day=sprint.current_day,
        )
        save_daily_entries(entries)

    return entries[today]


def update_today_entry(updates: dict) -> DailyEntry:
    """Update today's entry with new values."""
    today = datetime.now().strftime("%Y-%m-%d")
    entries = load_daily_entries()
    current = get_today_entry()

    # Merge updates
    entry_dict = current.model_dump()
    entry_dict.update(updates)
    entries[today] = DailyEntry.model_validate(entry_dict)
    save_daily_entries(entries)

    return entries[today]


def add_field_report(report: str) -> None:
    """Add a field report to today's entry."""
    entry = get_today_entry()
    timestamp = datetime.now().strftime("%H:%M")
    entry.field_reports.append(f"[{timestamp}] {report}")
    update_today_entry({"field_reports": entry.field_reports})


# ============================================
# ENERGY TRACKING
# ============================================


def log_energy(level: EnergyLevel, context: Optional[str] = None) -> EnergyReading:
    """Log an energy reading."""
    reading = EnergyReading(
        timestamp=datetime.now(),
        level=level,
        context=context,
    )

    entry = get_today_entry()
    entry.energy_readings.append(reading)
    update_today_entry({"energy_readings": [r.model_dump() for r in entry.energy_readings]})

    return reading


def get_recent_energy_readings(days: int = 7) -> list[EnergyReading]:
    """Get energy readings from the past N days."""
    entries = load_daily_entries()
    cutoff = datetime.now() - timedelta(days=days)
    readings: list[EnergyReading] = []

    for date, entry in entries.items():
        entry_date = datetime.strptime(date, "%Y-%m-%d")
        if entry_date >= cutoff:
            readings.extend(entry.energy_readings)

    return sorted(readings, key=lambda r: r.timestamp)


def calculate_average_energy(readings: list[EnergyReading]) -> float:
    """Calculate average energy level from readings."""
    if not readings:
        return 0.0

    level_values = {
        EnergyLevel.HIGH: 5,
        EnergyLevel.MEDIUM: 4,
        EnergyLevel.LOW: 3,
        EnergyLevel.DEPLETED: 2,
        EnergyLevel.RECOVERY: 1,
    }

    total = sum(level_values[r.level] for r in readings)
    return total / len(readings)


# ============================================
# SPRINT TRACKING
# ============================================


def get_sprint_status() -> SprintStatus:
    """Get current sprint status."""
    data = load_json("sprint.json", {
        "current_day": 1,
        "start_date": datetime.now().strftime("%Y-%m-%d"),
        "last_work_day": datetime.now().strftime("%Y-%m-%d"),
        "rest_days": [],
    })

    config = get_config()
    today = datetime.now().strftime("%Y-%m-%d")

    # Check if we need to update the day count
    if data.get("last_work_day") != today:
        last_work = datetime.strptime(data["last_work_day"], "%Y-%m-%d")
        today_date = datetime.strptime(today, "%Y-%m-%d")
        days_since = (today_date - last_work).days

        if days_since > 1:
            # Rest day(s) detected - reset sprint
            data["current_day"] = 1
            data["start_date"] = today
        else:
            data["current_day"] = data.get("current_day", 0) + 1

        data["last_work_day"] = today
        save_json("sprint.json", data)

    # Determine status
    current_day = data.get("current_day", 1)
    if current_day >= config.sprint.danger_day:
        status = SprintStatusLevel.DANGER
    elif current_day >= config.sprint.warning_day:
        status = SprintStatusLevel.WARNING
    else:
        status = SprintStatusLevel.HEALTHY

    rest_days = data.get("rest_days", [])

    return SprintStatus(
        current_day=current_day,
        start_date=data.get("start_date", today),
        status=status,
        last_rest_day=rest_days[-1] if rest_days else None,
    )


def record_rest_day() -> None:
    """Record a rest day and reset sprint counter."""
    data = load_json("sprint.json", {
        "current_day": 0,
        "start_date": datetime.now().strftime("%Y-%m-%d"),
        "last_work_day": datetime.now().strftime("%Y-%m-%d"),
        "rest_days": [],
    })

    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    rest_days = data.get("rest_days", [])
    rest_days.append(today)

    data["rest_days"] = rest_days
    data["current_day"] = 0
    data["start_date"] = tomorrow

    save_json("sprint.json", data)


# ============================================
# SESSION MANAGEMENT
# ============================================


def get_current_session() -> Optional[Session]:
    """Get the current active session."""
    data = load_json("sessions.json", {"history": []})
    current = data.get("current_session")
    if current:
        return Session.model_validate(current)
    return None


def start_session(session_type: SessionType) -> Session:
    """Start a new session."""
    data = load_json("sessions.json", {"history": []})

    # Archive current session if exists
    if data.get("current_session"):
        data["history"].append(data["current_session"])

    session = Session(
        id=generate_id(),
        started_at=datetime.now(),
        last_activity=datetime.now(),
        type=session_type,
    )

    data["current_session"] = session.model_dump()
    save_json("sessions.json", data)

    return session


def end_session() -> None:
    """End the current session."""
    data = load_json("sessions.json", {"history": []})

    if data.get("current_session"):
        data["history"].append(data["current_session"])
        data["current_session"] = None

    save_json("sessions.json", data)


# ============================================
# PATTERN ANALYSIS
# ============================================


def analyze_patterns() -> PatternAnalysis:
    """Analyze productivity patterns."""
    tasks = load_tasks()
    entries = load_daily_entries()
    sprint = get_sprint_status()
    config = get_config()

    # Avoidance patterns
    avoidance_patterns = [
        AvoidancePattern(
            task_id=t.id,
            task_content=t.content,
            roll_count=t.roll_forward_count,
            first_rolled=t.notes[0].replace("Rolled forward on ", "") if t.notes else t.created_at.isoformat(),
            category=t.priority,
        )
        for t in tasks
        if t.roll_forward_count >= 3 and t.completed_at is None
    ]

    # Energy trends by time of day
    all_readings = get_recent_energy_readings(7)

    morning_readings = [
        r for r in all_readings
        if 6 <= r.timestamp.hour < 12
    ]
    afternoon_readings = [
        r for r in all_readings
        if 12 <= r.timestamp.hour < 18
    ]
    evening_readings = [
        r for r in all_readings
        if r.timestamp.hour >= 18 or r.timestamp.hour < 6
    ]

    energy_trends = [
        EnergyTrend(
            period="morning",
            average_level=calculate_average_energy(morning_readings),
            sample_count=len(morning_readings),
        ),
        EnergyTrend(
            period="afternoon",
            average_level=calculate_average_energy(afternoon_readings),
            sample_count=len(afternoon_readings),
        ),
        EnergyTrend(
            period="evening",
            average_level=calculate_average_energy(evening_readings),
            sample_count=len(evening_readings),
        ),
    ]

    # Completion rate
    cutoff = datetime.now() - timedelta(days=7)
    recent_entries = [
        e for date, e in entries.items()
        if datetime.strptime(date, "%Y-%m-%d") >= cutoff
    ]
    total_completed = sum(len(e.tasks_completed) for e in recent_entries)
    total_rolled = sum(len(e.tasks_rolled_forward) for e in recent_entries)
    completion_rate = (
        total_completed / (total_completed + total_rolled)
        if (total_completed + total_rolled) > 0
        else 0.0
    )

    # Category balance
    active_tasks = [t for t in tasks if t.completed_at is None]
    category_balance = CategoryBalance(
        deep=len([t for t in active_tasks if t.priority == TaskPriority.DEEP]),
        standard=len([t for t in active_tasks if t.priority == TaskPriority.STANDARD]),
        light=len([t for t in active_tasks if t.priority == TaskPriority.LIGHT]),
        someday=len([t for t in active_tasks if t.priority == TaskPriority.SOMEDAY]),
    )

    # Burnout risk assessment
    avg_energy = calculate_average_energy(all_readings)

    if sprint.status == SprintStatusLevel.DANGER or avg_energy < 2.5:
        burnout_risk = BurnoutRisk.HIGH
    elif sprint.status == SprintStatusLevel.WARNING or avg_energy < 3.5:
        burnout_risk = BurnoutRisk.MEDIUM
    else:
        burnout_risk = BurnoutRisk.LOW

    return PatternAnalysis(
        avoidance_patterns=avoidance_patterns,
        energy_trends=energy_trends,
        completion_rate=completion_rate,
        category_balance=category_balance,
        burnout_risk=burnout_risk,
    )


def get_data_summary() -> dict:
    """Get a summary of all productivity data."""
    tasks = load_tasks()
    entries = load_daily_entries()
    sprint = get_sprint_status()
    patterns = analyze_patterns()

    return {
        "total_tasks": len(tasks),
        "active_tasks": len([t for t in tasks if t.completed_at is None]),
        "completed_tasks": len([t for t in tasks if t.completed_at is not None]),
        "avoided_tasks": len(patterns.avoidance_patterns),
        "daily_entries": len(entries),
        "sprint_day": sprint.current_day,
        "sprint_status": sprint.status.value,
        "burnout_risk": patterns.burnout_risk.value,
        "completion_rate": f"{patterns.completion_rate * 100:.1f}%",
    }
