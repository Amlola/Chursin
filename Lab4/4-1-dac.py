import RPi.GPIO as GPIO
import time



GPIO.setmode(GPIO.BCM)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setup(dac, GPIO.OUT)


def dec2bin(val):
    return[int(i) for i in bin(val)[2:].zfill(8)]


try:
    print("Input 0-255 number:")
    num = input()

    if num != 'q' and num.isdigit() and (0 <= int(num) <= 255):
        num = int(num)
        GPIO.output(dac, dec2bin(num))
        time.sleep(15)
        print("V ~~ ", 3.3 * (num / 255), " volts")

    else:
        if (num.isdigit()):
            print("Wrong value!")
        else:
            print("Input number, not a letter!")

    
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()

