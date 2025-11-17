#!/bin/bash

# Watchtower Journal Processor - Interactive Version
# Opens Claude Code and waits for you to drag your journal photo

DATE=$(date '+%A, %B %d, %Y')

echo "═══════════════════════════════════════════"
echo "  PROCESSING JOURNAL ENTRY"
echo "  $DATE"
echo "═══════════════════════════════════════════"
echo ""
echo "This will open Claude Code in interactive mode."
echo "When it opens:"
echo ""
echo "  1. DRAG your journal photo into the Claude window"
echo "  2. PRESS ENTER"
echo "  3. Claude will read and extract insights"
echo ""
echo "Press any key to continue..."
read -n 1 -s

echo ""
echo "Opening Claude Code..."
echo ""

# Create temporary prompt
cat > /tmp/watchtower-journal-prompt.txt << 'PROMPT'
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

STEP 5: UPDATE THE LONG ROAD (mcp__the-long-road)
Add to the "Waystones Passed" or reflections section:
- Date the entry
- Key insights in my own voice/tone
- Keep it authentic - don't sanitize my thoughts

STEP 6: UPDATE THE FORGE (if needed)
If there were clear actionable items, add them to The Forge
in appropriate energy sections.

STEP 7: OFFER PERSPECTIVE (optional)
If you notice patterns of:
- Burnout or exhaustion
- Strategic confusion
- Anxiety about capacity

Offer brief Stoic-influenced coaching (2-3 sentences max).
Be direct but supportive.

Now drag the journal image and press Enter...
PROMPT

# Launch Claude Code
claude < /tmp/watchtower-journal-prompt.txt

echo ""
echo "✓ Journal processed"
echo "✓ Insights added to The Long Road"
echo "✓ Your reflections are preserved"
echo ""
