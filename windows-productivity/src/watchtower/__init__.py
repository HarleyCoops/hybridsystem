"""
Watchtower Windows - Productivity System powered by Claude Agent SDK

A hybrid physical-digital workflow companion that bridges pen-and-paper
work with AI-powered digital intelligence.
"""

__version__ = "1.0.0"

from watchtower.core.config import get_config, update_config, reset_config
from watchtower.core.state import (
    load_tasks,
    add_task,
    complete_task,
    get_sprint_status,
    log_energy,
    analyze_patterns,
)
from watchtower.core.agent import (
    run_agent,
    run_morning_briefing,
    process_card,
    check_energy,
    run_accountability_check,
)

__all__ = [
    "__version__",
    # Config
    "get_config",
    "update_config",
    "reset_config",
    # State
    "load_tasks",
    "add_task",
    "complete_task",
    "get_sprint_status",
    "log_energy",
    "analyze_patterns",
    # Agent
    "run_agent",
    "run_morning_briefing",
    "process_card",
    "check_energy",
    "run_accountability_check",
]
