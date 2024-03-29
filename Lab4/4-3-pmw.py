import RPi.GPIO as GPIO
#import time



GPIO.setmode(GPIO.BCM)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

p = GPIO.PWM(25, 50)

try:
    while True:
        print("Input duty cycle:")
        t = int(input())
        print("V ~", 3.3 * t / 100, " volts")
        p.start(t)
        input("Press to stop")
        p.stop()

finally:
    GPIO.cleanup()