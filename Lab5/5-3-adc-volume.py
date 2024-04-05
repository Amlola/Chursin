
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
led = [2, 3, 4, 17, 27, 22, 10, 9]
comparator = 14
troyka = 13

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)
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
    if(k != 128): return k


def Volume(val):
    print("Val - ", val)
    arr = [0]*8
    for i in range(7, 0, -1):
        if ( val >= 256 - 32 * i):
            arr[i] = 1
    return arr

try:
    while True:
        i = adc()
        if i:
            volume_val = Volume(i)
            voltage = 3.3 - i * 3.3 / 256.0
            print(volume_val)
            GPIO.output(led, volume_val)
            print("Voltage:", voltage)
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
    print("ERROR")
