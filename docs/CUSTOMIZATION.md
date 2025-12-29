# Customization Guide

The Hybrid System is designed to adapt to your workflow. Configuration is stored in JSON format at `%APPDATA%\.watchtower\config.json`.

---

## Configuration File

View your current configuration:

```powershell
watchtower config --show
```

Find the config file location:

```powershell
watchtower config --path
```

You can edit the JSON file directly, or use CLI commands for common changes.

---

## Energy Windows

Define when you're at peak energy. The system uses these to route you toward appropriate work.

Edit the `energy_windows` section in your config:

```json
{
  "energy_windows": {
    "peak_1_start": 9,
    "peak_1_end": 13,
    "peak_2_start": 15,
    "peak_2_end": 18,
    "peak_3_start": 0,
    "peak_3_end": 0
  }
}
```

**Tips:**
- Use 24-hour format
- Set unused windows to `0` to disable them
- Track your actual energy for a week before customizing

---

## Sprint Thresholds

How many consecutive work days before the system warns you about potential burnout.

```json
{
  "sprint": {
    "warning_day": 14,
    "danger_day": 21
  }
}
```

**Adjust based on your patterns:**
- If you crash around day 10, set warning to 7-8
- If you can sustain 3 weeks easily, extend the thresholds
- The system tracks actual energy, so it may warn earlier if energy is declining

---

## Coaching Voices

The system uses three archetypal voices for different situations. Change these to figures that resonate with you.

```json
{
  "voices": {
    "discipline": {
      "name": "Marcus Aurelius",
      "style": "Stoic clarity, focused on what's in your control"
    },
    "wisdom": {
      "name": "Gandalf",
      "style": "Patient, long-view thinking, permission to rest"
    },
    "leadership": {
      "name": "Aragorn",
      "style": "Steady commander energy, sustainable campaigns"
    }
  }
}
```

**Alternative ideas:**
- Discipline: Seneca, Jocko Willink, David Goggins, your strict mentor
- Wisdom: Yoda, Mr. Rogers, your grandmother, a favorite teacher
- Leadership: Captain Picard, Ted Lasso, a leader you admire

---

## Task Categories

The names for energy-based task buckets:

```json
{
  "categories": {
    "deep": "Deep Work Forging",
    "standard": "Standard Forge Work",
    "light": "Light Smithing",
    "someday": "The Anvil Awaits"
  }
}
```

**Alternative naming:**
```json
{
  "categories": {
    "deep": "Focus Required",
    "standard": "Routine",
    "light": "Quick Wins",
    "someday": "Ideas"
  }
}
```

---

## Optional Modules

Enable or disable features via CLI:

```powershell
# Health tracking
watchtower config --enable-health
watchtower config --disable-health

# Weekly review
watchtower config --enable-weekly
watchtower config --disable-weekly

# Deep work sessions
watchtower config --enable-deepwork
watchtower config --disable-deepwork
```

Or edit the config directly:

```json
{
  "modules": {
    "health": false,
    "weekly_review": true,
    "deep_work_sessions": true
  }
}
```

---

## Timezone

Set your timezone:

```powershell
watchtower config --set-timezone "America/New_York"
```

Common timezone strings:
- `America/New_York`
- `America/Los_Angeles`
- `America/Chicago`
- `America/Denver`
- `Europe/London`
- `Europe/Paris`
- `Asia/Tokyo`

---

## Resetting to Defaults

To start fresh, delete the config file:

```powershell
del %APPDATA%\.watchtower\config.json
```

The next command will regenerate defaults.

---

## Backing Up Your Config

Your config contains no sensitive data by default. Back it up:

```powershell
# Backup
copy %APPDATA%\.watchtower\config.json %USERPROFILE%\Documents\watchtower-config.json

# Restore
copy %USERPROFILE%\Documents\watchtower-config.json %APPDATA%\.watchtower\config.json
```

---

## Example Configurations

### Minimalist

```json
{
  "energy_windows": {
    "peak_1_start": 9,
    "peak_1_end": 12,
    "peak_2_start": 0,
    "peak_2_end": 0
  },
  "sprint": {
    "warning_day": 7,
    "danger_day": 14
  },
  "modules": {
    "health": false,
    "weekly_review": false,
    "deep_work_sessions": false
  }
}
```

### Night Owl

```json
{
  "energy_windows": {
    "peak_1_start": 14,
    "peak_1_end": 18,
    "peak_2_start": 21,
    "peak_2_end": 1
  },
  "system": {
    "timezone": "America/Los_Angeles"
  }
}
```

### High Performer with Health Tracking

```json
{
  "energy_windows": {
    "peak_1_start": 5,
    "peak_1_end": 9,
    "peak_2_start": 15,
    "peak_2_end": 17
  },
  "sprint": {
    "warning_day": 21,
    "danger_day": 30
  },
  "modules": {
    "health": true,
    "weekly_review": true,
    "deep_work_sessions": true
  }
}
```
