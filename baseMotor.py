from helper import lerp, q_lerp, clamp

class BaseMotor:
    startAngle = 0
    angle = 0
    targetAngle = 0
    smoothness = 1.5 #min value of 1 end go to inf -> straight to step function
    motor = None

    def __init__(this, angle):
        this.startAngle = angle
        this.angle = angle

    def set_angle(this, targetAngle):
        this.targetAngle = targetAngle
        this.startAngle = this.angle

    def move(this, progress = 1):
        """Set the motor to a certain angle"""

        if(progress >= 1):
            #the servo is arrived, return the target angle
            this.angle = this.targetAngle
        else:
            this.angle = lerp(this.startAngle, this.targetAngle, q_lerp(progress,this.smoothness))
        