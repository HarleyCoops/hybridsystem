# Hybrid System

A productivity system that bridges pen-and-paper workflow with AI-powered digital intelligence.

**Morning:** AI generates daily priorities  
**Day:** Work from a physical card  
**Evening:** Photo your card → AI reads handwriting → updates everything automatically

Built with [Craft Docs](https://craft.do), [Claude Code](https://docs.claude.com/en/docs/claude-code), and Craft's MCP server.

## Quick Start

**Requirements:**
- macOS
- [Craft Docs](https://www.craft.do) (free tier works)
- [Claude Code](https://docs.claude.com/en/docs/claude-code) (requires Claude subscription)

**Install:**
```bash
git clone https://github.com/krispuckett/hybridsystem.git
cd hybridsystem
./install.sh
```

**Setup takes 10 minutes.** Follow the [Setup Guide](docs/SETUP.md).

## How It Works

### Three Connected Documents

**The Watchtower** (Daily Hub)
- Morning briefing with prioritized tasks
- Field reports for quick captures
- Links to your task pool

**The Forge** (Task Pool)
- Organized by energy/context
- Deep Work, Standard Tasks, Light Work, Someday

**The Long Road** (Journey Tracker)
- Work/rest cycle tracking
- Pattern recognition over time
- Insights from reflections

### Daily Workflow

**Morning (5 min):**
```bash
watchtower brief
```
Generates priorities. Write top 3-5 on a physical card.

**Evening (5 min):**
```bash
watchtower card
```
Drag card photo into terminal. AI reads handwriting, updates tasks automatically.

**Anytime:**
```bash
watchtower add "task description" normal
watchtower journal  # Process journal entries
watchtower status   # See system overview
```

## Why It Works

**The constraint of paper forces real prioritization.**  
**The intelligence of digital routes you to the right work.**

Low energy isn't failure—it's a signal to do different work, not no work.

## Technical Details

**Vision AI** reads handwritten text (~90% accuracy on cursive)  
**Craft MCP** enables direct document updates via Model Context Protocol  
**Bash scripts** handle automation without complex dependencies

Everything runs locally. Your data stays yours.

## Documentation

- [Setup Guide](docs/SETUP.md) - Initial configuration
- [Commands](docs/COMMANDS.md) - All available commands
- [Customization](docs/CUSTOMIZATION.md) - Adapt to your workflow
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues

## Screenshots

![Three Craft Documents](images/craft-docs.png)
![Physical Card Workflow](images/card-workflow.png)
![Terminal OCR Processing](images/terminal-ocr.png)

## Philosophy

This system assumes:
- Your capacity varies day-to-day
- Physical constraints improve focus
- Digital intelligence improves routing
- Quick capture prevents losing ideas
- Patterns emerge when tracked consistently

Built for people who work in energy waves, not steady streams.

## Contributing

Improvements welcome! This is a personal productivity tool that others might find useful.

**Ideas for contributions:**
- Better error handling
- Windows/Linux support
- Alternative MCP integrations (Obsidian, Notion)
- Documentation improvements

## License

MIT - Use freely, modify as needed, share improvements.

## Acknowledgments

Built during one Saturday evening exploring what's possible with:
- [Craft's MCP server](https://www.craft.do/imagine/guide/mcp/claude_code)
- [Claude Code](https://docs.claude.com/en/docs/claude-code)
- [Model Context Protocol](https://modelcontextprotocol.io)

## Questions?

Open an issue or reach out: [@krispuckett](https://twitter.com/krispuckett) on Twitter

---

**Cost:** $0 (with existing Claude subscription)  
**Setup time:** 10 minutes  
**Daily overhead:** 10 minutes (5 min morning + 5 min evening)
