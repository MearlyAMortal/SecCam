#!/home/logan/ml-env/bin/python3

#Listens for esp32 to send signal through GPIO
#Executes the send.sh script upon signal

import lgpio
import subprocess
import time

CHIP = 0
PIN = 18
SCRIPT = "/home/logan/Projects/SecCam/send.sh"

handle = lgpio.gpiochip_open(CHIP)
lgpio.gpio_claim_input(handle, PIN, lgpio.SET_PULL_DOWN)

def trigger(pin, tick):
    print("Trigger received!")
    subprocess.Popen([SCRIPT])

callback = lgpio.callback(handle, PIN, lgpio.RISING_EDGE, trigger)

print("Listening for GPIO triggers on pin %d" % PIN)

#Loop
try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting...")
    callback.cancel()
    lgpio.gpiochip_close(handle)
