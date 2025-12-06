# Customization Guide

The Hybrid System is designed to adapt to your workflow. All configuration lives in `~/.watchtower/config`.

---

## Configuration File

After installation, your config is at `~/.watchtower/config`. Edit it anytime:

```bash
nano ~/.watchtower/config
# or
code ~/.watchtower/config
```

Changes take effect on the next command run.

---

## Energy Windows

Define when you're at peak energy. The system uses these to route you toward appropriate work.

```bash
# Peak Window 1 (e.g., morning focus time)
PEAK_WINDOW_1_START=9
PEAK_WINDOW_1_END=13

# Peak Window 2 (e.g., afternoon second wind)
PEAK_WINDOW_2_START=15
PEAK_WINDOW_2_END=18

# Peak Window 3 (e.g., evening creative time)
PEAK_WINDOW_3_START=20
PEAK_WINDOW_3_END=22
```

**Tips:**
- Use 24-hour format
- You can have 1, 2, or 3 windows
- Set unused windows to `0` to disable them
- Track your actual energy for a week before customizing

---

## Sprint Thresholds

How many consecutive work days before the system warns you about potential burnout.

```bash
# Gentle reminder to check in
SPRINT_WARNING_DAY=14

# Strong suggestion to take recovery
SPRINT_DANGER_DAY=21
```

**Adjust based on your patterns:**
- If you crash around day 10, set warning to 7-8
- If you can sustain 3 weeks easily, extend the thresholds
- The system tracks actual energy, so it may warn earlier if energy is declining

---

## Coaching Voices

The system uses three archetypal voices for different situations. Change these to figures that resonate with you.

```bash
# Used when avoiding known hard work - brings discipline
VOICE_DISCIPLINE="Marcus Aurelius"
VOICE_DISCIPLINE_STYLE="Stoic clarity, focused on what's in your control"

# Used when burned out or uncertain - brings wisdom
VOICE_WISDOM="Gandalf"
VOICE_WISDOM_STYLE="Patient, long-view thinking, permission to rest"

# Used when scattered or need to lead yourself - brings resolve
VOICE_LEADERSHIP="Aragorn"
VOICE_LEADERSHIP_STYLE="Steady commander energy, sustainable campaigns"
```

**Alternative ideas:**
- Discipline: Seneca, Jocko Willink, David Goggins, your strict mentor
- Wisdom: Yoda, Mr. Rogers, your grandmother, a favorite teacher
- Leadership: Captain Picard, Ted Lasso, a leader you admire

The system will adapt its coaching style to match.

---

## Document Names

If you prefer different names for your Craft documents:

```bash
DOC_DAILY="The Watchtower"
DOC_TASKS="The Forge"
DOC_JOURNEY="The Long Road"
```

**Examples:**
```bash
# Minimalist
DOC_DAILY="Today"
DOC_TASKS="Tasks"
DOC_JOURNEY="Journal"

# Corporate
DOC_DAILY="Daily Brief"
DOC_TASKS="Backlog"
DOC_JOURNEY="Work Log"

# Gaming
DOC_DAILY="Quest Log"
DOC_TASKS="Inventory"
DOC_JOURNEY="Adventure Log"
```

---

## Task Categories

The names for energy-based task buckets:

```bash
CATEGORY_DEEP="Deep Work Forging"
CATEGORY_STANDARD="Standard Forge Work"
CATEGORY_LIGHT="Light Smithing"
CATEGORY_SOMEDAY="The Anvil Awaits"
```

**Alternative naming:**
```bash
# GTD-style
CATEGORY_DEEP="High Energy"
CATEGORY_STANDARD="Normal Energy"
CATEGORY_LIGHT="Low Energy"
CATEGORY_SOMEDAY="Someday/Maybe"

# Context-based
CATEGORY_DEEP="Focus Required"
CATEGORY_STANDARD="Routine"
CATEGORY_LIGHT="Quick Wins"
CATEGORY_SOMEDAY="Ideas"
```

---

## Optional Modules

Enable or disable features:

```bash
# Health tracking (biometrics, bloodwork, etc.)
HEALTH_MODULE_ENABLED=false

# Weekly review generation
WEEKLY_REVIEW_ENABLED=true

# Deep work session tracking
DEEP_WORK_SESSIONS_ENABLED=true
```

---

## Timezone

Important for accurate time-based features:

```bash
TIMEZONE="America/Denver"
```

Find your timezone string:
```bash
# List available timezones
ls /usr/share/zoneinfo/America/
ls /usr/share/zoneinfo/Europe/
```

---

## Data Directories

Where local data is stored:

```bash
DATA_DIR="$HOME/.watchtower"
SESSIONS_DIR="$HOME/.watchtower/sessions"
HEALTH_LOG="$HOME/.watchtower/health-log.md"
```

Usually no need to change these unless you want data in a specific location (e.g., synced folder).

---

## Advanced: Custom Prompts

The scripts use prompts that reference your config variables. To customize the actual prompts:

1. Copy the script you want to modify:
   ```bash
   cp /usr/local/bin/watchtower-scripts/morning-briefing.sh ~/my-morning-briefing.sh
   ```

2. Edit the prompt text in your copy

3. Either:
   - Replace the original: `sudo cp ~/my-morning-briefing.sh /usr/local/bin/watchtower-scripts/`
   - Or create an alias in your shell config

**Note:** Your customizations may be overwritten if you reinstall. Keep backups.

---

## Resetting to Defaults

To start fresh:

```bash
# Remove current config
rm ~/.watchtower/config

# Reinstall
cd hybridsystem
./install.sh
```

Or copy the defaults:
```bash
cp hybridsystem/config/defaults.conf ~/.watchtower/config
```

---

## Sharing Your Config

Your config contains no sensitive data by default. Feel free to share it or version control it:

```bash
# Backup your config
cp ~/.watchtower/config ~/dotfiles/watchtower-config

# Restore on new machine
cp ~/dotfiles/watchtower-config ~/.watchtower/config
```

---

## Examples: Complete Configs

### Minimalist

```bash
PEAK_WINDOW_1_START=9
PEAK_WINDOW_1_END=12
PEAK_WINDOW_2_START=0
PEAK_WINDOW_2_END=0
PEAK_WINDOW_3_START=0
PEAK_WINDOW_3_END=0

SPRINT_WARNING_DAY=7
SPRINT_DANGER_DAY=14

VOICE_DISCIPLINE="Your Best Self"
VOICE_WISDOM="Your Mentor"
VOICE_LEADERSHIP="Your Role Model"

DOC_DAILY="Today"
DOC_TASKS="Tasks"
DOC_JOURNEY="Log"

CATEGORY_DEEP="Hard"
CATEGORY_STANDARD="Medium"
CATEGORY_LIGHT="Easy"
CATEGORY_SOMEDAY="Later"

HEALTH_MODULE_ENABLED=false
```

### Night Owl

```bash
PEAK_WINDOW_1_START=14
PEAK_WINDOW_1_END=18
PEAK_WINDOW_2_START=21
PEAK_WINDOW_2_END=25  # 1am

SPRINT_WARNING_DAY=10
SPRINT_DANGER_DAY=18

TIMEZONE="America/Los_Angeles"
```

### High Performer with Health Tracking

```bash
PEAK_WINDOW_1_START=5
PEAK_WINDOW_1_END=9
PEAK_WINDOW_2_START=15
PEAK_WINDOW_2_END=17

SPRINT_WARNING_DAY=21
SPRINT_DANGER_DAY=30

HEALTH_MODULE_ENABLED=true
WEEKLY_REVIEW_ENABLED=true
DEEP_WORK_SESSIONS_ENABLED=true
```
