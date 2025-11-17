#!/bin/bash

# Watchtower Card Processor - Interactive Version
# Opens Claude Code and waits for you to drag your card image

DATE=$(date '+%A, %B %d, %Y')

echo "═══════════════════════════════════════════"
echo "  PROCESSING ANALOGUE CARD"
echo "  $DATE"  
echo "═══════════════════════════════════════════"
echo ""
echo "This will open Claude Code in interactive mode."
echo "When it opens:"
echo ""
echo "  1. DRAG your card photo into the Claude window"
echo "  2. PRESS ENTER"
echo "  3. Claude will read and process it automatically"
echo ""
echo "Press any key to continue..."
read -n 1 -s

echo ""
echo "Opening Claude Code..."
echo ""

# Create a temporary prompt file
cat > /tmp/watchtower-card-prompt.txt << 'PROMPT'
I need you to carefully read my handwritten Analogue card.

STEP 1: WAIT FOR IMAGE
I'm going to drag my card photo into this window now.

STEP 2: READ THE CARD
Once you see the image, transcribe:
- Date at top
- Each task line  
- Completion markers (●/✓ = DONE | ○ = INCOMPLETE)

STEP 3: FORMAT YOUR TRANSCRIPTION
```
Date: [date from card]

COMPLETED:
- [task 1]
- [task 2]

INCOMPLETE:  
- [task 3]
- [task 4]
```

STEP 4: UPDATE THE FORGE (mcp__the-forge)
- Mark completed tasks: change [ ] to [x]
- Keep incomplete tasks as [ ]
- Add any new tasks to appropriate energy sections

STEP 5: UPDATE THE WATCHTOWER (mcp__watchtower)
Add to today's Field Reports section:
- Brief summary of what got done
- What's rolling to tomorrow

STEP 6: UPDATE THE LONG ROAD (mcp__the-long-road)
- Increment sprint day counter
- If sprint day > 5, warn about burnout

STEP 7: SUMMARY
Show me what you updated in each document.

Now drag the card image and press Enter...
PROMPT

# Launch Claude Code with the prompt
claude < /tmp/watchtower-card-prompt.txt

echo ""
echo "═══════════════════════════════════════════"
echo ""
echo "Now let's log your energy level..."
echo ""
echo "How was today's energy?"
echo "  1) High - felt great, got deep work done"
echo "  2) Medium - normal productive day"  
echo "  3) Low - struggled, but pushed through"
echo "  4) Recovery - intentional rest day"
echo ""
read -p "Enter 1-4: " ENERGY

case $ENERGY in
    1) ENERGY_LEVEL="High" ;;
    2) ENERGY_LEVEL="Medium" ;;
    3) ENERGY_LEVEL="Low" ;;
    4) ENERGY_LEVEL="Recovery" ;;
    *) ENERGY_LEVEL="Medium" ;;
esac

echo ""
echo "Updating energy log..."

claude << EOF
Update The Long Road (mcp__the-long-road) with today's energy:

Date: $DATE
Energy: $ENERGY_LEVEL

Add this to the energy tracking section.
If this was a Recovery day, reset the sprint counter to 0.
Otherwise, the sprint day should already be incremented from the card processing.

Just confirm when done - no long explanation needed.
EOF

echo ""
echo "✓ Card processed"
echo "✓ Tasks updated in The Forge"
echo "✓ Energy logged: $ENERGY_LEVEL"
echo "✓ Sprint tracking updated"
echo ""
echo "Tomorrow morning, run: watchtower brief"
echo ""
