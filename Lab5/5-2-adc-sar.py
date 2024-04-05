import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comparator = 14
troyka = 13

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comparator, GPIO.IN)

def adc():
    k = 0
    for i in range(7, -1, -1):

        k += 2**i

        dac_val = [int(elem) for elem in bin(k)[2:].zfill(8)]

        GPIO.output(dac, dac_val)

        comp_val = GPIO.input(comparator)

        sleep(0.01)

        if comp_val == 1:
            k -= 2**i
    #print(k)
    return k

try:
    while True:
        voltage = 3.3 - adc() * 3.3 / 256.0
        if (voltage != 1.65):
            print("Voltage:", voltage)
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
    print("ERROR")
    