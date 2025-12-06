#!/bin/bash

# ============================================================================
# WEEKLY REVIEW
# Comprehensive weekly pattern analysis
# ============================================================================

# Load config
CONFIG_FILE="$HOME/.watchtower/config"
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
else
    # Defaults
    DOC_DAILY="The Watchtower"
    DOC_TASKS="The Forge"
    DOC_JOURNEY="The Long Road"
    VOICE_DISCIPLINE="Marcus Aurelius"
    VOICE_WISDOM="Gandalf"
    VOICE_LEADERSHIP="Aragorn"
fi

DATE=$(date '+%A, %B %d, %Y')
WEEK_END=$(date '+%m.%d.%Y')
WEEK_START=$(date -v-7d '+%m.%d.%Y' 2>/dev/null || date -d '7 days ago' '+%m.%d.%Y')

echo "═══════════════════════════════════════════"
echo "  WEEKLY INTELLIGENCE REVIEW"
echo "  $WEEK_START → $WEEK_END"
echo "═══════════════════════════════════════════"
echo ""
echo "Analyzing patterns from the past week..."
echo ""

claude << EOF
Generate a comprehensive WEEKLY INTELLIGENCE REVIEW from my Craft documents:

**ANALYZE $DOC_JOURNEY** (past 7 entries):
- Extract completion counts from each day
- Extract energy levels from each day
- Note sprint day at start and end of week
- List any tasks mentioned multiple times as "rolled"

**ANALYZE $DOC_TASKS**:
- What tasks were completed/removed this week?
- What tasks have been there all week without moving?
- What NEW tasks arrived this week?
- Count by category

**PATTERN SYNTHESIS**:

1. COMPLETION ANALYSIS:
   - Total tasks completed this week
   - Daily average
   - Best day (highest completions) and worst day
   - Deep work vs. standard vs. light breakdown

2. AVOIDANCE ANALYSIS:
   - Tasks that appeared 3+ times this week without completion
   - Tasks with the most "rolled forward" notes
   - Pattern hypothesis: What TYPE of work is being avoided?
   
3. ENERGY ANALYSIS:
   - Energy readings across the week
   - Average energy
   - Trend: improving, stable, declining?
   - Correlation: Did high-energy days = more completions?
   
4. SPRINT ANALYSIS:
   - Started week at Day X, ended at Day Y
   - Sustainable pace or showing strain?
   - Recovery periods taken or needed?

**GENERATE WEEKLY REPORT** and write to $DOC_DAILY:

## Weekly Review - $WEEK_START to $WEEK_END

### By the Numbers
- Tasks Completed: X
- Daily Average: X
- Sprint Progress: Day X → Day Y
- Energy Trend: [improving/stable/declining]
- Best Day: [day] with X completions

### What Worked
[Specific patterns that correlated with success]

### What Didn't
[Specific struggles - name stuck tasks]

### Avoidance Patterns
[List chronically avoided tasks if any]
[Hypothesis on why]

### Strategic Question for Next Week
[One meaningful question based on the patterns]

### Voice of [Select based on what's most needed]

**If productive week** ($VOICE_LEADERSHIP):
"The campaign advances. X tasks this week, steady energy. This is the work of a commander who understands that lasting victory comes from discipline, not heroics. The road continues."

**If struggling week** ($VOICE_WISDOM):
"A harder week. [X] tasks, declining energy by day [Y]. But remember: even Frodo had the Dead Marshes. The question is not whether you struggled—it's whether you kept moving. You did. That matters."

**If avoidance-heavy week** ($VOICE_DISCIPLINE):
"[X] tasks completed, but [Y] rolled repeatedly. You know which ones. What story are you telling yourself about these tasks? Is it true? 'The impediment to action advances action. What stands in the way becomes the way.'"

---

This becomes part of your historical record in $DOC_DAILY.
EOF

echo ""
echo "═══════════════════════════════════════════"
echo "Weekly review complete. Check $DOC_DAILY."
echo "═══════════════════════════════════════════"
