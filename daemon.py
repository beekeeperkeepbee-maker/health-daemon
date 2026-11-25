import time
import os
import json
import webbrowser
import threading
import subprocess
from plyer import notification
from playsound import playsound

# --- CONFIGURATION ---
AUDIO_FILE = "alarm.mp3"
WEB_APP_URL = "https://beekeeperkeepbee-maker.github.io/health-monitor/" 
DATA_FILE = "health_data.json"

WATER_GOAL = 3
WATER_INTERVAL_MINUTES = 120  # two hours

EYE_INTERVAL_MINUTES = 20  # 20 minutes for eye break

# Global variables
water_drunk = 0
last_water_alert = time.time()
last_eye_alert = time.time()
alarm_active = False
current_sound_process = None

def load_progress():
    global water_drunk
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                water_drunk = data.get("water", 0)
                print(f"Loaded existing progress: {water_drunk} glasses of water.")
        except:
            print("Could not read data file. Starting fresh.")

def save_progress():
    with open(DATA_FILE, "w") as f:
        json.dump({"water": water_drunk}, f)

def stop_sound():
    """Kill any currently playing sound."""
    global current_sound_process
    if current_sound_process is not None:
        try:
            current_sound_process.terminate()
        except:
            pass
        current_sound_process = None

def play_sound_async():
    """Play sound in a background process so we can kill it."""
    global current_sound_process
    try:
        current_sound_process = subprocess.Popen(["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", AUDIO_FILE])
    except Exception as e:
        print(f"Could not play sound: {e}. Trying alternative method...")
        try:
            playsound(AUDIO_FILE)
        except Exception as e2:
            print(f"Alternative sound method also failed: {e2}")

def send_alert(title, message):
    """Send a water reminder: sound, notification, and open browser."""
    global alarm_active
    alarm_active = True
    print(f"\nALERT: {message}")
    
    stop_sound()
    sound_thread = threading.Thread(target=play_sound_async, daemon=True)
    sound_thread.start()
    
    try:
        notification.notify(
            title=title,
            message=message,
            app_name="Health Monitor",
            timeout=10
        )
    except Exception as e:
        print(f"Notification failed: {e}")

    webbrowser.open(WEB_APP_URL)

def send_eye_alert():
    """Send an eye break reminder: sound and notification only (no browser)."""
    print("\nEYE BREAK: Look away from the screen for 20 seconds.")
    stop_sound()
    sound_thread = threading.Thread(target=play_sound_async, daemon=True)
    sound_thread.start()
    
    try:
        notification.notify(
            title="Eye Break",
            message="Look at something 20 feet away for 20 seconds.",
            app_name="Health Monitor",
            timeout=10
        )
    except Exception as e:
        print(f"Notification failed: {e}")

def timer_loop():
    global last_water_alert, last_eye_alert, alarm_active
    while True:
        current_time = time.time()
        
        # Check water timer
        water_minutes_passed = (current_time - last_water_alert) / 60
        if water_minutes_passed >= WATER_INTERVAL_MINUTES and water_drunk < WATER_GOAL and not alarm_active:
            send_alert("Drink Water!", f"You have drunk {water_drunk}/{WATER_GOAL} glasses. Drink up!")
            last_water_alert = time.time()
        
        # Check eye timer
        eye_minutes_passed = (current_time - last_eye_alert) / 60
        if eye_minutes_passed >= EYE_INTERVAL_MINUTES:
            send_eye_alert()
            last_eye_alert = time.time()
        
        time.sleep(1)

def main():
    global water_drunk, last_water_alert, last_eye_alert, alarm_active
    load_progress()
    
    if water_drunk >= WATER_GOAL:
        print("You already reached your water goal for today! Water reminders are off.")
    else:
        print("Health Daemon is running. Water timer is active.")
        print(f"Water goal: {WATER_GOAL} glasses.")
        
        t = threading.Thread(target=timer_loop, daemon=True)
        t.start()

    try:
        while True:
            user_input = input("Press 'y' and Enter if you drank a glass of water (or 'q' to quit): ")
            if user_input.lower() == 'y':
                alarm_active = False
                stop_sound()
                
                water_drunk += 1
                save_progress()
                print(f"Progress: {water_drunk}/{WATER_GOAL} glasses.")
                
                if water_drunk >= WATER_GOAL:
                    print("Goal reached! Water reminders are now off for the day.")
                
                last_water_alert = time.time()
            elif user_input.lower() == 'q':
                break
    except KeyboardInterrupt:
        pass
    
    print("\nHealth Daemon stopped.")
    stop_sound()

if __name__ == "__main__":
    main()
