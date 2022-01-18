import time

import busio
#import the PCA module
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit
from board import SCL, SDA
from RpiMotorLib import RpiMotorLib

from servo import Servo
from stepper import Stepper


class MotorController:
    servos = []
    steppers = []
    motors = []
    servoKit = None
    speed = 90 #the degrees per second to move
    frameTime = 0.016


    def log_angles(this):
        """outputs all the current angles of the attatched servos"""

        print("these are the servo angles:")
        i = 0
        for motor in this.motors:
            print(i,": ", motor.angle)
            i+=1

    def setup_servos(this, servoList : list, speed = 180, frameTime = 0.016):
        """Prepares everything for the servo's to work"""

        this.speed = speed
        this.frameTime = frameTime

        # Create the I2C bus interface.
        i2c_bus = busio.I2C(SCL, SDA)
        # Create a simple PCA9685 class instance.
        pca = PCA9685(i2c_bus)
        # Set the PWM frequency to 60hz.
        pca.frequency = 60
        # Set the channels active
        kit = ServoKit(channels=16)

        # create new servo objects
        servos = []
        for pin in servoList:
            kit.servo[pin[0]].set_pulse_width_range(pin[1], pin[2])
            newServo = Servo(max(0, min(180,kit.servo[pin[0]].angle)), kit.servo[pin[0]])
            servos.append(newServo)

        this.kit = kit
        this.servos = servos

        return servos

    def setup_steppers(this,GPIO_pins, stepperList):
        """Sets up stepper motors to control
        stepperlist: (direction_pin, step_pin, type, resolution)"""
        steppers = []
        for pins in stepperList:
            newStepperMotor = RpiMotorLib.A4988Nema(pins[0], pins[1], GPIO_pins, pins[2])
            newStepper = Stepper(0, newStepperMotor, pins[3])
            steppers.append(newStepper)
        
        return steppers

    def set_motor_order(self, motorList):
        self.motors = motorList

    def reset_motors(self):
        self.set_smooth_motors([0] * len(self.motors))
        time.sleep(1)

    def set_smooth_motors(this, angles):
        """Moves the servos to the target angles in the list"""

        if(len(angles) != len(this.motors)):
            print("ERROR: incorrect number of angles to move theservos to")
            return

        #set the target angles to all the servos
        for i in range(len(this.motors)):
            this.motors[i].set_angle(angles[i])

        #determine the larges angle to calculate the time to reach the target
        largestAngleDelta = 0
        for i in range(len(this.motors)):
            largestAngleDelta = max(largestAngleDelta, abs(max(0,this.motors[i].angle) - angles[i]))

        duration = (largestAngleDelta / this.speed)
        steps = duration / this.frameTime
        if(steps == 0): 
            steps = 1
        progress = 0
        print("starting movement")
        startTime = time.time()
        
        
        while progress < 1:
            currentTime = time.time()
            #print("newLoop")
            progress += 1.0/steps
            progress = min(1,progress)
            for i,motor in enumerate(this.motors):
                motor.move(progress)
                if(i == 1): print("angle:", motor.motor.angle)
                #print(servo.pin," servo progress:" , progress, "Angle:", this.kit.servo[servo.pin].angle)
            #print("frameTime:", this.frameTime - (time.time()-currentTime))
            time.sleep(max(0, this.frameTime - (time.time()-currentTime)))
        #print("")

    def set_angles(this, angles):
        """Set the angles for all the servos as fast as possible"""
        if(len(angles) != len(this.motors)):
            print("ERROR: incorrect number of angles to move theservos to")
            return

        #set the target angles to all the servos
        for i in range(len(this.motors)):
            this.motors[i].set_angle(angles[i])
            
        #set all the servo pins to the end value
        for servo in this.motors:
            servo.move(1)









