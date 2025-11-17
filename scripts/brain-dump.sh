#!/bin/bash

# Watchtower Brain Dump - Adds tasks directly to Craft via MCP
# Usage: ./brain-dump.sh "your task here" [energy-level]
# Energy levels: high, normal, low, someday

if [ -z "$1" ]; then
    echo "Usage: ./brain-dump.sh \"your task\" [high|normal|low|someday]"
    exit 1
fi

TASK="$1"
ENERGY="${2:-normal}"  # Default to normal energy

# Map energy level to Forge section
case $ENERGY in
    high)
        SECTION="Deep Work Forging"
        ;;
    normal)
        SECTION="Standard Forge Work"
        ;;
    low)
        SECTION="Light Smithing"
        ;;
    someday)
        SECTION="The Anvil Awaits"
        ;;
    *)
        SECTION="Standard Forge Work"
        ;;
esac

echo "Adding task to $SECTION..."

# Add task to The Forge via Claude Code
claude << EOF
Add this task to The Forge document in the "$SECTION" section:
- [ ] $TASK

Use the mcp__the-forge server's markdown_add tool to append it to the correct section.
Make sure it's formatted as a Craft task (checkbox syntax) so it appears in the Tasks sidebar.

Just confirm when done - no extra explanation needed.
EOF

echo "✓ Task added to The Forge → $SECTION"
echo "✓ Will appear in Craft Tasks sidebar"
