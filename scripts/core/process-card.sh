#!/bin/bash

# ============================================================================
# PROCESS CARD
# OCR your end-of-day card and update all documents
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
    SPRINT_WARNING_DAY=14
    VOICE_DISCIPLINE="Marcus Aurelius"
    VOICE_WISDOM="Gandalf"
    VOICE_LEADERSHIP="Aragorn"
fi

if [ -z "$1" ]; then
    echo "Usage: watchtower card <path-to-card-photo>"
    echo ""
    echo "Example: watchtower card ~/Downloads/IMG_1234.jpeg"
    echo ""
    echo "Or drag the image file into the terminal after the command."
    exit 1
fi

CARD_IMAGE="$1"

if [ ! -f "$CARD_IMAGE" ]; then
    echo "Error: Image not found at $CARD_IMAGE"
    exit 1
fi

DATE=$(date '+%A, %B %d, %Y')
DATE_SHORT=$(date '+%m.%d.%Y')

echo "═══════════════════════════════════════════"
echo "  PROCESSING CARD"
echo "  $DATE"
echo "═══════════════════════════════════════════"
echo ""
echo "Reading card and analyzing patterns..."
echo ""

claude --attach "$CARD_IMAGE" << EOF
Process my end-of-day card and UPDATE all three Craft documents with PATTERN TRACKING:

**READ THE CARD** (attached image):
- Completed tasks (filled circles ● or checkmarks ✓)
- Incomplete tasks (empty circles ○ or unchecked boxes)
- Delegated items (if marked)
- Appointments or time-specific items

**CRITICAL - PATTERN TRACKING FOR INCOMPLETE TASKS**:

For EACH incomplete task:
1. Check $DOC_TASKS - does this task already exist there?
2. If yes, look for any existing "Rolled forward" notes on that task
3. Count how many times it has rolled
4. ADD A NEW NOTE to that task in $DOC_TASKS:
   "[$DATE_SHORT] Rolled forward (Xth time)" where X is the new count

This creates avoidance history INSIDE Craft for future pattern detection.

**UPDATE $DOC_TASKS**:
- Mark or remove completed tasks
- Keep incomplete tasks with the new roll count notes added
- Maintain categorization

**UPDATE $DOC_JOURNEY**:
- Increment Days Traveled by 1 (or equivalent counter)
- Add entry:
  "[$DATE_SHORT] - X tasks completed, Y rolled forward. [If any task hit 3+ rolls, note it: 'Task Z now at Xth roll']"

**ENERGY CHECK**:
After processing, ask me:
"How was your energy today? (high / medium / low / recovery)"

Wait for my response, then update $DOC_JOURNEY with:
- Today's energy level
- Current sprint day
- Brief pattern note if relevant

**COACHING INSIGHT** (deliver if patterns warrant):

If task rolled 3+ times (developing avoidance):
Voice of $VOICE_DISCIPLINE: "You have carried '[task name]' for X days without completing it or setting it down. This is not procrastination—it is information. The obstacle is not the work itself. What is the real resistance?"

If task rolled 5+ times (serious avoidance):
Voice of $VOICE_WISDOM: "'[Task name]' has followed you like a shadow for X days now. Perhaps the task itself is not the enemy—but the way you have framed it. What would happen if you started, even badly? Or is this a burden meant to be set down?"

If sprint > $SPRINT_WARNING_DAY days AND energy seems to be declining:
Voice of $VOICE_WISDOM: "Day X of your march, and I sense weariness. Even the Fellowship rested before Mordor. What would strategic recovery look like—not stopping entirely, but lighter duty?"

If good completion day:
Voice of $VOICE_LEADERSHIP: "The line held today. X tasks completed. This is how lasting campaigns are won—not in glory, but in steady advance. Well fought."

**SUMMARY**:
- X completed, Y rolled forward
- Current sprint day
- Any avoidance flags (name the specific tasks)
- Any burnout warnings based on sprint length + energy

Keep the pattern history IN THE CRAFT DOCS so it accumulates over time.
EOF

echo ""
echo "═══════════════════════════════════════════"
echo "Card processed. Documents updated."
echo "═══════════════════════════════════════════"
