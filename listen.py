# AUTHOR: Logan Puntous
# DATE: 11/28/2025

# Listens for esp32 to send signal through GPIO 17
# Executes the send.sh script upon signal
# Waits for send.sh to finish before continuing
# Writes into movement log

import RPi.GPIO as GPIO
import subprocess
import atexit
import signal
import time
from datetime import datetime
import sys
import os

#Setup
SCRIPT = os.environ.get("CONF_SEND_SCRIPT")
FRAMES_DIR = os.environ.get("CONF_FRAMES_DIR")
GIF_DIR = os.environ.get("CONF_GIF_DIR")
LOG_DIR = os.environ.get("CONF_LOG_DIR")

for path in [LOG_DIR, FRAMES_DIR, GIF_DIR]:
    os.makedirs(path, exist_ok=True)

#GPIO
PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Subprocess setup
MAX_PROCESSES = 3
children = []
MIN_INTERVAL = 8
last_process_time = 0

#Virtual enviroment setup (for vision)
venv_path = os.environ.get("CONF_VIRTUAL_ENV")
if venv_path:
    print("Virtual environment active:", venv_path)
else:
    print("No virtual environment detected.")

#Log setup
start_date = datetime.now().strftime("%Y-%m-%d")
active_log_file = os.path.join(LOG_DIR, start_date)
with open(active_log_file, "a") as f:
        f.write("----- START OF LOG -----\n")



#Returns unique log filepath
def get_unique_filename(path):
    if not os.path.exists(path):
        return path

    base, ext = os.path.splitext(path)
    counter = 1

    new_path = f"{base}_{counter}{ext}"
    while os.path.exists(new_path):
        counter += 1
        new_path = f"{base}_{counter}{ext}"

    return new_path

#Spawns a new script child process group 
def start_child():
    global children
    p = subprocess.Popen(
        [SCRIPT],
        stdin=subprocess.DEVNULL,      
        stdout=subprocess.DEVNULL,     
        stderr=subprocess.DEVNULL,     
        preexec_fn=os.setsid
    )
    children.append(p)
    return p

#Stops all child processes
def kill_all_processes():
    for p in children:
        try:
            os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        except ProcessLookupError:
            pass  
atexit.register(kill_all_processes)



print("Starting...")
print("Ill text you if I see anything important!")


#Main Loop
try:
    while True:
        
        if GPIO.input(PIN):  # HIGH detected
            now = time.time()
            #print("Movement detected! (%s)" % datetime.now().strftime("%H:%M:%S")) #DUBUG
            children = [p for p in children if p.poll() is None]
            if len(children) < MAX_PROCESSES and now - last_process_time >= MIN_INTERVAL:
                p_new = start_child()
                #print(f"Started new process {p_new.pid}, total processes = {len(children)}.") #DEBUG
                last_process_time = now
            
            # Wait until pin goes LOW
            while GPIO.input(PIN):
                time.sleep(0.05)
        
        time.sleep(0.01)
    
except KeyboardInterrupt:
    print("\nExiting...")
    
    end_date = datetime.now().strftime("_%Y-%m-%d")
    final_log = get_unique_filename(f"{active_log_file}{end_date}.txt")

    kill_all_processes()

    with open(active_log_file, "a") as f:
        f.write("------- END OF LOG -------\n")
    if not os.path.exists(final_log):
        os.rename(active_log_file, final_log)
    
    GPIO.cleanup()
    sys.exit(0)

