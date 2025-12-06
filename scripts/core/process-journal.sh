#!/bin/bash

# ============================================================================
# PROCESS JOURNAL
# Extract insights from handwritten journal entries
# ============================================================================

# Load config
CONFIG_FILE="$HOME/.watchtower/config"
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
else
    # Defaults
    DOC_TASKS="The Forge"
    DOC_JOURNEY="The Long Road"
fi

DATE=$(date '+%A, %B %d, %Y')

echo "═══════════════════════════════════════════"
echo "  PROCESSING JOURNAL ENTRY"
echo "  $DATE"
echo "═══════════════════════════════════════════"
echo ""

if [ -z "$1" ]; then
    echo "This will open Claude Code in interactive mode."
    echo "When it opens:"
    echo ""
    echo "  1. DRAG your journal photo into the Claude window"
    echo "  2. PRESS ENTER"
    echo "  3. Claude will read and extract insights"
    echo ""
    echo "Or run: watchtower journal <path-to-image>"
    echo ""
    echo "Press any key to continue..."
    read -n 1 -s
    echo ""
    echo "Opening Claude Code..."
    echo ""

    # Interactive mode
    claude << 'EOF'
I need you to process my handwritten journal entry.

STEP 1: WAIT FOR IMAGE
I'm going to drag my journal photo into this window now.

STEP 2: READ THE JOURNAL
Carefully transcribe my cursive writing.
Preserve the tone and emotion - this is personal reflection.

STEP 3: EXTRACT INSIGHTS
Look for:
- Strategic thinking or decisions
- Energy observations or patterns
- Concerns, anxieties, or worries
- Ideas or inspirations
- Gratitude or positive moments
- Self-awareness about work patterns

STEP 4: IDENTIFY ACTIONABLE ITEMS
If I mentioned tasks or things to do, note them separately.

STEP 5: UPDATE THE JOURNEY DOCUMENT
Add to the reflections section:
- Date the entry
- Key insights in my own voice/tone
- Keep it authentic - don't sanitize my thoughts

STEP 6: UPDATE TASKS (if needed)
If there were clear actionable items, add them to the task pool
in appropriate energy sections.

STEP 7: OFFER PERSPECTIVE (optional)
If you notice patterns of:
- Burnout or exhaustion
- Strategic confusion
- Anxiety about capacity

Offer brief coaching (2-3 sentences max).
Be direct but supportive.

Now drag the journal image and press Enter...
EOF

else
    # Image provided as argument
    JOURNAL_IMAGE="$1"
    
    if [ ! -f "$JOURNAL_IMAGE" ]; then
        echo "Error: Image not found at $JOURNAL_IMAGE"
        exit 1
    fi
    
    claude --attach "$JOURNAL_IMAGE" << EOF
Process my handwritten journal entry (attached image):

1. **TRANSCRIBE**: Read my cursive writing carefully. Preserve tone and emotion.

2. **EXTRACT INSIGHTS**: Look for:
   - Strategic thinking or decisions
   - Energy observations
   - Concerns or anxieties
   - Ideas or inspirations
   - Self-awareness about patterns

3. **ACTIONABLE ITEMS**: If I mentioned tasks, note them separately.

4. **UPDATE $DOC_JOURNEY**: Add to reflections:
   - Date: $DATE
   - Key insights in my voice
   - Keep it authentic

5. **UPDATE $DOC_TASKS** (if needed): Add any clear actionable items.

6. **BRIEF PERSPECTIVE** (if warranted): 2-3 sentences of coaching if you notice burnout signals or strategic confusion.

Process now.
EOF
fi

echo ""
echo "✓ Journal processed"
echo "✓ Insights added to $DOC_JOURNEY"
echo ""
