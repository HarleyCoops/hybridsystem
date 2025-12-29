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

```powershell
watchtower config --enable-health
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
```powershell
# Wearable screenshots
watchtower health C:\Users\YourName\Pictures\oura-sleep.png
watchtower health %USERPROFILE%\Downloads\whoop-recovery.png
watchtower health %USERPROFILE%\Downloads\apple-watch-hrv.png

# Lab results
watchtower health C:\Users\YourName\Documents\bloodwork.pdf
watchtower health %USERPROFILE%\Documents\annual-physical.pdf

# Data exports
watchtower health %USERPROFILE%\Downloads\sleep-data.csv
```

### `watchtower coach "question"`

Ask health-related questions for evidence-based guidance.

```powershell
watchtower coach "Should I do intense exercise today given my HRV?"
watchtower coach "What does low ferritin mean for energy?"
watchtower coach "How can I improve my sleep quality?"
watchtower coach "What supplements might help with recovery?"
```

---

## Data Storage

All health data is stored locally:

```
%APPDATA%\.watchtower\health-log.md
```

This file:
- Is **not synced** anywhere by default
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
2. **Not synced** — Unless you explicitly choose to
3. **No cloud processing** — Claude processes files locally via Claude Code
4. **You control deletion** — Just delete the health-log.md file

To delete health data:
```powershell
del %APPDATA%\.watchtower\health-log.md
```

---

## Limitations

The health module is **not medical advice**:

- Extracts and organizes your data
- Identifies patterns and trends
- Provides evidence-based general guidance
- Connects health to work capacity
- Does **NOT** diagnose conditions
- Does **NOT** prescribe treatments
- Does **NOT** replace professional medical care

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

To disable:

```powershell
watchtower config --disable-health
```

To remove health data completely:

```powershell
del %APPDATA%\.watchtower\health-log.md
```
