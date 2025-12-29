# Troubleshooting

Common issues and solutions for Windows.

---

## Installation Issues

### "watchtower: command not found"

The command wasn't added to PATH properly.

**Fix:**
```powershell
# Try running via Python module
python -m watchtower --help

# If that works, reinstall the package
pip install -e .

# Verify Python Scripts is in PATH
echo %PATH%
```

If the Scripts folder isn't in PATH, add it:
```powershell
# Usually located at:
# C:\Users\YourName\AppData\Local\Programs\Python\Python3xx\Scripts
```

### "pip: command not found"

Python may not be properly installed or in PATH.

**Fix:**
1. Reinstall Python from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Restart your terminal

---

## Claude Code Issues

### "Claude Code not found"

Install Claude Code first:
1. Visit [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
2. Follow installation instructions
3. Verify: `claude --version`

### Claude Code hangs or times out

**Try:**
```powershell
# Kill any running Claude processes
taskkill /f /im claude.exe

# Restart Claude Code
claude
```

Or restart your terminal/PowerShell completely.

### "Context too long" errors

Clear context between operations:
```powershell
# In Claude Code
/clear
```

Or start a fresh session:
```powershell
exit
claude
```

---

## Configuration Issues

### Config not loading

**Check:**
```powershell
# View config location
watchtower config --path

# View current config
watchtower config --show

# If missing or corrupt, delete and regenerate
del %APPDATA%\.watchtower\config.json
watchtower config --show
```

### Changes to config not taking effect

Config is loaded fresh each command. If still not working:
- Ensure valid JSON syntax
- Check for typos in key names
- Try regenerating the config file

---

## Card Processing Issues

### "Image not found"

Use full path to the image:
```powershell
# Wrong
watchtower card card.jpg

# Right
watchtower card C:\Users\YourName\Pictures\card.jpg
watchtower card %USERPROFILE%\Downloads\IMG_1234.jpeg
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
```powershell
# Supported formats
.jpg .jpeg .png .heic .webp
```

---

## Windows Task Scheduler Issues

### Scheduled briefings not running

**Check Task Scheduler:**
1. Open Task Scheduler (search in Start menu)
2. Look for "Watchtower Morning Briefing"
3. Check the History tab for errors

**Common fixes:**
```powershell
# Remove and recreate the task
watchtower schedule --disable
watchtower schedule --enable 08:00
```

### Task runs but nothing happens

The task might not find the `watchtower` command. Ensure:
1. Watchtower is installed properly: `pip install -e .`
2. The watchtower.exe is in a PATH accessible to Task Scheduler

---

## Context Menu Issues

### Right-click options not appearing

```powershell
# Reinstall context menus
watchtower uninstall-menus
watchtower install-menus
```

If still not working, try logging out and back in to refresh Explorer.

### Context menu error when clicking

The watchtower command path may have changed. Reinstall:
```powershell
watchtower uninstall-menus
pip install -e .
watchtower install-menus
```

---

## Health Module Issues

### "Health module not enabled"

**Fix:**
```powershell
watchtower config --enable-health
```

### PDF not processing

Some PDFs are image-based or have complex layouts. Try:
- Screenshot the relevant page instead
- Use a simpler PDF export if available
- Ensure the PDF isn't password-protected

---

## Performance Issues

### Commands running slowly

- Claude Code API calls take a few seconds; this is normal
- For status checks, the first call may be slower as models load

### High memory usage

- Restart your terminal session
- Clear Claude Code context: `/clear`

---

## Data Issues

### Lost tasks or data

Data is stored in:
```
%APPDATA%\.watchtower\
```

**Backup regularly:**
```powershell
copy %APPDATA%\.watchtower\*.json %USERPROFILE%\Documents\watchtower-backup\
```

### Corrupt data files

If a JSON file is corrupt:
```powershell
# View the file
type %APPDATA%\.watchtower\tasks.json

# If corrupt, you may need to delete and start fresh
del %APPDATA%\.watchtower\tasks.json
```

---

## Getting Help

If none of these solve your issue:

1. Check [GitHub Issues](https://github.com/krispuckett/hybridsystem/issues)
2. Open a new issue with:
   - What you tried
   - Error messages (exact text)
   - Your Windows version
   - Python version: `python --version`
   - Output of `watchtower config --show`
3. Reach out: [@krispuckett](https://twitter.com/krispuckett)
