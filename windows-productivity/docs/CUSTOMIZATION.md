# Watchtower Windows - Customization Guide

Personalize your productivity system for your unique workflow.

## Document Names

The three core documents can be renamed to match your preferences:

```json
{
  "documents": {
    "daily": "Daily Command Center",
    "tasks": "Task Backlog",
    "journey": "Progress Journal"
  }
}
```

## Task Categories

Rename categories to match your mental model:

```json
{
  "categories": {
    "deep": "Focus Blocks",
    "standard": "Regular Work",
    "light": "Quick Wins",
    "someday": "Backburner"
  }
}
```

## Energy Windows

Configure up to 3 peak productivity windows:

```json
{
  "energyWindows": [
    {
      "start": 6,
      "end": 9,
      "label": "Early Morning Writing"
    },
    {
      "start": 10,
      "end": 13,
      "label": "Late Morning Meetings"
    },
    {
      "start": 14,
      "end": 17,
      "label": "Afternoon Execution"
    }
  ]
}
```

The system uses these to suggest appropriate tasks based on current time.

## Sprint Thresholds

Adjust burnout detection sensitivity:

```json
{
  "sprint": {
    "warningDay": 10,    // Earlier warning for sensitive users
    "dangerDay": 14      // Stricter limit
  }
}
```

Or for high-endurance periods:

```json
{
  "sprint": {
    "warningDay": 21,    // Later warning
    "dangerDay": 30      // Extended limit
  }
}
```

## Coaching Voices

The system uses three archetypal voices for different situations:

```json
{
  "voices": {
    "discipline": "Marcus Aurelius",  // For avoidance patterns
    "wisdom": "Gandalf",              // For burnout signals
    "leadership": "Aragorn"           // For scattered priorities
  }
}
```

### Alternative Voice Options

Choose voices that resonate with you:

**For Discipline (addressing avoidance):**
- Marcus Aurelius (Stoic emperor)
- Jocko Willink (Modern discipline)
- Seneca (Stoic philosopher)
- David Goggins (Extreme ownership)

**For Wisdom (burnout prevention):**
- Gandalf (Patient guide)
- Yoda (Ancient master)
- Mr. Rogers (Gentle compassion)
- Dumbledore (Wise mentor)

**For Leadership (strategic focus):**
- Aragorn (Reluctant king)
- Captain Picard (Calm authority)
- Admiral Adama (Crisis leader)
- Coach Taylor (Inspirational)

Example with different voices:

```json
{
  "voices": {
    "discipline": "Jocko Willink",
    "wisdom": "Mr. Rogers",
    "leadership": "Captain Picard"
  }
}
```

## Custom Prompts (Advanced)

You can extend the system prompts by creating custom command files.

### Create a Custom Command

Create `.claude/commands/custom-brief.md`:

```markdown
Generate a morning briefing with extra focus on:
- Yesterday's wins (celebrate completions)
- One key insight from pattern analysis
- Weather and calendar context for today

Include a motivational quote aligned with current challenges.
```

Run with: `claude /custom-brief`

## Notification Sounds

Enable/disable sounds (Windows only):

```typescript
import { playSound } from 'watchtower-windows';

// On task completion
await playSound('success');

// On avoidance pattern detected
await playSound('warning');
```

## Theme Integration

The system can detect Windows theme:

```typescript
import { getWindowsTheme } from 'watchtower-windows';

const theme = await getWindowsTheme();
// Returns 'light' or 'dark'
```

## Data Export

Export your data for backup or analysis:

```powershell
# Copy data directory
Copy-Item -Recurse "$env:APPDATA\watchtower" "D:\Backup\watchtower-backup"
```

### JSON Data Structure

**tasks.json**:
```json
{
  "tasks": [
    {
      "id": "123-abc",
      "content": "Write quarterly report",
      "priority": "deep",
      "createdAt": "2024-01-15T09:00:00Z",
      "rollForwardCount": 2,
      "notes": ["Rolled forward on 2024-01-16"]
    }
  ]
}
```

**daily.json**:
```json
{
  "entries": {
    "2024-01-15": {
      "date": "2024-01-15",
      "sprintDay": 5,
      "energyReadings": [
        {"timestamp": "...", "level": "high", "context": "Morning coffee"}
      ],
      "tasksCompleted": ["123-abc"],
      "tasksRolledForward": ["456-def"],
      "fieldReports": ["[09:15] Completed standup meeting"]
    }
  }
}
```

## Integration Examples

### With Obsidian

Export daily entries to Obsidian vault:

```typescript
import { getTodayEntry } from 'watchtower-windows';
import { writeFileSync } from 'fs';

const entry = getTodayEntry();
const markdown = `
# Daily Log - ${entry.date}

## Sprint Day ${entry.sprintDay}

### Completed
${entry.tasksCompleted.map(t => `- [x] ${t}`).join('\n')}

### Field Reports
${entry.fieldReports.join('\n')}

### Energy
${entry.energyReadings.map(r => `- ${r.timestamp}: ${r.level}`).join('\n')}
`;

writeFileSync(`C:/Obsidian/DailyNotes/${entry.date}.md`, markdown);
```

### With Todoist/Notion

The task data can be exported and synced:

```typescript
import { loadTasks } from 'watchtower-windows';

const tasks = loadTasks();
const activeTasks = tasks.filter(t => !t.completedAt);

// Transform to your target format
const todoistFormat = activeTasks.map(t => ({
  content: t.content,
  priority: t.priority === 'deep' ? 1 : 4,
  labels: [t.priority]
}));
```

## Keyboard Shortcuts (PowerShell Profile)

Add to your PowerShell profile (`$PROFILE`):

```powershell
# Quick aliases
Set-Alias wt watchtower
Set-Alias wtb 'watchtower brief'
Set-Alias wts 'watchtower status'

# Quick energy logging
function wte { watchtower energy $args }

# Quick task add
function wta { watchtower add $args }
```

## Multiple Profiles

For different work contexts (work vs. personal):

```powershell
# Set profile via environment
$env:WATCHTOWER_PROFILE = "work"
watchtower brief

$env:WATCHTOWER_PROFILE = "personal"
watchtower brief
```

Implement in config by checking the environment variable.

## Debugging

Enable verbose output:

```powershell
$env:WATCHTOWER_DEBUG = "true"
watchtower brief
```

View raw API responses:

```powershell
$env:WATCHTOWER_DEBUG = "verbose"
watchtower card photo.jpg
```
