# Watchtower Windows - Setup Guide

Complete setup instructions for the Windows productivity system.

## Prerequisites

### Required

1. **Python 3.10+**
   - Download from https://www.python.org/downloads/
   - Verify: `python --version`

2. **Claude Code SDK**
   - Install: `pip install claude-code-sdk`
   - Verify: `python -c "import claude_code_sdk; print('OK')"`

3. **Anthropic API Key**
   - Get from https://console.anthropic.com/
   - Set environment variable: `ANTHROPIC_API_KEY`

### Optional

4. **Craft App** (for document integration)
   - Install Craft MCP server for Claude Code
   - Configure in Claude Code settings

## Installation

### Option 1: pip Install

```powershell
pip install watchtower-windows
```

### Option 2: From Source

```powershell
# Clone the repository
git clone https://github.com/your-repo/watchtower-windows
cd watchtower-windows

# Install in development mode
pip install -e .
```

### Verify Installation

```powershell
watchtower --version
watchtower help-full
```

## Initial Configuration

### 1. First Run

The first time you run any command, Watchtower creates:
- Configuration file at `%APPDATA%\.watchtower\config.json`
- Data directory at `%APPDATA%\.watchtower\`

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
notepad "%APPDATA%\.watchtower\config.json"
```

### 3. Set Your Timezone

```powershell
watchtower config --set-timezone "America/New_York"
```

### 4. Enable Optional Modules

```powershell
# Enable weekly reviews
watchtower config --enable-weekly

# Enable deep work session tracking
watchtower config --enable-deepwork

# Enable health module (for biometric data)
watchtower config --enable-health
```

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

## Troubleshooting

### "Claude Code SDK not found"

Ensure the SDK is installed:
```powershell
pip install claude-code-sdk
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
icacls "%APPDATA%\.watchtower"
```

## Upgrading

```powershell
pip install --upgrade watchtower-windows
```

## Uninstalling

```powershell
# Remove package
pip uninstall watchtower-windows

# Remove data (optional)
Remove-Item -Recurse "%APPDATA%\.watchtower"
```

## Next Steps

1. Read the [README](../README.md) for usage examples
2. Run `watchtower help-full` for command reference
3. Start with `watchtower brief` tomorrow morning!
