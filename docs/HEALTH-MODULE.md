# Health Module

An optional, tool-agnostic module for tracking biometrics and getting evidence-based health guidance.

---

## Overview

The health module:
- Accepts data from **any** health source (wearables, labs, apps)
- Stores data **locally** for privacy
- Provides **evidence-based** guidance, not medical advice
- Connects health insights to **work capacity**

---

## Enabling the Module

During installation, answer "y" when asked about the health module.

Or edit `~/.watchtower/config`:
```bash
HEALTH_MODULE_ENABLED=true
```

Then reinstall:
```bash
cd hybridsystem
./install.sh
```

---

## Commands

### `watchtower health <file>`

Process any biometric data file.

**Supported file types:**
- Images: `.png`, `.jpg`, `.jpeg`, `.heic`, `.webp`
- Documents: `.pdf`
- Data: `.csv`, `.txt`

**Examples:**
```bash
# Wearable screenshots
watchtower health ~/Downloads/oura-sleep.png
watchtower health ~/Downloads/whoop-recovery.png
watchtower health ~/Downloads/apple-watch-hrv.png

# Lab results
watchtower health ~/Downloads/bloodwork.pdf
watchtower health ~/Documents/annual-physical.pdf

# Data exports
watchtower health ~/Downloads/sleep-data.csv
```

### `watchtower coach`

Interactive Q&A for evidence-based health guidance.

```bash
watchtower coach
```

Then ask questions like:
- "Should I do intense exercise today given my HRV?"
- "What does low ferritin mean for energy?"
- "How can I improve my sleep quality?"
- "What supplements might help with recovery?"

Type `quit` to exit.

---

## Data Storage

All health data is stored locally:

```
~/.watchtower/health-log.md
```

This file:
- Is **not synced** to Craft by default
- Contains extracted metrics from your files
- Stays on your machine
- Can be deleted anytime

---

## Supported Sources

The module is **tool-agnostic** — it reads whatever you give it:

### Wearables
- Oura Ring
- Whoop
- Apple Watch
- Fitbit
- Garmin
- Any device with screenshot or export capability

### Lab Work
- Any blood test PDF
- Metabolic panels
- Hormone panels
- Nutrient levels
- Specialty labs

### Apps
- Sleep trackers
- HRV apps
- Nutrition trackers
- Any app with export capability

---

## Privacy

Your health data stays private:

1. **Local storage only** — Data never leaves your machine
2. **Not synced to Craft** — Unless you explicitly choose to
3. **No cloud processing** — Claude processes files locally via Claude Code
4. **You control deletion** — `rm ~/.watchtower/health-log.md`

---

## Limitations

The health module is **not medical advice**:

- ✅ Extracts and organizes your data
- ✅ Identifies patterns and trends
- ✅ Provides evidence-based general guidance
- ✅ Connects health to work capacity
- ❌ Does not diagnose conditions
- ❌ Does not prescribe treatments
- ❌ Does not replace professional medical care

For medical concerns, consult a healthcare provider.

---

## Research & Evidence

The coaching module grounds guidance in research:

- **Sleep**: References peer-reviewed studies on sleep architecture, circadian rhythms
- **HRV**: Uses established research on heart rate variability and recovery
- **Nutrition**: Cites evidence on nutrients, deficiencies, and supplementation
- **Exercise**: References sports science on training, recovery, overtraining

When uncertain, the module will search for current research and note the level of evidence.

---

## Disabling the Module

To disable without uninstalling:

```bash
# Edit config
nano ~/.watchtower/config

# Set to false
HEALTH_MODULE_ENABLED=false
```

To remove completely:

```bash
# Remove health scripts
sudo rm /usr/local/bin/watchtower-scripts/health-*.sh

# Remove health log (optional)
rm ~/.watchtower/health-log.md
```
