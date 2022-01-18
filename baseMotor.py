from helper import lerp, q_lerp, clamp

class BaseMotor:
    startAngle = 0
    angle = 0
    targetAngle = 0
    smoothness = 1.5 #min value of 1 end go to inf -> straight to step function
    motor = None

    def __init__(self, angle, motor):
        self.startAngle = angle
        self.angle = angle
        self.motor = motor

    def set_angle(self, targetAngle):
        self.targetAngle = targetAngle
        self.startAngle = self.angle

    def move(self, progress = 1):
        """Set the motor to a certain angle"""

        if(progress >= 1):
            #the servo is arrived, return the target angle
            self.angle = self.targetAngle
        else:
            self.angle = lerp(self.startAngle, self.targetAngle, q_lerp(progress,self.smoothness))
        