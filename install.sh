#!/bin/bash

# ============================================================================
# HYBRID SYSTEM INSTALLER
# A productivity system bridging pen-and-paper with AI intelligence
# ============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  HYBRID SYSTEM INSTALLER${NC}"
echo -e "${BLUE}  Pen-and-Paper + AI Intelligence${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# ----------------------------------------------------------------------------
# CHECK REQUIREMENTS
# ----------------------------------------------------------------------------

echo -e "${YELLOW}Checking requirements...${NC}"
echo ""

# Check for Claude Code
if command -v claude &> /dev/null; then
    echo -e "  ${GREEN}✓${NC} Claude Code found"
else
    echo -e "  ${RED}✗${NC} Claude Code not found"
    echo ""
    echo "  Claude Code is required. Install from:"
    echo "  https://docs.anthropic.com/en/docs/claude-code"
    echo ""
    exit 1
fi

# Check for Craft MCP (optional but recommended)
if claude mcp list 2>/dev/null | grep -qi "craft"; then
    echo -e "  ${GREEN}✓${NC} Craft MCP configured"
    CRAFT_MCP_AVAILABLE=true
else
    echo -e "  ${YELLOW}!${NC} Craft MCP not detected"
    echo "    (Optional but recommended - see docs/SETUP.md)"
    CRAFT_MCP_AVAILABLE=false
fi

echo ""

# ----------------------------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------------------------

echo -e "${YELLOW}Configuration${NC}"
echo ""
echo "You can customize or use defaults. Press Enter to accept [defaults]."
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load defaults
source "$SCRIPT_DIR/config/defaults.conf"

# Ask about customization
read -p "Do you want to customize settings? (y/N): " CUSTOMIZE
echo ""

if [[ "$CUSTOMIZE" =~ ^[Yy]$ ]]; then
    # Energy windows
    echo "Peak Energy Windows (24-hour format)"
    echo "These are when the system routes you to deep work."
    echo ""
    
    read -p "  Peak Window 1 Start [$PEAK_WINDOW_1_START]: " input
    PEAK_WINDOW_1_START="${input:-$PEAK_WINDOW_1_START}"
    
    read -p "  Peak Window 1 End [$PEAK_WINDOW_1_END]: " input
    PEAK_WINDOW_1_END="${input:-$PEAK_WINDOW_1_END}"
    
    read -p "  Peak Window 2 Start [$PEAK_WINDOW_2_START]: " input
    PEAK_WINDOW_2_START="${input:-$PEAK_WINDOW_2_START}"
    
    read -p "  Peak Window 2 End [$PEAK_WINDOW_2_END]: " input
    PEAK_WINDOW_2_END="${input:-$PEAK_WINDOW_2_END}"
    
    read -p "  Peak Window 3 Start [$PEAK_WINDOW_3_START]: " input
    PEAK_WINDOW_3_START="${input:-$PEAK_WINDOW_3_START}"
    
    read -p "  Peak Window 3 End [$PEAK_WINDOW_3_END]: " input
    PEAK_WINDOW_3_END="${input:-$PEAK_WINDOW_3_END}"
    
    echo ""
    
    # Sprint thresholds
    echo "Sprint Thresholds (consecutive work days)"
    read -p "  Warning day [$SPRINT_WARNING_DAY]: " input
    SPRINT_WARNING_DAY="${input:-$SPRINT_WARNING_DAY}"
    
    read -p "  Danger day [$SPRINT_DANGER_DAY]: " input
    SPRINT_DANGER_DAY="${input:-$SPRINT_DANGER_DAY}"
    
    echo ""
    
    # Timezone
    read -p "Timezone [$TIMEZONE]: " input
    TIMEZONE="${input:-$TIMEZONE}"
    
    echo ""
    
    # Health module
    read -p "Enable health tracking module? (y/N): " input
    if [[ "$input" =~ ^[Yy]$ ]]; then
        HEALTH_MODULE_ENABLED=true
    fi
    
    echo ""
fi

# ----------------------------------------------------------------------------
# CREATE DIRECTORIES
# ----------------------------------------------------------------------------

echo -e "${YELLOW}Setting up directories...${NC}"

# Config and data directory
mkdir -p "$HOME/.watchtower/sessions"
echo -e "  ${GREEN}✓${NC} Created ~/.watchtower/"

# Scripts directory
INSTALL_DIR="/usr/local/bin/watchtower-scripts"
sudo mkdir -p "$INSTALL_DIR"
echo -e "  ${GREEN}✓${NC} Created $INSTALL_DIR/"

# ----------------------------------------------------------------------------
# WRITE CONFIG FILE
# ----------------------------------------------------------------------------

echo -e "${YELLOW}Writing configuration...${NC}"

