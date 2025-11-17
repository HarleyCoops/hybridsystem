#!/bin/bash

# Watchtower Status Check
# Quick overview of where you are

echo "═══════════════════════════════════════════"
echo "  WATCHTOWER STATUS"
echo "  $(date '+%A, %B %d, %Y - %I:%M %p')"
echo "═══════════════════════════════════════════"
echo ""

# Get status via Claude Code
claude << 'EOF'
Give me a quick status report by reading:

1. mcp__the-long-road
   - Current sprint day
   - Recent energy pattern
   - Any burnout warnings

2. mcp__the-forge  
   - Count of tasks in each energy category
   - Any overdue or high-priority items

3. mcp__watchtower
   - Today's priorities
   - Anything in Field Reports

Format it concise and scannable:

## Current Sprint
Day X of Y | Energy: [pattern]

## Task Pool (The Forge)
- Deep Work: X tasks
- Standard: X tasks  
- Light: X tasks
- Someday: X tasks

## Today (Watchtower)
[Top 3 priorities or "Not set - run morning-briefing.sh"]

## Alerts
[Any burnout warnings or important notes]

Keep it SHORT - this is a quick check, not a full report.
EOF

echo ""
