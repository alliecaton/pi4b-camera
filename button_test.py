#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Press button 10 times...")
for i in range(10):
    state = GPIO.input(16)
    print(f"Pin 16 state: {state}")
    time.sleep(0.5)

GPIO.cleanup()
print("Test complete")