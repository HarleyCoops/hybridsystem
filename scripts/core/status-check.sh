#!/bin/bash

# ============================================================================
# STATUS CHECK
# Quick overview of current system state
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
fi

echo "═══════════════════════════════════════════"
echo "  STATUS CHECK"
echo "  $(date '+%A, %B %d, %Y - %I:%M %p')"
echo "═══════════════════════════════════════════"
echo ""

# Get status via Claude Code
claude << EOF
Give me a quick status report by reading:

1. $DOC_JOURNEY
   - Current sprint day
   - Recent energy pattern
   - Any burnout warnings

2. $DOC_TASKS
   - Count of tasks in each energy category
   - Any overdue or high-priority items

3. $DOC_DAILY
   - Today's priorities
   - Anything in Field Reports

Format it concise and scannable:

## Current Sprint
Day X | Energy trend: [pattern]

## Task Pool
- $CATEGORY_DEEP: X tasks
- $CATEGORY_STANDARD: X tasks
- $CATEGORY_LIGHT: X tasks
- $CATEGORY_SOMEDAY: X tasks

## Today
[Top 3 priorities or "Not set - run watchtower brief"]

## Alerts
[Any burnout warnings, avoidance patterns, or important notes]

Keep it SHORT - this is a quick check, not a full report.
EOF

echo ""
