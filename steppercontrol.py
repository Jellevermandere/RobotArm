from RpiMotorLib import RpiMotorLib
import time

from stepper import Stepper

#define GPIO pins
GPIO_pins = (13, 19, 26)    # Microstep Resolution MS1-MS3 -> GPIO Pin
direction= 20               # Direction Pin, 
step = 21                   # Step Pin
distance = 1200              # Default move 1mm => 80 steps per mm
# Declare an named instance of class pass GPIO pins numbers
baseStepper = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")
#wristStepper = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")
#baseStepper.motor_go(True, "Full" , distance, 0.01 , False, .05)

stepper = Stepper(0, baseStepper, 200)

stepper.set_angle(180)
stepper.move()

stepper.set_angle(270)
stepper.move()

stepper.set_angle(0)
stepper.move()




class StepperController():
    "control all the connected stepper motors with simple controls"
    