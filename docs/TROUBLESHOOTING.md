# Troubleshooting

Common issues and solutions.

---

## Installation Issues

### "watchtower: command not found"

The main command wasn't installed properly.

**Fix:**
```bash
# Check if it exists
ls -la /usr/local/bin/watchtower

# If it's a directory (common issue from old installs)
sudo rm -rf /usr/local/bin/watchtower

# Reinstall
cd hybridsystem
./install.sh
```

### "Permission denied" when running install.sh

**Fix:**
```bash
chmod +x install.sh
./install.sh
```

### Scripts not executable

**Fix:**
```bash
sudo chmod +x /usr/local/bin/watchtower-scripts/*.sh
```

---

## Claude Code Issues

### "Claude Code not found"

Install Claude Code first:
1. Visit [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
2. Follow installation instructions
3. Verify: `claude --version`

### Claude Code hangs or times out

**Try:**
```bash
# Kill and restart
pkill -f claude
claude
```

Or restart your terminal completely.

### "Context too long" errors

Clear context between operations:
```bash
# In Claude Code
/clear
```

Or start a fresh session:
```bash
# Quit and reopen
exit
claude
```

---

## Craft MCP Issues

### "Craft MCP not detected"

The system works without Craft MCP, but you'll need to manually update documents.

**To fix:**
1. Follow [Craft's MCP guide](https://www.craft.do/imagine/guide/mcp/claude_code)
2. Verify connection: `claude mcp list`
3. Restart Claude Code after configuration

### Can't read/write Craft documents

**Check:**
1. Document is shared properly in Craft
2. MCP server is running
3. Document names in config match actual names

**Test:**
```bash
claude
# Then type:
Read my Watchtower document
```

### Changes not appearing in Craft

Craft may take a moment to sync. Also verify:
- You're looking at the right document
- The MCP is connected
- No errors in Claude Code output

---

## Time/Timezone Issues

### Wrong time in briefings

**Fix:**
```bash
# Check current timezone
date

# Set timezone in config
nano ~/.watchtower/config
# Change: TIMEZONE="America/Your_City"

# Also add to shell config
echo 'export TZ="America/Your_City"' >> ~/.zshrc
source ~/.zshrc
```

### Energy windows not working correctly

Verify your config uses 24-hour format:
```bash
# Correct
PEAK_WINDOW_1_START=9
PEAK_WINDOW_1_END=13

# Wrong
PEAK_WINDOW_1_START=9am
PEAK_WINDOW_1_END=1pm
```

---

## Card Processing Issues

### "Image not found"

Use full path to the image:
```bash
# Wrong
watchtower card card.jpg

# Right
watchtower card ~/Downloads/card.jpg
watchtower card /Users/yourname/Downloads/IMG_1234.jpeg
```

### Poor handwriting recognition

Tips for better OCR:
- Good lighting when photographing
- Flat surface, no shadows
- Clear contrast (dark ink on light paper)
- Avoid cursive if recognition is poor
- Take photo straight-on, not at an angle

### Card not processing

Check file format is supported:
```bash
# Supported
.jpg .jpeg .png .heic .webp

# Check your file
file ~/Downloads/your-image.jpg
```

---

## Config Issues

### Config not loading

**Check:**
```bash
# Verify config exists
cat ~/.watchtower/config

# If empty or missing, copy defaults
cp hybridsystem/config/defaults.conf ~/.watchtower/config
```

### Changes to config not taking effect

Config is loaded fresh each command. If still not working:
```bash
# Check for syntax errors
bash -n ~/.watchtower/config

# Should return nothing if valid
```

---

## Health Module Issues

### "Health module not installed"

**Fix:**
```bash
# Edit config
nano ~/.watchtower/config
# Set: HEALTH_MODULE_ENABLED=true

# Reinstall
cd hybridsystem
./install.sh
```

### PDF not processing

Some PDFs are image-based or have complex layouts. Try:
- Screenshot the relevant page instead
- Use a simpler PDF export if available

---

## General Issues

### Scripts work in terminal but not in Claude Code

Claude Code may have different PATH. Use full paths:
```bash
/usr/local/bin/watchtower-scripts/morning-briefing.sh
```

### "No such file or directory"

Check the path exists:
```bash
ls -la /path/you/specified
```

### Performance is slow

- Clear Claude Code context: `/clear`
- Restart Claude Code
- Check if Craft documents are very large (trim old entries)

---

## Getting Help

If none of these solve your issue:

1. Check [GitHub Issues](https://github.com/krispuckett/hybridsystem/issues)
2. Open a new issue with:
   - What you tried
   - Error messages (exact text)
   - Your macOS version
   - Output of `watchtower status`
3. Reach out: [@krispuckett](https://twitter.com/krispuckett)
