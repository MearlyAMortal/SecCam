# AUTHOR: Logan Puntous
# DATE: 11/28/2025

# Listens for esp32 to send signal through GPIO 17
# Executes the send.sh script upon signal
# Waits for send.sh to finish before continuing

import RPi.GPIO as GPIO
import subprocess
import signal
import time
from datetime import datetime
import sys
import os

PIN = 17
SCRIPT = os.environ.get("CONF_SEND_SCRIPT")

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Listening for signal from GPIO %d..." % PIN)

try:
    while True:
        if GPIO.input(PIN):  # HIGH detected
            print("Trigger received at %s" % datetime.now().strftime("%H:%M:%S"))
            subprocess.run([SCRIPT])
            # Wait until pin goes LOW
            while GPIO.input(PIN):
                time.sleep(0.05)
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nExiting...")
    GPIO.cleanup()
    sys.exit(0)
