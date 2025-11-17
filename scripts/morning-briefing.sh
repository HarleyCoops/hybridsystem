#!/bin/bash

# Watchtower Morning Briefing
# Reads your Craft docs and generates today's priorities

DATE=$(date '+%A, %B %d, %Y')

echo "═══════════════════════════════════════════"
echo "  WATCHTOWER MORNING BRIEFING"
echo "  $DATE"
echo "═══════════════════════════════════════════"
echo ""
echo "Analyzing your documents..."
echo ""

# Generate briefing via Claude Code
claude << 'EOF'
I need you to generate my morning briefing by reading all three Craft documents:

1. Read mcp__the-forge to see all available tasks
2. Read mcp__the-long-road to check current sprint day and energy patterns
3. Read mcp__watchtower to see yesterday's field reports

Then create today's briefing in The Watchtower:

**UPDATE THE WATCHTOWER DOCUMENT** with:

## Today - [Current Date]

### Current Power Level
[Based on sprint day and recent energy patterns from Long Road]

### Today's Mission Briefing
[Top 3-5 priorities from The Forge, weighted by:
- Energy level match (high energy tasks if power is good)
- Urgency/importance
- What makes sense for today]

### Transfer to Analogue Card
→ [The specific items to write on the physical card - clear, actionable]

### Field Reports
[Empty - ready for today's captures]

---

Use markdown_add or blocks_update on mcp__watchtower to write this.
Keep it concise and actionable.
Focus on what actually matters TODAY.
EOF

echo ""
echo "✓ Briefing generated in The Watchtower"
echo "✓ Open Craft to see your priorities"
echo "✓ Write top items on your Analogue card"
echo ""
