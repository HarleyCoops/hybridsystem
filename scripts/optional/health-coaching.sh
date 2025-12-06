#!/bin/bash

# ============================================================================
# HEALTH COACHING
# Evidence-based health Q&A (no personal medical advice)
# ============================================================================

# Load config
CONFIG_FILE="$HOME/.watchtower/config"
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
else
    HEALTH_LOG="$HOME/.watchtower/health-log.md"
    DOC_JOURNEY="The Long Road"
fi

echo "═══════════════════════════════════════════"
echo "  HEALTH COACHING"
echo "  Evidence-Based Guidance"
echo "═══════════════════════════════════════════"
echo ""

# Check if health log exists
if [ -f "$HEALTH_LOG" ]; then
    HEALTH_CONTEXT=$(tail -100 "$HEALTH_LOG" 2>/dev/null)
    HAS_HEALTH_DATA=true
else
    HAS_HEALTH_DATA=false
fi

echo "Ask any health-related question. I'll provide evidence-based guidance."
echo "Type 'quit' to exit."
echo ""
echo "Examples:"
echo "  - Should I work out today given my recovery scores?"
echo "  - What does low HRV mean for my work capacity?"
echo "  - How can I improve my sleep quality?"
echo "  - What supplements might help with energy?"
echo ""

while true; do
    echo -n "Question: "
    read QUESTION
    
    if [ "$QUESTION" = "quit" ] || [ "$QUESTION" = "exit" ] || [ "$QUESTION" = "q" ]; then
        echo "Goodbye."
        exit 0
    fi
    
    if [ -z "$QUESTION" ]; then
        continue
    fi
    
    echo ""
    
    if [ "$HAS_HEALTH_DATA" = true ]; then
        claude << EOF
You are a health-focused assistant providing evidence-based guidance.

**RECENT HEALTH DATA** (from local log):
$HEALTH_CONTEXT

**QUESTION**:
"$QUESTION"

**RESPONSE GUIDELINES**:

1. **Ground in evidence**: Cite research when relevant. Use web search if needed to verify claims or find current research.

2. **Be specific**: Give concrete, actionable guidance rather than vague advice.
   - Not: "Get better sleep"
   - Instead: "Aim for 7-9 hours, keep bedroom at 65-68°F, avoid screens 1hr before bed"

3. **Consider the data**: If the health log shows relevant metrics, reference them.
   - "Your HRV of X suggests..."
   - "Given your sleep score of Y..."

4. **Know your limits**: 
   - Don't diagnose medical conditions
   - Don't recommend specific medications or dosages
   - For serious concerns, recommend consulting a healthcare provider
   - Say "I don't know" if uncertain

5. **Connect to productivity** (when relevant):
   - How does this affect work capacity?
   - What adjustments might help today?

**FORMAT**:

[Direct answer to the question - 2-4 paragraphs]

**Specific Actions:**
1. [Concrete step]
2. [Concrete step]
3. [Concrete step]

**Evidence:**
- [Source or research citation if applicable]

[If this warrants professional consultation, note that clearly]
EOF
    else
        claude << EOF
You are a health-focused assistant providing evidence-based guidance.

**NOTE**: No health data has been logged yet. Providing general guidance.

**QUESTION**:
"$QUESTION"

**RESPONSE GUIDELINES**:

1. **Ground in evidence**: Cite research when relevant. Use web search if needed.

2. **Be specific**: Give concrete, actionable guidance.

3. **Know your limits**: 
   - Don't diagnose conditions
   - Don't recommend specific medications
   - For serious concerns, recommend consulting a healthcare provider

4. **Connect to productivity** (when relevant):
   - How does this affect work capacity?

**FORMAT**:

[Direct answer - 2-4 paragraphs]

**Specific Actions:**
1. [Concrete step]
2. [Concrete step]
3. [Concrete step]

**Evidence:**
- [Source if applicable]

**Tip**: Run 'watchtower health <file>' with your biometric data for more personalized guidance.
EOF
    fi
    
    echo ""
    echo "───────────────────────────────────────────"
    echo ""
done