cat > "$HOME/.watchtower/config" << EOF
# Hybrid System Configuration
# Generated: $(date)

# Energy Windows
PEAK_WINDOW_1_START=$PEAK_WINDOW_1_START
PEAK_WINDOW_1_END=$PEAK_WINDOW_1_END
PEAK_WINDOW_2_START=$PEAK_WINDOW_2_START
PEAK_WINDOW_2_END=$PEAK_WINDOW_2_END
PEAK_WINDOW_3_START=$PEAK_WINDOW_3_START
PEAK_WINDOW_3_END=$PEAK_WINDOW_3_END

# Sprint Thresholds
SPRINT_WARNING_DAY=$SPRINT_WARNING_DAY
SPRINT_DANGER_DAY=$SPRINT_DANGER_DAY

# Coaching Voices
VOICE_DISCIPLINE="$VOICE_DISCIPLINE"
VOICE_WISDOM="$VOICE_WISDOM"
VOICE_LEADERSHIP="$VOICE_LEADERSHIP"

# Document Names
DOC_DAILY="$DOC_DAILY"
DOC_TASKS="$DOC_TASKS"
DOC_JOURNEY="$DOC_JOURNEY"

# Categories
CATEGORY_DEEP="$CATEGORY_DEEP"
CATEGORY_STANDARD="$CATEGORY_STANDARD"
CATEGORY_LIGHT="$CATEGORY_LIGHT"
CATEGORY_SOMEDAY="$CATEGORY_SOMEDAY"

# Modules
HEALTH_MODULE_ENABLED=$HEALTH_MODULE_ENABLED
WEEKLY_REVIEW_ENABLED=$WEEKLY_REVIEW_ENABLED
DEEP_WORK_SESSIONS_ENABLED=$DEEP_WORK_SESSIONS_ENABLED

# System
TIMEZONE="$TIMEZONE"
DATA_DIR="$HOME/.watchtower"
SESSIONS_DIR="$HOME/.watchtower/sessions"
HEALTH_LOG="$HOME/.watchtower/health-log.md"
EOF

echo -e "  ${GREEN}✓${NC} Configuration saved to ~/.watchtower/config"

# ----------------------------------------------------------------------------
# INSTALL SCRIPTS
# ----------------------------------------------------------------------------

echo -e "${YELLOW}Installing scripts...${NC}"

# Copy core scripts
sudo cp "$SCRIPT_DIR/scripts/core/"*.sh "$INSTALL_DIR/"
sudo chmod +x "$INSTALL_DIR/"*.sh
echo -e "  ${GREEN}✓${NC} Core scripts installed"

# Copy optional scripts if modules enabled
if [ "$HEALTH_MODULE_ENABLED" = true ]; then
    sudo cp "$SCRIPT_DIR/scripts/optional/health-"*.sh "$INSTALL_DIR/"
    sudo chmod +x "$INSTALL_DIR/health-"*.sh
    echo -e "  ${GREEN}✓${NC} Health module installed"
fi

if [ -f "$SCRIPT_DIR/scripts/optional/weekly-review.sh" ]; then
    sudo cp "$SCRIPT_DIR/scripts/optional/weekly-review.sh" "$INSTALL_DIR/"
    sudo chmod +x "$INSTALL_DIR/weekly-review.sh"
    echo -e "  ${GREEN}✓${NC} Weekly review installed"
fi

if [ -f "$SCRIPT_DIR/scripts/optional/deep-work.sh" ]; then
    sudo cp "$SCRIPT_DIR/scripts/optional/deep-work.sh" "$INSTALL_DIR/"
    sudo chmod +x "$INSTALL_DIR/deep-work.sh"
    echo -e "  ${GREEN}✓${NC} Deep work sessions installed"
fi

# ----------------------------------------------------------------------------
# CREATE MAIN COMMAND
# ----------------------------------------------------------------------------

echo -e "${YELLOW}Creating main command...${NC}"

# Remove if exists as directory (common upgrade issue)
if [ -d "/usr/local/bin/watchtower" ]; then
    sudo rm -rf /usr/local/bin/watchtower
fi

# Create the main watchtower command
sudo tee /usr/local/bin/watchtower > /dev/null << 'MAINSCRIPT'
#!/bin/bash

# Hybrid System Main Command
# https://github.com/krispuckett/hybridsystem

SCRIPTS_DIR="/usr/local/bin/watchtower-scripts"
CONFIG_FILE="$HOME/.watchtower/config"

# Load config if exists
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
fi

