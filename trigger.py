import RPi.GPIO as GPIO
import subprocess
import time

PIN = 18  # GPIO pin connected to ESP32 output

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN)

def trigger_camera(channel):
    subprocess.run(["/home/pi/scripts/take_photo.sh"])

GPIO.add_event_detect(PIN, GPIO.RISING, callback=trigger_camera, bouncetime=200)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
