#!/bin/bash

# ============================================================================
# MORNING BRIEFING
# Generates daily priorities with pattern analysis
# ============================================================================

# Load config
CONFIG_FILE="$HOME/.watchtower/config"
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
else
    # Defaults if no config
    DOC_DAILY="The Watchtower"
    DOC_TASKS="The Forge"
    DOC_JOURNEY="The Long Road"
    SPRINT_WARNING_DAY=14
    SPRINT_DANGER_DAY=21
    VOICE_DISCIPLINE="Marcus Aurelius"
    VOICE_WISDOM="Gandalf"
    VOICE_LEADERSHIP="Aragorn"
fi

DATE=$(date '+%A, %B %d, %Y')
DATE_SHORT=$(date '+%m.%d.%Y')

echo "═══════════════════════════════════════════"
echo "  MORNING BRIEFING"
echo "  $DATE"
echo "═══════════════════════════════════════════"
echo ""
echo "Analyzing patterns across your documents..."
echo ""

claude << EOF
Generate my morning briefing by reading ALL THREE Craft documents with PATTERN ANALYSIS:

**$DOC_JOURNEY** - Read recent entries (last 7):
- Current sprint day (Days Traveled or equivalent counter)
- Energy levels mentioned in recent entries
- Completion patterns (tasks done vs. rolled)
- Look for any task names that appear multiple times as "rolled"

**$DOC_TASKS** - Look for AVOIDANCE PATTERNS:
- Tasks that have been sitting there for days
- Any task with "rolled forward" notes - count how many times
- If a task has rolled 3+ times: FLAG IT SPECIFICALLY BY NAME

**$DOC_DAILY** - Recent Field Reports:
- What types of work have been completing?
- What keeps sliding to the next day?

**PATTERN ANALYSIS**:

1. AVOIDANCE DETECTION:
   - Identify any task rolled 3+ times
   - Name it specifically: "'[Task name]' has rolled X times"
   - Ask what's blocking it

2. SPRINT HEALTH:
   - If past day $SPRINT_WARNING_DAY: Note it
   - If past day $SPRINT_DANGER_DAY: Warning about energy management
   - Check if recent completion rates are declining

3. ENERGY TREND:
   - What energy levels appear in recent entries?
   - Is there a pattern (declining, stable, recovering)?

**GENERATE BRIEFING** and UPDATE $DOC_DAILY with:

## Today - $DATE_SHORT

### Sprint Status
Day X of current sprint. [Add warning if past day $SPRINT_WARNING_DAY or if patterns show strain]

### Pattern Alert
[If you found tasks rolling repeatedly, name them specifically]
[Example: "'Metal shader implementation' has appeared 4 times without completion. What's the real resistance here?"]
[If no concerning patterns: "No avoidance patterns detected. Systems nominal."]

### Current Power Level
[Based on recent energy readings and sprint day - assess readiness]

### Today's Mission
[Top 3-5 priorities based on energy routing]
[Weight toward tasks that have been avoided if energy supports it]

### Transfer to Card
→ [Specific items for the physical card - clear, actionable]

### Field Reports
[Empty - ready for today's captures]

---

VOICE: Direct and strategic, like $VOICE_LEADERSHIP planning the day's march.
If you see concerning patterns, say so clearly. Don't soften warnings.
If a task keeps rolling, challenge me on it.

After updating $DOC_DAILY, show me the briefing.
EOF

echo ""
echo "✓ Briefing generated in $DOC_DAILY"
echo "✓ Check Craft to see your priorities"
echo ""
