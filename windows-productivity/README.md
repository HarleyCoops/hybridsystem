# Watchtower Windows

A Windows productivity system powered by the Claude Code SDK — reimagining the hybrid physical-digital workflow for Windows users.

## Overview

Watchtower Windows bridges the focus benefits of physical pen-and-paper work with AI-powered digital intelligence. Write your daily priorities on an index card, work from it throughout the day, then photograph it to let Claude analyze your patterns and update your productivity system.

### Key Features

- **Physical-Digital Bridge**: Work from a handwritten index card, photograph it for AI processing
- **Pattern Recognition**: Detect avoidance patterns, burnout signals, and energy trends
- **Empathetic Coaching**: Contextual guidance from archetypal voices (Marcus Aurelius, Gandalf, Aragorn)
- **Energy-Based Routing**: Tasks categorized by cognitive demand, matched to your energy levels
- **Sprint Tracking**: Monitor consecutive work days with built-in burnout prevention

## Architecture

Built on the Claude Code SDK for Python:

```
┌─────────────────────────────────────────────────────────┐
│  CLI Layer (Click)                                      │
├─────────────────────────────────────────────────────────┤
│  Agent Orchestration (Claude Code SDK)                  │
├─────────────────────────────────────────────────────────┤
│  Productivity Tools (task, energy, sprint tracking)     │
├─────────────────────────────────────────────────────────┤
│  State Management (Pydantic + JSON persistence)         │
├─────────────────────────────────────────────────────────┤
│  Windows Integrations (notifications, scheduler)        │
└─────────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites

- Python 3.10 or later
- Claude Code SDK installed and configured
- Windows 10/11

### Install from PyPI

```bash
pip install watchtower-windows
```

### Install from source

```bash
git clone https://github.com/your-repo/watchtower-windows
cd watchtower-windows
pip install -e .
```

## Quick Start

### Morning Routine (5 minutes)

```bash
# Generate your daily briefing
watchtower brief

# Review patterns, energy forecast, and suggested priorities
# Write your top 3-5 tasks on a physical index card
```

### During the Day

```bash
# Quick capture new tasks
watchtower add "Review quarterly report" -p deep
watchtower add "Reply to emails" -p light

# Log energy when it shifts
watchtower energy high
watchtower energy low

# Quick status check
watchtower status
```

### Evening Routine (5 minutes)

```bash
# Photograph your index card and process it
watchtower card ~/Pictures/card-today.jpg

# The system will:
# - Read your handwriting via Claude's vision
# - Mark completed tasks (● or ✓)
# - Track rolled-forward tasks (○)
# - Detect avoidance patterns (3+ rolls)
# - Update your productivity metrics
```

## Commands

### Core Commands

| Command | Description |
|---------|-------------|
| `watchtower brief` | Generate morning briefing |
| `watchtower card <image>` | Process photographed index card |
| `watchtower energy [level]` | Log/analyze energy level |
| `watchtower status` | Quick status overview |
| `watchtower add <task>` | Add a new task |
| `watchtower journal [text]` | Process journal entry |
| `watchtower accountability` | Deep pattern analysis |

### Task Priority Levels

```bash
watchtower add "Deep research" -p deep      # High cognitive load
watchtower add "Team standup" -p standard   # Normal energy (default)
watchtower add "File expenses" -p light     # Low energy, easy wins
watchtower add "Learn Rust" -p someday      # Future possibilities
```

### Energy Levels

```bash
watchtower energy high       # Peak performance, deep work time
watchtower energy medium     # Good for standard tasks
watchtower energy low        # Stick to light tasks
watchtower energy depleted   # Consider stopping
watchtower energy recovery   # Take it easy
```

### Optional Modules

```bash
# Weekly Intelligence Review
watchtower weekly

# Deep Work Sessions
watchtower work "Project Alpha"

# Health Tracking (if enabled)
watchtower health ~/data/sleep-report.pdf
watchtower coach "How can I improve my sleep?"
```

## Configuration

### View/Edit Configuration

```bash
watchtower config --show      # View all settings
watchtower config --path      # Show config file location
```

### Enable Optional Modules

```bash
watchtower config --enable-health      # Health tracking
watchtower config --enable-weekly      # Weekly reviews
watchtower config --enable-deepwork    # Deep work sessions
```

## Python API Usage

Use Watchtower as a library in your own applications:

```python
import asyncio
from watchtower import (
    run_morning_briefing,
    process_card,
    add_task,
    log_energy,
    analyze_patterns,
    get_config,
)
from watchtower.types import TaskPriority, EnergyLevel

async def main():
    # Run briefing
    briefing = await run_morning_briefing()
    print(briefing.text)

    # Add task programmatically
    task = add_task("Review PR #123", TaskPriority.STANDARD)
    print(f"Added: {task.id}")

    # Log energy
    log_energy(EnergyLevel.HIGH, "Morning coffee")

    # Get pattern analysis
    patterns = analyze_patterns()
    print(f"Avoidance patterns: {len(patterns.avoidance_patterns)}")

asyncio.run(main())
```

## Data Storage

All data is stored locally in `%APPDATA%\.watchtower\`:

```
%APPDATA%\.watchtower\
├── config.json         # Configuration
├── tasks.json          # Task database
├── daily.json          # Daily entries
├── sprint.json         # Sprint tracking
├── sessions.json       # Session history
└── health-log.md       # Health data (if enabled)
```

## Philosophy

This system is built on several core principles:

1. **Physical constraints create focus**: Writing only 3-5 items on a card forces prioritization
2. **Patterns reveal truth**: Long-term tracking shows what you're really avoiding
3. **Sustainable pace matters**: Built-in burnout detection protects your wellbeing
4. **Compassionate accountability**: Coaching voices meet you where you are

## Development

### Setup Development Environment

```bash
git clone https://github.com/your-repo/watchtower-windows
cd watchtower-windows
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Type Checking

```bash
mypy src/watchtower
```

### Linting

```bash
ruff check src/watchtower
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Powered by: Claude Code SDK by Anthropic
- Inspired by: Cal Newport's deep work principles, GTD methodology, Stoic philosophy
