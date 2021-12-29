from RpiMotorLib import RpiMotorLib
from baseMotor import BaseMotor
from helper import lerp, q_lerp, clamp

class Stepper(BaseMotor):
    "Base class to control and set up a stepper"

    resolution = 200
    motor = None
    angle = 0
    startAngle = 0
    targetAngle = 0

    def __init__(this, directionPin, stepPin, GPIO_pins, resolution):
        this.resolution = resolution
        this.motor = RpiMotorLib.A4988Nema(directionPin, stepPin, GPIO_pins, "A4988")

    def set_angle(this, targetAngle):
        super().set_angle(targetAngle)

        if(this.angle >= 360): this.angle -= 360
        if(this.angle < 0): this.angle += 360
        if(targetAngle - this.angle > 180):
            #it's shorter to go in the negative direction
            this.targetAngle -= 360


    def move(this, progress = 1):
        "move the stepper motor a number of steps at "
        if(progress >= 1):
            #the servo is arrived, return the target angle
            this.angle = this.targetAngle
        else:
            this.angle = clamp(lerp(this.startAngle, this.targetAngle, q_lerp(progress,this.smoothness)),0,180)
        return this.angle
        #angle = 

        #this.motor.motor_go(True, "Full" , steps, 0.01 , False, .05)




