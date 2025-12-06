#!/bin/bash

# ============================================================================
# DEEP WORK SESSION
# Focused work session with tracking
# ============================================================================

# Load config
CONFIG_FILE="$HOME/.watchtower/config"
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
else
    # Defaults
    DOC_TASKS="The Forge"
    DOC_JOURNEY="The Long Road"
    SESSIONS_DIR="$HOME/.watchtower/sessions"
fi

if [ -z "$1" ]; then
    echo "Usage: watchtower work \"project name\""
    echo ""
    echo "Examples:"
    echo "  watchtower work \"Website redesign\""
    echo "  watchtower work \"API integration\""
    echo "  watchtower work \"Interview prep\""
    exit 1
fi

PROJECT="$1"
DATE=$(date '+%A, %B %d, %Y')
SESSION_FILE="$SESSIONS_DIR/$(date '+%Y%m%d')-$(echo $PROJECT | tr ' ' '-' | tr '[:upper:]' '[:lower:]').md"

# Create sessions directory if needed
mkdir -p "$SESSIONS_DIR"

echo "═══════════════════════════════════════════"
echo "  DEEP WORK SESSION"
echo "  $PROJECT"
echo "  $DATE"
echo "═══════════════════════════════════════════"
echo ""

# Check current energy and sprint status
echo "Checking your current state..."
claude << EOF
Quick check - read $DOC_JOURNEY and tell me:
1. Current sprint day
2. Recent energy pattern
3. Any burnout warnings

Keep it to 2-3 lines max.
EOF

echo ""
echo "Starting deep work session..."
echo "Session notes: $SESSION_FILE"
echo ""

# Initialize session notes
cat > "$SESSION_FILE" << NOTES
# Deep Work Session: $PROJECT
Date: $DATE

## Session Goals
[Define 2-3 specific goals]

## Work Log
[Track what you accomplish]

## Insights & Decisions
[Key learnings and strategic choices]

## Next Actions
[What to tackle next session]

---
NOTES

# Launch focused Claude Code session
claude << EOF
I'm starting a deep work session on: $PROJECT

SETUP:
1. First, read $DOC_TASKS and find tasks related to "$PROJECT"
2. Help me define 2-3 specific goals for THIS session (next 1-3 hours)
3. Create a battle plan - what order should we tackle things?

DURING THE SESSION:
- I'll work alongside you
- Track what we accomplish
- If I get stuck or scattered, pull me back to the goals
- If I want to pivot to something else, challenge me: "Is this session goal still $PROJECT or are we pivoting?"

FOCUS MODE RULES:
- No context switching unless I explicitly say "pivot"
- If I mention other tasks, capture them for later but don't derail
- Keep me on track with gentle reminders

ENERGY AWARENESS:
- If I seem frustrated or stuck for >15 minutes, suggest a 5-min break
- Watch for signs I'm forcing it when energy is low
- It's okay to stop early if energy crashes

AT END OF SESSION:
- Summarize what we accomplished
- Update $DOC_JOURNEY with session insights
- Update task progress in $DOC_TASKS
- Suggest next session goals

Ready? Let's define the session goals for: $PROJECT
EOF

echo ""
echo "═══════════════════════════════════════════"
echo "  SESSION COMPLETE"
echo "═══════════════════════════════════════════"
echo ""
echo "Session notes: $SESSION_FILE"
echo ""
echo "Take a break before the next session."
echo ""
