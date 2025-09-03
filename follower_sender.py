from instagrapi import Client
import os
import time

USERNAME = # your instagram username
PASSWORD = # your instagram password
SETTINGS_FILE = f"{USERNAME}_settings.json"
LOG_FILE = F"{USERNAME}already_messaged.txt"
DM_LIMIT =   # <-- Set your DM limit here
DELAY_SECONDS = 5  # <-- Delay between DMs to avoid spam detection
TARGET = USERNAME
MESSAGE = "Hello! This is a test message."

cl = Client()

# Load previous session if available
if os.path.exists(SETTINGS_FILE):
    cl.load_settings(SETTINGS_FILE)

try:
    cl.login(USERNAME, PASSWORD)
except Exception as e:
    print("Login failed, retrying with fresh settings:", e)
    cl.set_settings({})
    cl.login(USERNAME, PASSWORD)

# Save session to reuse later
cl.dump_settings(SETTINGS_FILE)

# Load already messaged usernames
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        already_messaged = set(line.strip() for line in f.readlines())
else:
    already_messaged = set()

# Get your own followers
user_id = cl.user_id_from_username(TARGET)
followers = cl.user_followers(user_id)

sent_count = 0
with open(LOG_FILE, "a") as log_file:
    for follower in followers.values():
        username = follower.username

        # Skip if already messaged or limit reached
        if username in already_messaged:
            print(f"Skipping @{username} (already messaged)")
            continue
        if sent_count >= DM_LIMIT:
            print(f"DM limit of {DM_LIMIT} reached. Stopping.")
            break

        try:
            cl.direct_send(MESSAGE, [follower.pk])
            print(f"✅ DM sent to @{username}")
            log_file.write(username + "\n")  # Save to log
            already_messaged.add(username)
            sent_count += 1
            time.sleep(DELAY_SECONDS)
        except Exception as e:
            print(f"❌ Failed to message @{username}: {e}")

