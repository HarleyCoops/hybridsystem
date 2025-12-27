# Watchtower Windows - Setup Guide

Complete setup instructions for the Windows productivity system.

## Prerequisites

### Required

1. **Node.js 20+**
   - Download from https://nodejs.org/
   - Verify: `node --version`

2. **Claude Code CLI**
   - Install: `npm install -g @anthropic-ai/claude-code`
   - Configure: `claude login`
   - Verify: `claude --version`

3. **Anthropic API Key**
   - Get from https://console.anthropic.com/
   - Set environment variable: `ANTHROPIC_API_KEY`

### Optional

4. **Craft App** (for document integration)
   - Install Craft MCP server for Claude Code
   - Configure in Claude Code settings

5. **PowerShell 7+** (for enhanced Windows features)
   - Download from https://github.com/PowerShell/PowerShell

## Installation

### Option 1: npm Global Install

```powershell
npm install -g watchtower-windows
```

### Option 2: From Source

```powershell
# Clone the repository
git clone https://github.com/your-repo/watchtower-windows
cd watchtower-windows

# Install dependencies
npm install

# Build TypeScript
npm run build

# Link globally
npm link
```

### Verify Installation

```powershell
watchtower --version
watchtower help-full
```

## Initial Configuration

### 1. First Run

The first time you run any command, Watchtower creates:
- Configuration file at `%APPDATA%\watchtower\config.json`
- Data directory at `%APPDATA%\watchtower\`

```powershell
# Run a simple command to initialize
watchtower status
```

### 2. Configure Your Documents

If using Craft or another note system:

```powershell
# View current config
watchtower config --show

# The default document names are:
# - daily: "The Watchtower"
# - tasks: "The Forge"
# - journey: "The Long Road"
```

Edit the config file directly to change document names:
```powershell
notepad "%APPDATA%\watchtower\Config\watchtower\config.json"
```

### 3. Set Your Timezone

```powershell
watchtower config --set-timezone "America/New_York"
```

### 4. Configure Energy Windows

Edit the config to set your peak productivity hours:

```json
{
  "energyWindows": [
    { "start": 9, "end": 12, "label": "Morning Deep Work" },
    { "start": 14, "end": 17, "label": "Afternoon Focus" },
    { "start": 20, "end": 22, "label": "Evening Flow" }
  ]
}
```

### 5. Enable Optional Modules

```powershell
# Enable weekly reviews
watchtower config --enable-weekly

# Enable deep work session tracking
watchtower config --enable-deepwork

# Enable health module (for biometric data)
watchtower config --enable-health
```

## Craft MCP Integration (Optional)

If you use Craft for notes:

### 1. Install Craft MCP Server

```powershell
# In Claude Code settings, add the Craft MCP server
claude mcp install craft
```

### 2. Configure Document Links

The system uses these three documents:
- **The Watchtower**: Daily hub for briefings and field reports
- **The Forge**: Task pool with energy-categorized buckets
- **The Long Road**: Journey tracker for patterns and reflections

Create these documents in Craft, then the system will read/write to them automatically.

## Windows Task Scheduler (Optional)

Automate your morning briefing:

### Using PowerShell

```powershell
# Create scheduled task for 8 AM weekdays
$action = New-ScheduledTaskAction -Execute "watchtower" -Argument "brief"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At 8:00AM
Register-ScheduledTask -TaskName "WatchtowerBrief" -Action $action -Trigger $trigger
```

### Using Task Scheduler GUI

1. Open Task Scheduler
2. Create Basic Task
3. Name: "Watchtower Morning Brief"
4. Trigger: Daily at 8:00 AM
5. Action: Start a program
6. Program: `watchtower`
7. Arguments: `brief`

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | Yes |
| `WATCHTOWER_DATA_DIR` | Override data directory | No |
| `WATCHTOWER_DEBUG` | Enable debug logging | No |

Set in PowerShell:
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

Or permanently in System Properties > Environment Variables.

## Troubleshooting

### "Claude Code not found"

Ensure Claude Code is installed and in PATH:
```powershell
npm install -g @anthropic-ai/claude-code
claude --version
```

### "Permission denied"

Run PowerShell as Administrator for global installation:
```powershell
Start-Process powershell -Verb RunAs
```

### "API key not set"

Set your Anthropic API key:
```powershell
$env:ANTHROPIC_API_KEY = "your-key-here"
```

### Vision/OCR Issues

For card processing, ensure:
- Image is well-lit and in focus
- Supported formats: PNG, JPG, JPEG, WebP
- File size under 20MB

### Config Not Saving

Check file permissions:
```powershell
icacls "%APPDATA%\watchtower"
```

## Upgrading

```powershell
# npm installed
npm update -g watchtower-windows

# From source
git pull
npm install
npm run build
```

## Uninstalling

```powershell
# Remove global package
npm uninstall -g watchtower-windows

# Remove data (optional)
Remove-Item -Recurse "%APPDATA%\watchtower"
```

## Next Steps

1. Read the [Customization Guide](CUSTOMIZATION.md) for advanced configuration
2. Run `watchtower help-full` for command reference
3. Start with `watchtower brief` tomorrow morning!
