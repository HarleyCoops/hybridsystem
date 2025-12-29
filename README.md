# Hybrid System

A Windows productivity system that bridges pen-and-paper workflow with AI-powered digital intelligence.

**Morning:** AI generates daily priorities
**Day:** Work from a physical card
**Evening:** Photo your card → AI reads handwriting → updates everything automatically

Built with [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and the Claude Agent SDK.

---

## Quick Start

**Requirements:**
- Windows 10/11
- Python 3.10 or later
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (requires Claude subscription)

**Install:**

```bash
git clone https://github.com/krispuckett/hybridsystem.git
cd hybridsystem/windows-productivity
pip install -e .
```

**Setup takes 10 minutes.** Follow the [Setup Guide](docs/SETUP.md).

---

## How It Works

### Physical-Digital Bridge

The system leverages the focus benefits of physical pen-and-paper work combined with AI-powered digital intelligence:

1. **Morning:** Run `watchtower brief` to get AI-generated priorities
2. **Write:** Transfer top 3-5 tasks to a physical index card
3. **Work:** Focus on the card throughout your day
4. **Evening:** Photograph your card and run `watchtower card photo.jpg`

The AI reads your handwriting, tracks completions, and detects patterns.

### Daily Workflow

**Morning (5 min):**
```bash
watchtower brief
```
Generates priorities. Write top 3-5 on a physical card.

**Evening (5 min):**
```bash
watchtower card ~/Pictures/card-photo.jpg
```
AI reads handwriting, updates tasks automatically.

**Anytime:**
```bash
watchtower add "task description" -p standard    # Add task
watchtower energy high                           # Log energy level
watchtower status                                # Quick overview
```

---

## Commands

### Core Commands
| Command | Description |
|---------|-------------|
| `watchtower brief` | Generate morning priorities |
| `watchtower card <image>` | Process end-of-day card photo |
| `watchtower energy [level]` | Log/analyze energy level |
| `watchtower status` | Quick system overview |

### Task Management
| Command | Description |
|---------|-------------|
| `watchtower add "task" -p [level]` | Add task (deep/standard/light/someday) |
| `watchtower tasks` | List all active tasks |
| `watchtower avoided` | Show tasks with avoidance patterns |

### Pattern Analysis
| Command | Description |
|---------|-------------|
| `watchtower accountability` | Deep pattern analysis + coaching |
| `watchtower weekly` | Weekly intelligence review |
| `watchtower summary` | Quick data summary |

### Focus & Health (Optional Modules)
| Command | Description |
|---------|-------------|
| `watchtower work "project"` | Start deep work session |
| `watchtower journal [text]` | Process journal entry |
| `watchtower health <file>` | Process biometric data |
| `watchtower coach "question"` | Evidence-based health Q&A |

---

## Energy-Based Task Routing

Tasks are categorized by energy requirement:

| Level | Category | When to Do |
|-------|----------|------------|
| `deep` | Deep Work | Peak energy windows only |
| `standard` | Standard Work | Productive but not peak |
| `light` | Light Work | Tired, admin, easy wins |
| `someday` | Future Ideas | When inspiration strikes |

The system learns your patterns and routes you to appropriate work based on your current energy.

---

## Pattern Detection

The system tracks:

- **Avoidance patterns**: Tasks rolled forward 3+ times get flagged
- **Sprint health**: Warns when you've been pushing too long
- **Energy trends**: Correlates energy levels with completion rates
- **Category imbalances**: Notices if one type of work is accumulating

---

## Coaching Voices

When patterns warrant it, coaching uses three archetypal voices:

- **Marcus Aurelius** — When avoiding known hard work (Stoic discipline)
- **Gandalf** — When showing burnout signals (wise patience)
- **Aragorn** — When scattered across too many fronts (commander clarity)

These can be customized in your configuration.

---

## Configuration

View and modify settings:

```bash
watchtower config --show      # View all settings
watchtower config --path      # Show config file location
```

Enable optional modules:
```bash
watchtower config --enable-health      # Health tracking
watchtower config --enable-weekly      # Weekly reviews
watchtower config --enable-deepwork    # Deep work sessions
```

See [Customization Guide](docs/CUSTOMIZATION.md) for details.

---

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

Everything runs locally. Your data stays yours.

---

## Windows Integration

### Scheduled Briefings

```bash
watchtower schedule --enable 08:00    # Daily briefing at 8 AM
watchtower schedule --disable         # Remove schedule
```

### Context Menus

```bash
watchtower install-menus     # Add right-click options for images
watchtower uninstall-menus   # Remove context menus
```

---

## Philosophy

This system assumes:

- **Your capacity varies day-to-day** — Energy levels matter
- **Physical constraints improve focus** — A paper card limits what you can carry
- **Digital intelligence improves routing** — AI helps you pick the right work
- **Patterns emerge when tracked** — Consistency reveals insights
- **Recovery is strategy, not weakness** — Sustainable pace beats heroic sprints

Built for people who work in energy waves, not steady streams.

---

## Documentation

- [Setup Guide](docs/SETUP.md) — Initial configuration
- [Customization](docs/CUSTOMIZATION.md) — Adapt to your workflow
- [Health Module](docs/HEALTH-MODULE.md) — Biometric tracking (optional)
- [Troubleshooting](docs/TROUBLESHOOTING.md) — Common issues

---

## License

MIT — Use freely, modify as needed, share improvements.

---

## Acknowledgments

Built exploring what's possible with:
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Agent SDK](https://docs.anthropic.com/en/docs/agents-and-tools)
- [Model Context Protocol](https://modelcontextprotocol.io)

---

## Questions?

Open an issue or reach out: [@krispuckett](https://twitter.com/krispuckett)

---

**Cost:** $0 (with existing Claude subscription)
**Setup time:** 10 minutes
**Daily overhead:** 10 minutes (5 min morning + 5 min evening)
