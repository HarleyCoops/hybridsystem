#!/bin/bash

# ============================================================================
# ACCOUNTABILITY CHECK
# Deep pattern analysis with coaching voices
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
    CATEGORY_DEEP="Deep Work Forging"
    CATEGORY_STANDARD="Standard Forge Work"
    CATEGORY_LIGHT="Light Smithing"
    CATEGORY_SOMEDAY="The Anvil Awaits"
    SPRINT_WARNING_DAY=14
    SPRINT_DANGER_DAY=21
    VOICE_DISCIPLINE="Marcus Aurelius"
    VOICE_WISDOM="Gandalf"
    VOICE_LEADERSHIP="Aragorn"
fi

DATE=$(date '+%A, %B %d, %Y')

echo "═══════════════════════════════════════════"
echo "  ACCOUNTABILITY CHECK"
echo "  $DATE"
echo "═══════════════════════════════════════════"
echo ""
echo "Deep pattern analysis in progress..."
echo ""

claude << EOF
Run an accountability check with DEEP PATTERN ANALYSIS across all Craft documents:

**DEEP READ OF $DOC_JOURNEY**:
- Current sprint day (Days Traveled or equivalent)
- Read the last 14 entries
- Extract: completion counts, energy levels, tasks mentioned as rolled
- Calculate: Are completions trending up, down, or stable?
- Note: Any task names that appear repeatedly as "rolled"

**DEEP READ OF $DOC_TASKS**:
- Count tasks in each category ($CATEGORY_DEEP, $CATEGORY_STANDARD, $CATEGORY_LIGHT, $CATEGORY_SOMEDAY)
- Look for tasks with "Rolled forward" notes
- For each task with roll notes: count how many times rolled
- Identify the oldest/most-rolled tasks

**PATTERN DETECTION**:

1. AVOIDANCE ANALYSIS:
   - List EVERY task that has rolled forward 3+ times
   - Format: "[Task name] - rolled X times, category: [category]"
   - Hypothesis: Is there a pattern? (Same category? Same energy requirement? Same project?)
   
2. SPRINT HEALTH:
   - Days in current sprint
   - Completion rate trend over last 7 days
   - If declining: flag it
   
3. ENERGY TREND:
   - What energy levels appear in recent entries?
   - Pattern: improving, stable, or declining?
   - Correlation: Do high-energy entries show more completions?

4. CATEGORY ANALYSIS:
   - Which categories are completing vs. accumulating?
   - If one category is growing while others shrink: note it

**GENERATE ACCOUNTABILITY REPORT**:

## Accountability Report - $DATE

### The State of Your Campaign
Sprint Day: X | Recent completion trend: [up/stable/down]
[If sprint > $SPRINT_WARNING_DAY: "⚠️ Extended campaign - monitor energy"]
[If sprint > $SPRINT_DANGER_DAY: "🛑 Day X. Recovery is not optional at this point."]

### Forces Assessment
- $CATEGORY_DEEP: X tasks [flag if > 10]
- $CATEGORY_STANDARD: X tasks [flag if > 20]
- $CATEGORY_LIGHT: X tasks
- $CATEGORY_SOMEDAY: X tasks

### Avoidance Patterns
[List each task rolled 3+ times with specific count]
[If pattern detected: "You appear to be avoiding [category/type] work"]
[If no avoidance: "No chronic avoidance detected"]

### What the Patterns Say
[Specific observations based on the data]
[Be direct - name problems specifically]

### Words You Need to Hear

[SELECT ONE VOICE based on what's most needed:]

**If avoiding known hard work** (use $VOICE_DISCIPLINE):
"You know the task that must be done. '[Task name]' has waited X days. Each day you delay, it grows larger in your mind until the mere thought exhausts you more than the doing would. The obstacle IS the way. You were not made for comfort—you were made to create things that matter. Stop deliberating. Begin."

**If showing burnout signals** (use $VOICE_WISDOM):
"Day X, and still you march. I have seen this before—the eager mind that runs until it stumbles. Your completion rate has [declined/stalled]. This is not weakness; it is the body's wisdom. Rest is not retreat. What would lighter duty look like today? One worthy task, done well, is enough."

**If scattered across too many fronts** (use $VOICE_LEADERSHIP):
"You scatter your forces across too many fronts. [X] deep work tasks, [Y] standard tasks—no army can hold every position. What would a commander do? Choose ONE campaign. Take that ground. Then choose another. What is the ONE task that, if completed today, would be victory?"

**If doing well** (use $VOICE_LEADERSHIP):
"The line holds. You fight with discipline. [X] tasks this week, no chronic avoidance. This is how lasting campaigns are won—not in heroic charges, but in steady advance. The road goes ever on. Continue."

---

**UPDATE $DOC_DAILY** with this report so it becomes part of your historical record.
EOF

echo ""
echo "═══════════════════════════════════════════"
echo "Accountability check complete."
echo "═══════════════════════════════════════════"
