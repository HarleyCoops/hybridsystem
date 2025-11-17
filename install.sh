#!/bin/bash

# Watchtower System Installer v5 - Craft MCP Edition
# Installs the Watchtower productivity system with Craft integration

set -e

echo "═══════════════════════════════════════════"
echo "  WATCHTOWER SYSTEM v5 INSTALLER"
echo "  Craft MCP Edition"
echo "═══════════════════════════════════════════"
echo ""

# Check if Claude Code is installed
if ! command -v claude &> /dev/null; then
    echo "❌ Error: Claude Code is not installed"
    echo ""
    echo "Install it first with:"
    echo "  npm install -g @anthropic-ai/claude-code"
    echo ""
    exit 1
fi

echo "✓ Claude Code found"
echo ""

# Check if Craft MCP servers are configured
echo "Checking Craft MCP connections..."
if ! claude mcp list | grep -q "watchtower\|the-forge\|the-long-road"; then
    echo "⚠️  Warning: Craft MCP servers not found"
    echo ""
    echo "Make sure you've added your three Craft documents:"
    echo "  claude mcp add --scope user --transport http watchtower https://mcp.craft.do/links/YOUR_LINK/mcp"
    echo "  claude mcp add --scope user --transport http the-forge https://mcp.craft.do/links/YOUR_LINK/mcp"
    echo "  claude mcp add --scope user --transport http the-long-road https://mcp.craft.do/links/YOUR_LINK/mcp"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✓ Craft MCP servers configured"
fi

echo ""

# Create installation directory
INSTALL_DIR="/usr/local/bin/watchtower"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing to $INSTALL_DIR..."

# Copy scripts
sudo mkdir -p "$INSTALL_DIR"
sudo cp "$SCRIPT_DIR"/*.sh "$INSTALL_DIR/"
sudo chmod +x "$INSTALL_DIR"/*.sh

# Create main watchtower command
cat << 'WATCHTOWER_CMD' | sudo tee /usr/local/bin/watchtower > /dev/null
#!/bin/bash
# Watchtower main command

WATCHTOWER_DIR="/usr/local/bin/watchtower"

case "$1" in
    brief|morning)
        "$WATCHTOWER_DIR/morning-briefing.sh"
        ;;
    card)
        "$WATCHTOWER_DIR/process-card.sh"
        ;;
    journal)
        "$WATCHTOWER_DIR/process-journal.sh"
        ;;
    add|task)
        shift
        "$WATCHTOWER_DIR/brain-dump.sh" "$@"
        ;;
    capture|dump)
        "$WATCHTOWER_DIR/brain-dump-capture.sh"
        ;;
    work|deep|session)
        shift
        "$WATCHTOWER_DIR/deep-work.sh" "$@"
        ;;
    energy|check)
        "$WATCHTOWER_DIR/energy-check.sh"
        ;;
    status)
        "$WATCHTOWER_DIR/status-check.sh"
        ;;
    context|cleanup)
        "$WATCHTOWER_DIR/context-cleanup.sh"
        ;;
    accountability|check-in)
        "$WATCHTOWER_DIR/accountability-check.sh"
        ;;
    schedule)
        "$WATCHTOWER_DIR/schedule-accountability.sh"
        ;;
    webhook)
        "$WATCHTOWER_DIR/setup-webhook.sh"
        ;;
    *)
        echo "Watchtower System v5 - Craft MCP Edition"
        echo ""
        echo "Daily Workflow:"
        echo "  watchtower brief              Generate morning briefing"
        echo "  watchtower card               Process end-of-day card (drag image)"
        echo "  watchtower journal            Process journal entry (drag image)"
        echo ""
        echo "Quick Captures:"
        echo "  watchtower add \"task\" [energy]  Add single task"
        echo "  watchtower capture            Brain dump mode (scattered thoughts)"
        echo ""
        echo "Deep Work:"
        echo "  watchtower work \"project\"      Start focused work session"
        echo "  watchtower energy             Check energy & get recommendations"
        echo ""
        echo "System Management:"
        echo "  watchtower status             Overview of system state"
        echo "  watchtower context            Manage Claude Code context"
        echo ""
        echo "Accountability:"
        echo "  watchtower accountability     Run accountability check NOW"
        echo "  watchtower schedule           Set up daily automated checks"
        echo "  watchtower webhook            Configure Slack/Discord alerts"
        echo ""
        echo "Energy levels: high, normal, low, someday"
        echo ""
        ;;
esac
WATCHTOWER_CMD

sudo chmod +x /usr/local/bin/watchtower

echo ""
echo "═══════════════════════════════════════════"
echo "  ✓ INSTALLATION COMPLETE"
echo "═══════════════════════════════════════════"
echo ""
echo "Commands available:"
echo "  watchtower brief       - Morning briefing"
echo "  watchtower card        - Process card photo"
echo "  watchtower journal     - Process journal"
echo "  watchtower add \"task\"  - Quick task capture"
echo "  watchtower status      - System overview"
echo ""
echo "Next steps:"
echo "  1. Make sure your three Craft docs are set up"
echo "  2. Run: watchtower brief"
echo "  3. Write priorities on your Analogue card"
echo "  4. Work from the card all day"
echo "  5. Photo your card, run: watchtower card photo.jpg"
echo ""
echo "The system is ready! 🏰"
echo ""
