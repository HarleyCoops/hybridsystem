#!/bin/bash

# ============================================================================
# BRAIN DUMP
# Quick task capture with energy-based routing
# ============================================================================

# Load config
CONFIG_FILE="$HOME/.watchtower/config"
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
else
    # Defaults
    DOC_TASKS="The Forge"
    CATEGORY_DEEP="Deep Work Forging"
    CATEGORY_STANDARD="Standard Forge Work"
    CATEGORY_LIGHT="Light Smithing"
    CATEGORY_SOMEDAY="The Anvil Awaits"
fi

if [ -z "$1" ]; then
    echo "Usage: watchtower add \"your task\" [energy-level]"
    echo ""
    echo "Energy levels:"
    echo "  high    → $CATEGORY_DEEP (complex, creative, demanding)"
    echo "  normal  → $CATEGORY_STANDARD (productive, routine)"
    echo "  low     → $CATEGORY_LIGHT (admin, organizing, easy wins)"
    echo "  someday → $CATEGORY_SOMEDAY (ideas for later)"
    echo ""
    echo "Examples:"
    echo "  watchtower add \"Write project proposal\" high"
    echo "  watchtower add \"Reply to emails\" low"
    echo "  watchtower add \"Learn Rust\" someday"
    exit 1
fi

TASK="$1"
ENERGY="${2:-normal}"  # Default to normal energy

# Map energy level to category
case $ENERGY in
    high|deep)
        SECTION="$CATEGORY_DEEP"
        ;;
    normal|standard|medium)
        SECTION="$CATEGORY_STANDARD"
        ;;
    low|light)
        SECTION="$CATEGORY_LIGHT"
        ;;
    someday|later|maybe)
        SECTION="$CATEGORY_SOMEDAY"
        ;;
    *)
        SECTION="$CATEGORY_STANDARD"
        ;;
esac

echo "Adding task to $SECTION..."

# Add task via Claude Code
claude << EOF
Add this task to $DOC_TASKS in the "$SECTION" section:
- [ ] $TASK

Use the Craft MCP to append it to the correct section.
Format as a Craft task (checkbox syntax) so it appears in the Tasks sidebar.

Just confirm when done - no extra explanation needed.
EOF

echo "✓ Task added to $DOC_TASKS → $SECTION"
