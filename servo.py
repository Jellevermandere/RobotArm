import numpy as np


class Servo:
    pin = 0
    startAngle = 0
    angle = 0
    targetAngle = 0
    smoothness = 1.5 #min value of 1 end go to inf -> straight to step function
    
    def __init__(this, pin, angle):
        this.pin = pin
        this.startAngle = angle
        this.angle = angle

    def set_angle(this, targetAngle):
        this.targetAngle = targetAngle
        this.startAngle = this.angle

    def move_servo(this, progress = 1):
        """Returns the angle the servo is on it's path to the target"""

        if(progress >= 1):
            #the servo is arrived, return the target angle
            this.angle = this.targetAngle
        else:
            this.angle = clamp(lerp(this.startAngle, this.targetAngle, q_lerp(progress,this.smoothness)),0,180)
        return this.angle


def lerp(start, end, value):
    return (value * end) + ((1-value) * start)

def q_lerp(value : float, ease : float):
    """convert a linear value to an eased value accrding to the smoothness (0->1)"""
    return pow(value,ease) / (pow(value,ease) + pow(1-value,ease))

def clamp(value, minimum, maximum):
    return max(minimum,min(maximum,value))
    

