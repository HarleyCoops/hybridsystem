# Hybrid System

A productivity system that bridges pen-and-paper workflow with AI-powered digital intelligence.

**Morning:** AI generates daily priorities  
**Day:** Work from a physical card  
**Evening:** Photo your card → AI reads handwriting → updates everything automatically

Built with [Craft Docs](https://craft.do), [Claude Code](https://docs.anthropic.com/en/docs/claude-code), and Craft's MCP server.

---

## Quick Start

**Requirements:**
- macOS
- [Craft Docs](https://www.craft.do) (free tier works)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (requires Claude subscription)

**Install:**

```bash
git clone https://github.com/krispuckett/hybridsystem.git
cd hybridsystem
./install.sh
```

**Setup takes 10 minutes.** Follow the [Setup Guide](docs/SETUP.md).

---

## How It Works

### Three Connected Documents

**The Watchtower** (Daily Hub)
- Morning briefing with prioritized tasks
- Field reports for quick captures
- Links to your task pool

**The Forge** (Task Pool)
- Organized by energy requirement
- Deep Work, Standard Tasks, Light Work, Someday

**The Long Road** (Journey Tracker)
- Work/rest cycle tracking
- Pattern recognition over time
- Insights from reflections

### Daily Workflow

**Morning (5 min):**
```bash
watchtower brief
```
Generates priorities. Write top 3-5 on a physical card.

**Evening (5 min):**
```bash
watchtower card ~/Downloads/card-photo.jpg
```
AI reads handwriting, updates tasks automatically.

**Anytime:**
```bash
watchtower add "task description" normal    # Add task
watchtower energy                           # Check/log energy
watchtower status                           # Quick overview
```

---

## Commands

### Daily Workflow
| Command | Description |
|---------|-------------|
| `watchtower brief` | Generate morning priorities |
| `watchtower card <image>` | Process end-of-day card photo |
| `watchtower energy` | Check and log energy level |

### Task Management
| Command | Description |
|---------|-------------|
| `watchtower add "task" [level]` | Add task (high/normal/low/someday) |
| `watchtower status` | Quick system overview |

### Accountability
| Command | Description |
|---------|-------------|
| `watchtower accountability` | Deep pattern analysis + coaching |
| `watchtower weekly` | Weekly intelligence review |

### Focus
| Command | Description |
|---------|-------------|
| `watchtower work "project"` | Start deep work session |
| `watchtower journal` | Process journal entry |

### Health (Optional Module)
| Command | Description |
|---------|-------------|
| `watchtower health <file>` | Process any biometric data |
| `watchtower coach` | Evidence-based health Q&A |

---

## Energy-Based Task Routing

Tasks are categorized by energy requirement:

| Level | Category | When to Do |
|-------|----------|------------|
| `high` | Deep Work | Peak energy windows only |
| `normal` | Standard Work | Productive but not peak |
| `low` | Light Work | Tired, admin, easy wins |
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

These can be customized in `~/.watchtower/config`.

---

## Customization

Edit `~/.watchtower/config` to customize:

- Peak energy windows
- Sprint warning thresholds
- Coaching voice names
- Document names
- Task categories

See [Customization Guide](docs/CUSTOMIZATION.md) for details.

---

## Optional: Health Module

The health module is tool-agnostic and privacy-focused:

- Accepts data from any wearable or lab (Oura, Whoop, Apple Watch, blood work PDFs, etc.)
- Stores data locally in `~/.watchtower/health-log.md`
- Not synced to Craft by default
- Provides evidence-based guidance, not medical advice

Enable during installation or edit config:
```bash
HEALTH_MODULE_ENABLED=true
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

## Technical Details

- **Vision AI** reads handwritten text (~90% accuracy on cursive)
- **Craft MCP** enables direct document updates via Model Context Protocol
- **Bash scripts** handle automation without complex dependencies
- **Config file** allows full customization without editing scripts

Everything runs locally. Your data stays yours.

---

## License

MIT — Use freely, modify as needed, share improvements.

---

## Acknowledgments

Built exploring what's possible with:
- [Craft's MCP server](https://www.craft.do/imagine/guide/mcp/claude_code)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- [Model Context Protocol](https://modelcontextprotocol.io)

---

## Questions?

Open an issue or reach out: [@krispuckett](https://twitter.com/krispuckett)

---

**Cost:** $0 (with existing Claude subscription)  
**Setup time:** 10 minutes  
**Daily overhead:** 10 minutes (5 min morning + 5 min evening)
