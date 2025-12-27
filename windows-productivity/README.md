# Watchtower Windows

A Windows productivity system powered by the Claude Agent SDK — reimagining the hybrid physical-digital workflow for Windows users.

## Overview

Watchtower Windows bridges the focus benefits of physical pen-and-paper work with AI-powered digital intelligence. Write your daily priorities on an index card, work from it throughout the day, then photograph it to let Claude analyze your patterns and update your productivity system.

### Key Features

- **Physical-Digital Bridge**: Work from a handwritten index card, photograph it for AI processing
- **Pattern Recognition**: Detect avoidance patterns, burnout signals, and energy trends
- **Empathetic Coaching**: Contextual guidance from archetypal voices (Marcus Aurelius, Gandalf, Aragorn)
- **Energy-Based Routing**: Tasks categorized by cognitive demand, matched to your energy levels
- **Sprint Tracking**: Monitor consecutive work days with built-in burnout prevention

## Architecture

Built on the Claude Agent SDK, this system provides:

```
┌─────────────────────────────────────────────────────────┐
│  CLI Layer (watchtower command)                         │
├─────────────────────────────────────────────────────────┤
│  Agent Orchestration (Claude SDK integration)           │
├─────────────────────────────────────────────────────────┤
│  Productivity Tools (task, energy, sprint tracking)     │
├─────────────────────────────────────────────────────────┤
│  State Management (JSON-based persistence)              │
├─────────────────────────────────────────────────────────┤
│  Windows Integrations (notifications, scheduler)        │
└─────────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites

- Node.js 20 or later
- Claude Code CLI installed and configured
- Windows 10/11 (or macOS/Linux for cross-platform use)

### Install from npm

```bash
npm install -g watchtower-windows
```

### Install from source

```bash
git clone https://github.com/your-repo/watchtower-windows
cd watchtower-windows
npm install
npm run build
npm link
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

| Command | Alias | Description |
|---------|-------|-------------|
| `watchtower brief` | `b` | Generate morning briefing |
| `watchtower card <image>` | `c` | Process photographed index card |
| `watchtower energy [level]` | `e` | Log/analyze energy level |
| `watchtower status` | `s` | Quick status overview |
| `watchtower add <task>` | `a` | Add a new task |
| `watchtower journal [text]` | `j` | Process journal entry |
| `watchtower accountability` | `acc` | Deep pattern analysis |

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

### Configuration Options

The config file supports:

```json
{
  "documents": {
    "daily": "The Watchtower",
    "tasks": "The Forge",
    "journey": "The Long Road"
  },
  "energyWindows": [
    { "start": 9, "end": 13, "label": "Morning Focus" },
    { "start": 15, "end": 18, "label": "Afternoon Drive" }
  ],
  "sprint": {
    "warningDay": 14,
    "dangerDay": 21
  },
  "voices": {
    "discipline": "Marcus Aurelius",
    "wisdom": "Gandalf",
    "leadership": "Aragorn"
  }
}
```

## Pattern Detection

### Avoidance Patterns

Tasks rolled forward 3+ times trigger avoidance alerts. The system tracks:
- Which tasks you're avoiding
- How long they've been avoided
- Category patterns (avoiding deep work?)

### Sprint Health

Consecutive work days are tracked to prevent burnout:
- **Day 1-13**: Healthy sprint
- **Day 14+**: Warning zone
- **Day 21+**: Danger zone - rest recommended

Use `watchtower rest` to record a rest day and reset the counter.

### Energy Trends

The system correlates your energy readings with:
- Time of day patterns
- Completion rates
- Task category success

## Windows Integration

### Toast Notifications

Get notified of important events:

```typescript
import { sendNotification } from 'watchtower-windows';

await sendNotification('Sprint Warning', 'Day 14 - consider a rest day');
```

### Task Scheduler

Automate your morning briefing:

```typescript
import { createScheduledTask } from 'watchtower-windows';

await createScheduledTask('WatchtowerBrief', 'watchtower brief', {
  time: '08:00',
  days: ['MON', 'TUE', 'WED', 'THU', 'FRI']
});
```

## API Usage

Use Watchtower as a library in your own applications:

```typescript
import {
  runMorningBriefing,
  processCard,
  toolAddTask,
  toolLogEnergy,
  analyzePatterns
} from 'watchtower-windows';

// Run briefing
const briefing = await runMorningBriefing();
console.log(briefing.text);

// Add task programmatically
const result = toolAddTask('Review PR #123', 'standard');

// Get pattern analysis
const patterns = analyzePatterns();
console.log(patterns.avoidancePatterns);
```

## Data Storage

All data is stored locally:

```
~/.watchtower/
├── tasks.json          # Task database
├── daily.json          # Daily entries
├── sprint.json         # Sprint tracking
├── sessions.json       # Session history
└── health-log.md       # Health data (if enabled)
```

On Windows, this is typically:
```
%APPDATA%\watchtower\
```

## Philosophy

This system is built on several core principles:

1. **Physical constraints create focus**: Writing only 3-5 items on a card forces prioritization
2. **Patterns reveal truth**: Long-term tracking shows what you're really avoiding
3. **Sustainable pace matters**: Built-in burnout detection protects your wellbeing
4. **Compassionate accountability**: Coaching voices meet you where you are

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Original Mac version: Hybrid Productivity System
- Powered by: Claude Agent SDK by Anthropic
- Inspired by: Cal Newport's deep work principles, GTD methodology, Stoic philosophy
