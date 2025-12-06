#!/bin/bash

# ============================================================================
# HEALTH CHECK
# Process biometric data from any source (tool-agnostic)
# ============================================================================

# Load config
CONFIG_FILE="$HOME/.watchtower/config"
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
else
    HEALTH_LOG="$HOME/.watchtower/health-log.md"
    DOC_JOURNEY="The Long Road"
fi

DATE=$(date '+%A, %B %d, %Y')
DATE_SHORT=$(date '+%Y-%m-%d')

echo "═══════════════════════════════════════════"
echo "  HEALTH CHECK"
echo "  $DATE"
echo "═══════════════════════════════════════════"
echo ""

if [ -z "$1" ]; then
    echo "Usage: watchtower health <file>"
    echo ""
    echo "Accepts any biometric data:"
    echo "  - Screenshots from wearables (Oura, Whoop, Apple Watch, etc.)"
    echo "  - Blood work PDFs"
    echo "  - CSV exports from health apps"
    echo "  - Photos of test results"
    echo ""
    echo "Examples:"
    echo "  watchtower health ~/Downloads/oura-screenshot.png"
    echo "  watchtower health ~/Downloads/bloodwork.pdf"
    echo "  watchtower health ~/Downloads/sleep-data.csv"
    echo ""
    echo "Data is stored locally in: $HEALTH_LOG"
    echo "(Not synced to Craft by default for privacy)"
    exit 1
fi

HEALTH_FILE="$1"

if [ ! -f "$HEALTH_FILE" ]; then
    echo "Error: File not found at $HEALTH_FILE"
    exit 1
fi

# Determine file type
FILE_EXT="${HEALTH_FILE##*.}"
FILE_EXT_LOWER=$(echo "$FILE_EXT" | tr '[:upper:]' '[:lower:]')

echo "Processing: $HEALTH_FILE"
echo "File type: $FILE_EXT_LOWER"
echo ""

# Create health log if it doesn't exist
if [ ! -f "$HEALTH_LOG" ]; then
    cat > "$HEALTH_LOG" << 'HEADER'
# Health Log

Private health tracking data. Not synced to external documents.

---

HEADER
fi

case $FILE_EXT_LOWER in
    png|jpg|jpeg|heic|webp)
        # Image file - use vision
        claude --attach "$HEALTH_FILE" << EOF
Process this health/biometric data (attached image):

**EXTRACT ALL METRICS**:
Read every number, score, and metric visible. Common things to look for:
- Sleep metrics (duration, quality, stages, efficiency)
- HRV (heart rate variability)
- Resting heart rate
- Recovery scores
- Readiness scores
- Activity metrics
- Blood markers (if lab results)
- Any other health indicators

**FORMAT THE DATA**:

## Health Data - $DATE_SHORT

### Source
[Identify the app/device if visible, otherwise "Unknown source"]

### Metrics
[List each metric with its value]
- Metric Name: Value (unit if shown)
- Metric Name: Value (unit if shown)
...

### Notable Observations
[Any values that seem particularly high, low, or noteworthy]
[Trends if multiple days shown]

### Relevance to Work Capacity
[Brief note on what this might mean for energy/productivity today]
- If HRV is low or recovery poor: "Consider lighter work today"
- If metrics look good: "Conditions support demanding work"

**IMPORTANT**: 
- Just extract and organize the data
- Don't make medical diagnoses
- Don't give specific treatment recommendations
- Note if anything seems worth discussing with a healthcare provider

After extracting, I'll append this to the local health log.
EOF
        ;;
    
    pdf)
        # PDF file
        claude --attach "$HEALTH_FILE" << EOF
Process this health document (attached PDF):

**EXTRACT ALL DATA**:
This is likely blood work, lab results, or a health report. Extract:
- All test names and values
- Reference ranges if shown
- Any flags (high/low/abnormal)
- Date of tests
- Provider/lab name if visible

**FORMAT THE DATA**:

## Health Data - $DATE_SHORT

### Source
[Lab name, provider, or document title]

### Results
| Test | Value | Reference Range | Flag |
|------|-------|-----------------|------|
| ... | ... | ... | ... |

### Out of Range Values
[List any values flagged as high or low]

### Summary
[Brief overview of overall results]

### Follow-up Notes
[Anything that might warrant discussion with a healthcare provider]

**IMPORTANT**: 
- Just extract and organize the data objectively
- Don't make diagnoses or treatment recommendations
- Note uncertainty if values are hard to read

After extracting, I'll append this to the local health log.
EOF
        ;;
    
    csv|txt)
        # CSV or text data
        claude << EOF
Process this health data file: $HEALTH_FILE

Read the contents and extract health metrics. Format as:

## Health Data - $DATE_SHORT

### Source
[File name and apparent source]

### Metrics
[Organized list of all health data found]

### Trends
[If multiple data points, note any trends]

### Relevance to Work Capacity
[Brief note on implications for energy/productivity]
EOF
        ;;
    
    *)
        echo "Unsupported file type: $FILE_EXT_LOWER"
        echo "Supported: png, jpg, jpeg, heic, webp, pdf, csv, txt"
        exit 1
        ;;
esac

# Append to health log
echo "" >> "$HEALTH_LOG"
echo "---" >> "$HEALTH_LOG"
echo "" >> "$HEALTH_LOG"

echo ""
echo "═══════════════════════════════════════════"
echo "Health data processed."
echo "Log: $HEALTH_LOG"
echo ""
echo "To sync summary to your journey document, run:"
echo "  watchtower coach"
echo "═══════════════════════════════════════════"
