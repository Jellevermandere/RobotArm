from board import SCL, SDA
import busio
import time

#import the PCA module
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit

from servo import Servo


class ServoController:
    servos = []
    kit = None
    speed = 180 #the degrees per second to move
    frameTime = 0.016


    def log_angles(this):
        """outputs all the current angles of the attatched servos"""

        print("these are the servo angles:")
        i = 0
        for servo in this.servos:
            print(i,": ", this.kit.servo[servo.pin].angle)
            i+=1

    def setup_servo_controller(this, servoList : list, speed = 180, frameTime = 0.016):
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
            kit.servo[pin].set_pulse_width_range(500, 2400)
            newServo = Servo(pin, max(0, min(180,kit.servo[pin].angle)))
            servos.append(newServo)

        this.kit = kit
        this.servos = servos

        this.set_smooth_servos([0] * len(servoList))

        return kit, servos

    def set_smooth_servos(this, angles):
        """Moves the servos to the target angles in the list"""

        if(len(angles) != len(this.servos)):
            print("ERROR: incorrect number of angles to move theservos to")
            return

        #set the target angles to all the servos
        for i in range(len(this.servos)):
            this.servos[i].set_angle(angles[i])

        #determine the larges angle to calculate the time to reach the target
        largestAngleDelta = 0
        for i in range(len(this.servos)):
            largestAngleDelta = max(largestAngleDelta, abs(this.servos[i].angle - angles[i]))

        duration = (largestAngleDelta / this.speed)
        steps = duration / this.frameTime
        if(steps == 0): 
            steps = 1
        progress = 0
        #print("starting movement")
        
        while progress < 1:
            #print("newLoop")
            progress += 1/steps
            progress = min(1,progress)
            for servo in this.servos:
                this.kit.servo[servo.pin].angle =  servo.move_servo(progress)
                #print(servo.pin," servo progress:" , progress, "Angle:", this.kit.servo[servo.pin].angle)
            
            time.sleep(this.frameTime)
        #print("")

    def set_servos(this, angles):
        """Set the angles for all the servos as fast as possible"""
        if(len(angles) != len(this.servos)):
            print("ERROR: incorrect number of angles to move theservos to")
            return

        #set the target angles to all the servos
        for i in range(len(this.servos)):
            this.servos[i].set_angle(angles[i])
            
        #set all the servo pins to the end value
        for servo in this.servos:
            this.kit.servo[servo.pin].angle =  servo.move_servo(1)









