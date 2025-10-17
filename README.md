# Claude Code Notification Setup Guide

Complete guide to setting up audio and visual notifications when Claude Code completes tasks.

## Overview

This notification system alerts you when Claude Code finishes work or stops, providing:
- **macOS System Notifications** - Visual banner notifications
- **Audio Alerts** - Sound effects for completion events
- **Hook-Based System** - Automatically triggers on specific events

## Quick Start

### Current Setup

Your `~/.claude/settings.json` is configured with:

```
~/.claude/
├── settings.json                    # Hook configuration
└── hooks/
    ├── macos_notification.py       # Shows macOS notifications
    └── play_audio.py               # Plays sound effects
```

## Step-by-Step Setup

### Step 1: Create the Hooks Directory

```bash
mkdir -p ~/.claude/hooks
```

### Step 2: Create the Audio Notification Script

Create `~/.claude/hooks/play_audio.py`:

```python
#!/usr/bin/env python3
import os

# Play system sound (macOS)
os.system('afplay /System/Library/Sounds/Glass.aiff')
```

Make it executable:
```bash
chmod +x ~/.claude/hooks/play_audio.py
```

### Step 3: Create the macOS Notification Script

Create `~/.claude/hooks/macos_notification.py`:

```python
#!/usr/bin/env python3
import subprocess

# Show macOS notification
subprocess.run([
    'osascript', '-e',
    'display notification "Task completed!" with title "Claude Code" sound name "Glass"'
])
```

Make it executable:
```bash
chmod +x ~/.claude/hooks/macos_notification.py
```

### Step 4: Configure settings.json

Add this to your `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/play_audio.py"
          },
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/macos_notification.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/play_audio.py"
          },
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/macos_notification.py"
          }
        ]
      }
    ]
  }
}
```

### Step 5: Test the Setup

Run each script manually to verify:

```bash
# Test audio
python3 ~/.claude/hooks/play_audio.py

# Test notification
python3 ~/.claude/hooks/macos_notification.py
```

You should hear a sound and see a notification banner.

## How It Works

### Event Triggers

**Notification Hook** - Fires when Claude Code completes a task
- Plays audio alert
- Shows macOS notification

**Stop Hook** - Fires when Claude Code is stopped/interrupted
- Plays audio alert
- Shows macOS notification

### Matcher Field

The `"matcher": ""` is empty, meaning hooks trigger for ALL tasks regardless of type.

## Customization Options

### Change the Notification Sound

Edit `play_audio.py` to use a different system sound:

```python
#!/usr/bin/env python3
import os

# Choose from these macOS system sounds:
# Basso, Blow, Bottle, Frog, Funk, Glass, Hero, Morse, Ping, Pop, Purr, Sosumi, Submarine, Tink
os.system('afplay /System/Library/Sounds/Ping.aiff')
```

Browse all available sounds:
```bash
ls /System/Library/Sounds/
```

### Change Notification Message

Edit `macos_notification.py` to customize the message:

```python
#!/usr/bin/env python3
import subprocess

subprocess.run([
    'osascript', '-e',
    'display notification "Your custom message here!" with title "Custom Title" sound name "Ping"'
])
```

### Use Custom Audio Files

Modify `play_audio.py` to use your own audio file:

```python
#!/usr/bin/env python3
import os

# Use any audio file (.mp3, .wav, .m4a, .aiff)
os.system('afplay ~/path/to/your/custom-sound.mp3')
```

### Disable Specific Hooks

To disable notifications but keep audio:
- Remove the `macos_notification.py` hook from `settings.json`

To disable audio but keep notifications:
- Remove the `play_audio.py` hook from `settings.json`

To disable everything:
- Remove the entire `"hooks"` section from `settings.json`

## Troubleshooting

### No Sound Playing

1. **Check volume** - Make sure your system volume is up
2. **Verify sound file exists**:
   ```bash
   ls /System/Library/Sounds/Glass.aiff
   ```
3. **Test audio directly**:
   ```bash
   afplay /System/Library/Sounds/Glass.aiff
   ```
4. **Check script permissions**:
   ```bash
   ls -l ~/.claude/hooks/play_audio.py
   chmod +x ~/.claude/hooks/play_audio.py  # If not executable
   ```

### No Notification Showing

1. **Check macOS notification permissions**:
   - Open **System Settings** → **Notifications**
   - Find your **Terminal app** (Terminal, iTerm2, etc.)
   - Enable **Allow Notifications**

2. **Test notification manually**:
   ```bash
   osascript -e 'display notification "Test" with title "Test"'
   ```

3. **Verify script works**:
   ```bash
   python3 ~/.claude/hooks/macos_notification.py
   ```

### Hooks Not Triggering

1. **Verify settings.json is valid JSON**:
   ```bash
   python3 -m json.tool ~/.claude/settings.json
   ```

2. **Check file paths are correct**:
   ```bash
   ls -la ~/.claude/hooks/
   ```

3. **Ensure scripts are executable**:
   ```bash
   chmod +x ~/.claude/hooks/*.py
   ```

4. **Test scripts manually**:
   ```bash
   python3 ~/.claude/hooks/play_audio.py
   python3 ~/.claude/hooks/macos_notification.py
   ```

### Python Not Found

If you get "python3: command not found":

```bash
# Check Python installation
which python3

# Install Python via Homebrew if needed
brew install python3
```

## Advanced Configuration

### Different Sounds for Different Events

You can create separate hook scripts for different scenarios:

```bash
# Create success sound
cat > ~/.claude/hooks/play_success.py << 'EOF'
#!/usr/bin/env python3
import os
os.system('afplay /System/Library/Sounds/Glass.aiff')
EOF

# Create error sound
cat > ~/.claude/hooks/play_error.py << 'EOF'
#!/usr/bin/env python3
import os
os.system('afplay /System/Library/Sounds/Basso.aiff')
EOF

chmod +x ~/.claude/hooks/play_*.py
```

### Add Context to Notifications

Make notifications show more details by reading stdin:

```python
#!/usr/bin/env python3
import subprocess
import sys
import json

# Read context from stdin if available
try:
    context = json.loads(sys.stdin.read())
    tool_name = context.get('tool_name', 'Unknown')
    message = f"{tool_name} completed!"
except:
    message = "Task completed!"

subprocess.run([
    'osascript', '-e',
    f'display notification "{message}" with title "Claude Code"'
])
```

## Summary

You now have a complete notification system for Claude Code that:

- Plays audio alerts when tasks complete
- Shows macOS notifications with task details
- Triggers on both completion and stop events
- Can be easily customized to your preferences

The setup uses simple Python scripts and macOS built-in tools, requiring no external dependencies.

## Quick Reference

**Configuration file**: `~/.claude/settings.json`

**Hook scripts**:
- `~/.claude/hooks/play_audio.py` - Audio alerts
- `~/.claude/hooks/macos_notification.py` - Visual notifications

**Test commands**:
```bash
python3 ~/.claude/hooks/play_audio.py
python3 ~/.claude/hooks/macos_notification.py
```

**Available system sounds**: `/System/Library/Sounds/`
