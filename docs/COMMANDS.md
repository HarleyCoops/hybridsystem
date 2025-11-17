# Commands Reference

All available commands in the Hybrid System.

## Daily Workflow Commands

### `watchtower brief`
**Generate morning briefing**

Reads all three Craft documents and creates a prioritized daily briefing in The Watchtower.

**When to use:** Every morning before starting work

**What it does:**
- Analyzes tasks in The Forge
- Checks patterns in The Long Road
- Generates 3-5 top priorities
- Updates The Watchtower document

**Example output in Craft:**
```
## Today's Mission Briefing
1. Complete Epilogue liquid glass effects (Deep Work - 9-1pm window)
2. Finish Claude Skills tutorial outline (Standard Work)
3. Review Ramp interview notes (Standard Work)

Recommended: Start with #1 during peak energy (9am-1pm)
```

---

### `watchtower card`
**Process end-of-day card photo**

Opens Claude Code in interactive mode to read your handwritten card.

**When to use:** End of every working day

**Steps:**
1. Take photo of your completed card
2. Run `watchtower card`
3. Drag photo into Claude Code terminal
4. Press Enter
5. AI reads handwriting and updates Forge
6. Answer energy level question (1-4)

**What it updates:**
- Marks completed tasks as `[x]` in The Forge
- Rolls incomplete tasks forward
- Logs energy level in The Long Road
- Tracks work/rest cycles

---

### `watchtower add "task description" [energy]`
**Quick task capture**

Adds a single task to The Forge.

**Energy levels:**
- `high` → Deep Work section
- `normal` → Standard Work section (default)
- `low` → Light Work section
- `someday` → Someday/Maybe section

**Examples:**
```bash
watchtower add "Research Metal shader performance" high
watchtower add "Update project README" normal
watchtower add "Organize desktop files" low
watchtower add "Learn about SwiftUI animations" someday
```

---

### `watchtower journal`
**Process journal entry photo**

Reads handwritten journal entries and extracts insights.

**When to use:** After journaling sessions

**Steps:**
1. Take photo of journal page
2. Run `watchtower journal`
3. Drag photo into terminal
4. Press Enter

**What it does:**
- Transcribes cursive handwriting
- Extracts key insights and observations
- Adds reflections to The Long Road
- Identifies actionable items → adds to The Forge
- Preserves your voice and tone

---

## Quick Reference Commands

### `watchtower status`
**System overview**

Shows current state across all three documents.

**Output includes:**
- Current work/rest cycle day
- Recent energy patterns
- Task counts by category
- Any alerts or warnings

**Example:**
```
Current Cycle: Day 3
Recent Energy: High, Medium, High
Task Pool:
  - Deep Work: 4 tasks
  - Standard: 8 tasks
  - Light: 2 tasks
Alerts: None - system healthy
```

---

### `watchtower capture`
**Brain dump mode**

For when multiple thoughts hit at once.

**How to use:**
```bash
watchtower capture
```

Then paste or type all your scattered thoughts. Press Ctrl+D when done.

**What it does:**
- Sorts thoughts into categories (tasks, ideas, concerns)
- Assigns energy levels to tasks
- Routes to appropriate Craft documents
- Flags patterns (overwhelm, fatigue, avoidance)

---

### `watchtower work "project name"`
**Start focused work session**

Launches a structured deep work session.

**Example:**
```bash
watchtower work "Claude Skills deep dive"
```

**What it does:**
- Checks your current energy level
- Helps define 2-3 session goals
- Creates session notes file
- Tracks what you accomplish
- Updates Craft docs with progress
- Keeps you on track (calls out pivots)

**Session notes saved to:** `~/.watchtower/sessions/`

---

### `watchtower energy`
**Energy level check-in**

Quick assessment of current capacity with recommendations.

**Prompts you:**
1. Current sprint day
2. Recent energy pattern  
3. Your actual energy level right now
4. Recommendations based on your state

**Helps you decide:**
- Should I be working at all?
- What type of work matches my energy?
- Do I need a break?

---

### `watchtower context`
**Manage Claude Code context**

Helps manage conversation history to prevent context bloat.

**When to use:**
- After 2-3 days of use
- When Claude seems slow or repetitive
- Before starting a new project

**What it does:**
- Checks for active Claude sessions
- Guides you through clearing context
- Explains when to start fresh
- Helps archive important sessions

---

## Advanced Commands

### `watchtower`
**Show all commands**

Displays help menu with all available commands.

---

## Command Workflow Examples

### Typical Morning
```bash
watchtower brief
# Check Craft → Write card → Work
```

### Scattered Afternoon
```bash
watchtower capture
# Dump everything → System sorts it
```

### Deep Work Block
```bash
watchtower energy         # Check if ready
watchtower work "Epilogue redesign"
# 2-3 hour focused session
```

### End of Day
```bash
watchtower card           # Process completed card
watchtower status         # Quick check
```

---

## Tips

**Context management:**
- Use `/clear` in Claude Code between daily tasks
- Start fresh Claude session for deep work projects
- Kill and restart Claude Code every 2-3 days

**Card workflow:**
- Keep cards small (3-5 items max)
- Cross off completed items clearly
- Take photo in good lighting
- AirDrop from iPhone works great

**Energy awareness:**
- Log honestly - patterns emerge over weeks
- Low energy days still accomplish light work
- Don't force deep work when depleted

---

## Keyboard Shortcuts

**In Claude Code terminal:**
- `Ctrl+D` - Exit current input
- `Ctrl+C` - Cancel current operation
- `/clear` - Clear conversation context
- `Cmd+K` - Clear terminal screen

---

## Getting More Help

- [Setup Guide](SETUP.md) - Initial configuration
- [Customization Guide](CUSTOMIZATION.md) - Adapt to your workflow
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues
- [GitHub Issues](https://github.com/krispuckett/hybridsystem/issues) - Report bugs or ask questions
