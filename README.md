# Health Daemon

A background Python script that acts as a health guardian for workaholics.

It runs quietly in the background, and at set intervals, it plays an alarm sound, sends a system notification, and opens the Health Monitor web app to force you to take a break.

### Why This Exists

When I get deep into a project, I forget to drink water, stretch, or even blink. This daemon exists to interrupt me, so I actually take care of my body while I work.

### Features

- [x] Water reminders every 2 hours (configurable)
- [x] Plays an alarm sound and sends a desktop notification
- [x] Opens the Health Monitor web app to force you to log your progress
- [x] Stops nagging you once you reach your daily goal (e.g., 3 glasses of water)
- [x] Progress is saved to a local `health_data.json` file so it persists across restarts

### Setup

1. Install the system dependency for playing audio:

```bash
   sudo apt install ffmpeg
```

2. Install the Python dependencies:

```bash
pip install -r requirements.txt
Place an alarm.mp3 file in the same folder as daemon.py.
```

Run the script:

```bash
python3 daemon.py
```

Configuration
Open daemon.py and change these variables at the top:

WATER_GOAL: How many glasses you want to drink per day.

WATER_INTERVAL_MINUTES: How often to remind you (in minutes).

WEB_APP_URL: The URL of your Health Monitor web app.

Roadmap
- [x] Version 1.0 — Water reminder with sound, notification, and browser opening
- [ ] Version 1.1 — Add eye strain reminders (20-20-20 rule)
- [ ] Version 2.0 — Connect to a local Flask backend so the web app and Python app share data automatically