# Show help if no arguments
show_help() {
    echo ""
    echo "Hybrid System - Pen-and-Paper + AI Intelligence"
    echo ""
    echo "DAILY WORKFLOW:"
    echo "  watchtower brief              Morning briefing with priorities"
    echo "  watchtower card <image>       Process end-of-day card photo"
    echo "  watchtower energy             Check/log current energy level"
    echo ""
    echo "TASK MANAGEMENT:"
    echo "  watchtower add \"task\" [level] Add task (level: high/normal/low/someday)"
    echo "  watchtower status             Quick system overview"
    echo ""
    echo "ACCOUNTABILITY:"
    echo "  watchtower accountability     Deep pattern analysis + coaching"
    echo "  watchtower weekly             Weekly intelligence review"
    echo ""
    echo "FOCUS:"
    echo "  watchtower work \"project\"     Start deep work session"
    echo "  watchtower journal            Process journal entry"
    echo ""
    if [ "$HEALTH_MODULE_ENABLED" = true ]; then
    echo "HEALTH (optional module):"
    echo "  watchtower health <file>      Process biometric data"
    echo "  watchtower coach              Evidence-based health Q&A"
    echo ""
    fi
    echo "Run 'watchtower help <command>' for detailed help on any command."
    echo ""
}

case "$1" in
    # Daily workflow
    brief|morning)
        "$SCRIPTS_DIR/morning-briefing.sh"
        ;;
    card)
        shift
        "$SCRIPTS_DIR/process-card.sh" "$@"
        ;;
    energy|check)
        "$SCRIPTS_DIR/energy-check.sh"
        ;;
    
    # Task management
    add|task)
        shift
        "$SCRIPTS_DIR/brain-dump.sh" "$@"
        ;;
    status)
        "$SCRIPTS_DIR/status-check.sh"
        ;;
    
    # Accountability
    accountability|account)
        "$SCRIPTS_DIR/accountability-check.sh"
        ;;
    weekly|week)
        if [ -f "$SCRIPTS_DIR/weekly-review.sh" ]; then
            "$SCRIPTS_DIR/weekly-review.sh"
        else
            echo "Weekly review not installed. Run installer with weekly review enabled."
        fi
        ;;
    
    # Focus
    work|deep|session)
        shift
        if [ -f "$SCRIPTS_DIR/deep-work.sh" ]; then
            "$SCRIPTS_DIR/deep-work.sh" "$@"
        else
            echo "Deep work sessions not installed. Run installer with deep work enabled."
        fi
        ;;
    journal)
        shift
        "$SCRIPTS_DIR/process-journal.sh" "$@"
        ;;
    
    # Health (optional)
    health|biometrics)
        shift
        if [ -f "$SCRIPTS_DIR/health-check.sh" ]; then
            "$SCRIPTS_DIR/health-check.sh" "$@"
        else
            echo "Health module not installed. Run installer with health module enabled."
        fi
        ;;
    coach|ask)
        if [ -f "$SCRIPTS_DIR/health-coaching.sh" ]; then
            "$SCRIPTS_DIR/health-coaching.sh"
        else
            echo "Health module not installed. Run installer with health module enabled."
        fi
        ;;
    
    # Help
    help|--help|-h|"")
        show_help
        ;;
    
    *)
        echo "Unknown command: $1"
        echo "Run 'watchtower help' for available commands."
        exit 1
        ;;
esac
MAINSCRIPT

sudo chmod +x /usr/local/bin/watchtower
echo -e "  ${GREEN}✓${NC} Main command installed"

# ----------------------------------------------------------------------------
# SET TIMEZONE
# ----------------------------------------------------------------------------

if ! grep -q "TZ=" "$HOME/.zshrc" 2>/dev/null && ! grep -q "TZ=" "$HOME/.bashrc" 2>/dev/null; then
    echo "export TZ=\"$TIMEZONE\"" >> "$HOME/.zshrc" 2>/dev/null || true
    echo "export TZ=\"$TIMEZONE\"" >> "$HOME/.bashrc" 2>/dev/null || true
    echo -e "  ${GREEN}✓${NC} Timezone set to $TIMEZONE"
fi

# ----------------------------------------------------------------------------
# COMPLETE
# ----------------------------------------------------------------------------

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  INSTALLATION COMPLETE${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Next steps:"
echo ""
echo "  1. Set up your three Craft documents (see docs/SETUP.md)"
echo "     - $DOC_DAILY (daily hub)"
echo "     - $DOC_TASKS (task pool)"
echo "     - $DOC_JOURNEY (journey tracking)"
echo ""
echo "  2. Configure Craft MCP in Claude Code (see docs/SETUP.md)"
echo ""
echo "  3. Test the installation:"
echo "     $ watchtower"
echo ""
echo "  4. Run your first morning briefing:"
echo "     $ watchtower brief"
echo ""
echo "Configuration: ~/.watchtower/config"
echo "Edit anytime to change settings."
echo ""
