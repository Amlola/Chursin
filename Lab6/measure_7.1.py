import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time

def dec2bin(val):
    return [int(i) for i in bin(val)[2:].zfill(8)]

def adc():
    level = 0
    for i in range(bits -1, -1, -1):
        level += 2**i
        GPIO.output(dac, dec2bin(level))
        time.sleep(0.005)
        comp_val = GPIO.input(comp)
        if (comp_val == 1):
            level -= 2**i
    return level


def bin_num_leds(val):
    sig = dec2bin(val)
    GPIO.output(dac, sig)
    return sig

leds = [2, 3, 4, 17, 27, 22, 10, 9]
dac  = [8, 11, 7, 1, 0, 5, 12, 6]
troyka = 13
comp = 14
bits = len(dac)
levels = 2 ** bits

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.LOW)

data_volt = []
data_times = []

try:
    GPIO.output(troyka, 1)
    time_0 = time.time()
    val = 0
    while(val < 205):
        val = adc()
        bin_num_leds(val)
        print("volt - {:3}".format(val / levels * 3.3))
        data_volt.append(val)
        data_times.append(time.time() - time_0)

    GPIO.output(troyka, 0)

    while (val > 168):
        val = adc()
        print("volt - {:3}".format(val / levels * 3.3))
        bin_num_leds(val)
        data_volt.append(val)
        data_times.append(time.time() - time_0)

    time2 = time.time()
    with open("./settings.txt", "w") as f:
        f.write(str((time2 - time_0) / len(data_volt)))
        f.write("\n")
        f.write(str(3.3 / 256))

    print(time2 - time_0, "secs\n", len(data_volt) / (time2 - time_0), "\n", 3.3 / 256)
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.output(troyka, GPIO.LOW)
    GPIO.cleanup()

data_volt_str = [str(i) for i in data_volt]
data_times_str = [str(i) for i in data_times]

with open("./data.txt", "w") as f:
    f.write("\n".join(data_volt_str))

plt.plot(data_times, data_volt)
plt.show()