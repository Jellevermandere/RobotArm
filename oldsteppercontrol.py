from board import SCL, SDA
import busio
import time

#import the PCA module
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit

# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)

# Set the PWM frequency to 50hz.
pca.frequency = 1000

kit = ServoKit(channels=16)

delay = 0.01 # time to settle
stepperWires = [12,13,14,15]
stepperResolution = 512

def getHex(input):
    if input == 0:
        return 0x0000
    else:
        return 0xFFFF

def setStepper(in1, in2, in3, in4):
    pca.channels[stepperWires[0]].duty_cycle = getHex(in1)
    pca.channels[stepperWires[1]].duty_cycle = getHex(in2)
    pca.channels[stepperWires[2]].duty_cycle = getHex(in3)
    pca.channels[stepperWires[3]].duty_cycle = getHex(in4)

    time.sleep(delay)

def forwardStep():
    setStepper(1, 1, 0, 0)
    setStepper(0, 1, 1, 0)
    setStepper(0, 0, 1, 1)
    setStepper(1, 0, 0, 1)

def backwardStep():
    setStepper(1, 0, 0, 1)
    setStepper(0, 0, 1, 1)
    setStepper(0, 1, 1, 0)
    setStepper(1, 1, 0, 0)

def forwardWaveStep():
    setStepper(1, 0, 0, 0)
    setStepper(0, 1, 0, 0)
    setStepper(0, 0, 1, 0)
    setStepper(0, 0, 0, 1)

def backwardWaveStep():
    setStepper(0, 0, 0, 1)
    setStepper(0, 0, 1, 0)
    setStepper(0, 1, 0, 0)
    setStepper(1, 0, 0, 0)

# 512 steps for 360 degrees, adapt to your motor
while True:
    print ("forward")
    for i in range(stepperResolution):
        forwardWaveStep() 
    print ("backward")
    for i in range(stepperResolution):
        backwardWaveStep() 