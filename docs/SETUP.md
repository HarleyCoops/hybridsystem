# Setup Guide

Complete setup takes about 10 minutes.

---

## Step 1: Install Prerequisites

### Python 3.10+

1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Verify installation:
   ```powershell
   python --version
   ```

### Claude Code

1. Visit [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
2. Follow installation instructions
3. Verify installation:
   ```powershell
   claude --version
   ```

---

## Step 2: Install Watchtower

```powershell
git clone https://github.com/krispuckett/hybridsystem.git
cd hybridsystem\windows-productivity
pip install -e .
```

Verify installation:
```powershell
watchtower --version
```

---

## Step 3: Initial Configuration

The first time you run a command, Watchtower creates its configuration:

```powershell
watchtower config --show
```

Configuration is stored at:
```
%APPDATA%\.watchtower\config.json
```

---

## Step 4: Enable Optional Modules (Optional)

```powershell
# Health tracking for biometric data
watchtower config --enable-health

# Weekly review generation
watchtower config --enable-weekly

# Deep work session tracking
watchtower config --enable-deepwork
```

---

## Step 5: Test It

```powershell
# Show available commands
watchtower --help

# Run your first morning briefing
watchtower brief

# Check status
watchtower status

# Add a test task
watchtower add "Test task" -p standard
```

---

## Step 6: Get a Physical Card System

The system works best with physical index cards or a card-based system:

- [Analogue](https://ugmonk.com/pages/analog) — Premium card system
- Plain index cards — Works fine
- Any pocket notebook — Cut to card size

The constraint of limited space forces prioritization.

---

## Step 7: Set Up Automation (Optional)

### Scheduled Daily Briefings

```powershell
# Schedule briefing for 8 AM on weekdays
watchtower schedule --enable 08:00
```

This creates a Windows Task Scheduler task.

### Context Menu Integration

```powershell
# Add right-click options for images
watchtower install-menus
```

Now you can right-click any image and select "Process with Watchtower (Card)".

---

## Daily Workflow

Once set up, your daily workflow is:

### Morning (5 minutes)
1. Run `watchtower brief`
2. Review the priorities
3. Write top 3-5 items on physical card
4. Work from the card all day

### Evening (5 minutes)
1. Photo your card
2. Run `watchtower card C:\Users\YourName\Pictures\photo.jpg`
3. Answer the energy question
4. Done — tomorrow is prepped

---

## Data Storage

All data is stored locally:

```
%APPDATA%\.watchtower\
├── config.json         # Configuration
├── tasks.json          # Task database
├── daily.json          # Daily entries
├── sprint.json         # Sprint tracking
├── sessions.json       # Session history
└── health-log.md       # Health data (if enabled)
```

---

## Troubleshooting

### "watchtower: command not found"

The command wasn't added to PATH. Try:
```powershell
# Check if Python Scripts is in PATH
python -m watchtower --help

# Or reinstall with pip
pip install -e .
```

### Claude Code issues

```powershell
# Verify Claude Code is working
claude --version

# Start fresh session
claude
```

### Wrong timezone

```powershell
watchtower config --set-timezone "America/New_York"
```

---

## Next Steps

- Read the [Customization Guide](CUSTOMIZATION.md) to adapt to your workflow
- Try the [Health Module](HEALTH-MODULE.md) for biometric tracking
- Check [Troubleshooting](TROUBLESHOOTING.md) if you hit issues

---

## Getting Help

- Open an issue on GitHub
- Reach out: [@krispuckett](https://twitter.com/krispuckett)
