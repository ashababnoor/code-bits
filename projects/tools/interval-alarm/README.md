# ⏰ Interval Alarm

A simple CLI tool to play an alarm sound or speak a message at regular intervals on macOS and Linux.

---

## 📦 Features
- Set interval in **seconds**, **minutes**, or **hours**
- Play a sound file (`.wav`, `.aiff`, etc.)
- Or speak a message (macOS) if no sound file is provided
- Optionally stop after a specific number of alarms
- Works on macOS (`afplay`, `say`) and Linux (`aplay`)

---

## 🚀 Usage

### Run the script:
```bash
python3 interval_alarm.py --interval <NUMBER> [options]
```

---

## 🎛️ Options

| Option             | Description |
|---------------------|-------------|
| `--interval`        | Interval value (number). **Required** |
| `--unit`            | Time unit: `sec` (seconds), `min` (minutes), `hour` (hours). Default: `min` |
| `--sound <file>`    | Path to a sound file to play |
| `--say <message>`   | Message to speak (if no sound file is given) |
| `--stop-after <n>`  | Stop after `n` alarms |

---

## 🔷 Examples

✅ Every **10 minutes** (default unit: minutes)  
```bash
python3 interval_alarm.py --interval 10
```

✅ Every **30 seconds**, stop after 5 alarms, and speak a message:  
```bash
python3 interval_alarm.py --interval 30 --unit sec --say "Time's up!" --stop-after 5
```

✅ Every **1.5 hours**, play a sound file:  
```bash
python3 interval_alarm.py --interval 1.5 --unit hour --sound /path/to/sound.wav
```

---

## 📋 Notes
- On macOS, if no `--sound` or `--say` is given, it plays the default system sound (`Glass.aiff`).
- On Linux, if no `--sound` or `--say`, it will beep (terminal bell).
- If you use `--sound`, it overrides `--say`.
- Requires `afplay` on macOS or `aplay` on Linux.

---

## 🔧 Dependencies
✅ Python 3.x  
✅ Built-in tools (`afplay`, `say` on macOS; `aplay` on Linux)

---

Enjoy your alarms! 🎉
