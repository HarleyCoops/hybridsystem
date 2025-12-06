#!/bin/bash

# ============================================================================
# ENERGY CHECK
# Track and log current energy level with sprint context
# ============================================================================

# Load config
CONFIG_FILE="$HOME/.watchtower/config"
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
else
    # Defaults
    PEAK_WINDOW_1_START=9
    PEAK_WINDOW_1_END=13
    PEAK_WINDOW_2_START=15
    PEAK_WINDOW_2_END=18
    PEAK_WINDOW_3_START=20
    PEAK_WINDOW_3_END=22
    SPRINT_WARNING_DAY=14
    SPRINT_DANGER_DAY=21
    DOC_JOURNEY="The Long Road"
    VOICE_WISDOM="Gandalf"
fi

TIME=$(date '+%I:%M %p')
DATE=$(date '+%A, %B %d, %Y')
HOUR=$(date '+%H')

echo "═══════════════════════════════════════════"
echo "  ENERGY CHECK"
echo "  $TIME - $DATE"
echo "═══════════════════════════════════════════"
echo ""

# Determine time context
if [ $HOUR -ge $PEAK_WINDOW_1_START ] && [ $HOUR -lt $PEAK_WINDOW_1_END ]; then
    WINDOW="PEAK WINDOW ($PEAK_WINDOW_1_START:00-$PEAK_WINDOW_1_END:00)"
elif [ $HOUR -ge $PEAK_WINDOW_2_START ] && [ $HOUR -lt $PEAK_WINDOW_2_END ]; then
    WINDOW="PEAK WINDOW ($PEAK_WINDOW_2_START:00-$PEAK_WINDOW_2_END:00)"
elif [ $HOUR -ge $PEAK_WINDOW_3_START ] && [ $HOUR -lt $PEAK_WINDOW_3_END ]; then
    WINDOW="PEAK WINDOW ($PEAK_WINDOW_3_START:00-$PEAK_WINDOW_3_END:00)"
else
    WINDOW="Outside peak windows"
fi

echo "Current time context: $WINDOW"
echo ""

claude << EOF
Quick energy check with sprint and pattern context:

**READ $DOC_JOURNEY**:
- Current sprint day (Days Traveled or equivalent)
- Last 5 energy readings from recent entries
- Trend: Is energy improving, stable, or declining over recent days?

**QUICK ASSESSMENT**:

Sprint Day: X
Recent energy pattern: [extract from last 5 entries - high/medium/low readings]
Energy trend: [improving / stable / declining]

[If sprint day > $SPRINT_WARNING_DAY AND energy declining]:
"⚠️ Day X with declining energy trend. This is data, not weakness. Consider your recovery strategy."

[If sprint day > $SPRINT_DANGER_DAY]:
"🛑 Day X. Extended sprint with [energy pattern]. Recovery is strategy, not surrender."

[If in peak window + recent energy good]:
"Peak conditions aligned. Good window for deep work if energy supports it."

[If outside peak window OR recent energy low]:
"Consider routing to lighter work or strategic recovery."

**ASK**:
"Current energy level?"
"  1) 🔥 High - Sharp, focused, ready for deep work"
"  2) ⚡ Medium - Productive, can handle standard tasks"  
"  3) 🔋 Low - Tired, light tasks only"
"  4) 💤 Depleted - Should not be working"
"  5) 🌿 Recovery - Intentional rest period"

After I respond, update $DOC_JOURNEY with:
- Energy level and name
- Current sprint day
- Time of check
- Brief pattern note if relevant (e.g., "3rd low energy day this week")
EOF

echo ""
