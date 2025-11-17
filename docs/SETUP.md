# Setup Guide

Complete installation and configuration for the Hybrid System.

## Prerequisites

- **macOS** (Big Sur or later)
- **Craft Docs** - [Download](https://www.craft.do)
- **Claude Code** - [Install Guide](https://docs.claude.com/en/docs/claude-code)
- **Claude subscription** (Pro or equivalent)

## Step 1: Create Craft Documents

### Document 1: The Watchtower

1. Open Craft and create a new document
2. Name it "The Watchtower"
3. Paste this template:

```markdown
# The Watchtower

## Today - [Date]

### Morning Briefing
[Generated automatically by watchtower brief]

### Today's Card
→ [Top 3-5 items to write on physical card]

### Field Reports
[Quick captures during the day]
```

4. Click **Share** → **Enable MCP**
5. Copy the MCP URL (looks like `https://mcp.craft.do/links/XXXXX/mcp`)
6. Save this URL - you'll need it in Step 3

### Document 2: The Forge

1. Create another new document
2. Name it "The Forge"
3. Paste this template:

```markdown
# The Forge

## Deep Work
High energy required - Complex, creative tasks
- [ ] 

## Standard Work
Normal energy - Productive routine tasks
- [ ] 

## Light Work
Low energy OK - Admin, organizing, easy wins
- [ ] 

## Someday/Maybe
Ideas for later
- [ ] 
```

4. Enable MCP and copy the URL

### Document 3: The Long Road

1. Create a third document
2. Name it "The Long Road"  
3. Paste this template:

```markdown
# The Long Road

## Current Cycle
Days active: 
Last rest: 

## Recent Patterns
[Energy levels, completion rates, observations]

## Reflections
[Insights from journals or reviews]
```

4. Enable MCP and copy the URL

**You should now have three MCP URLs saved somewhere.**

## Step 2: Install Hybrid System

Open Terminal and run:

```bash
# Clone the repository
git clone https://github.com/krispuckett/hybridsystem.git
cd hybridsystem

# Make the installer executable
chmod +x install.sh

# Run installation
./install.sh
```

The installer will:
- Copy scripts to `/usr/local/bin/watchtower/`
- Create the main `watchtower` command
- Set up necessary directories

## Step 3: Connect Craft Documents

Now connect your three Craft documents to Claude Code:

```bash
# Connect The Watchtower
claude mcp add --scope user --transport http watchtower YOUR_WATCHTOWER_URL

# Connect The Forge  
claude mcp add --scope user --transport http the-forge YOUR_FORGE_URL

# Connect The Long Road
claude mcp add --scope user --transport http the-long-road YOUR_LONG_ROAD_URL
```

Replace `YOUR_WATCHTOWER_URL` etc. with the actual MCP URLs you copied in Step 1.

**Verify the connections:**
```bash
claude mcp list
```

You should see:
```
watchtower
the-forge
the-long-road
```

## Step 4: Test the System

**Test 1: Generate a morning briefing**
```bash
watchtower brief
```

Claude Code should:
- Read your three Craft documents
- Generate a briefing in The Watchtower
- Show you what to write on your card

Open Craft and check The Watchtower document - you should see the briefing.

**Test 2: Add a task**
```bash
watchtower add "Test task" normal
```

Check The Forge in Craft - the task should appear in the Standard Work section.

**Test 3: Card processing**
```bash
watchtower card
```

This will open Claude Code and wait for you to drag an image. For now, just press Ctrl+C to exit.

## Step 5: Daily Workflow Setup

### Morning Routine

Add this to your morning workflow:
1. Open Terminal
2. Run `watchtower brief`
3. Open Craft → The Watchtower
4. Write top 3-5 items on a physical card
5. Close laptop, work from card

### Evening Routine

1. Take photo of your completed card (iPhone works great)
2. AirDrop to Mac or save to Downloads
3. Run `watchtower card`
4. Drag photo into Claude Code terminal
5. Press Enter
6. Answer the energy question

## Customization

### Adjust Task Categories

Edit The Forge in Craft to match your workflow:

**By energy level:**
- High Energy Required
- Medium Energy
- Low Energy OK

**By context:**
- Office Work
- Home Tasks
- Errands

**By project:**
- Project A
- Project B
- Project C

**By time:**
- Quick Wins (< 30 min)
- Standard Tasks (1-2 hours)
- Deep Work (3+ hours)

### Customize Prompts

Scripts are located in `/usr/local/bin/watchtower/`. You can edit them to change:
- How briefings are generated
- What patterns are tracked
- Tone and style of coaching

Example:
```bash
nano /usr/local/bin/watchtower/morning-briefing.sh
```

## Troubleshooting

### Scripts don't run

```bash
chmod +x /usr/local/bin/watchtower/*.sh
```

### Craft documents not updating

1. Verify MCP connections: `claude mcp list`
2. Check MCP URLs are correct
3. Ensure documents have MCP enabled in Craft
4. Restart Claude Code: `exit` then `claude`

### Handwriting not recognized

- Ensure good lighting in photos
- Try printed text first to test
- Make sure image is clearly visible
- Drag image directly into terminal (don't paste path)

### "Permission denied" errors

```bash
sudo chmod +x /usr/local/bin/watchtower
```

## Next Steps

- Read [Commands Guide](COMMANDS.md) for all available commands
- Check [Customization Guide](CUSTOMIZATION.md) to adapt to your workflow
- See [Troubleshooting](TROUBLESHOOTING.md) for common issues

## Getting Help

- Open an issue on GitHub
- Check existing issues for solutions
- Reach out on Twitter: [@krispuckett](https://twitter.com/krispuckett)
