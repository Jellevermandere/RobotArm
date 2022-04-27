
from baseMotor import BaseMotor
from helper import lerp, q_lerp, clamp
import math

class Stepper(BaseMotor):
    "Base class to control and set up a stepper"

    resolution = 200
    stepsTaken = 0
    totalSteps = 0
    

    def __init__(self, angle, motor, resolution):
        super().__init__(angle, motor)
        self.resolution = resolution


    def set_angle(self, targetAngle):

        super().set_angle(targetAngle)

        self.angle %= 360
        self.targetAngle %= 360
        if(targetAngle - self.angle > 180):
            #it's shorter to go in the negative direction
            self.targetAngle -= 360
        self.startAngle = self.angle
        self.totalsteps = (self.targetAngle - self.startAngle) / 360.0 * self.resolution
        self.stepsTaken = 0
        print("Startangle:", self.startAngle, "angle:", self.angle, "targetAngle:", self.targetAngle)
        print("total steps:", self.totalsteps)

    def move(self, progress = 1):
        """Returns the angle the servo is on it's path to the target"""

        super().move(progress)

        #stepping process:
        #1. determine the total amount of steps to take -> angle/res
        #2. link the progress to the amount of steps
        #3. check which step last time
        #4. add the new number of steps to the stepper motor

        stepProgress = self.totalsteps * q_lerp(progress,self.smoothness)
        stepsToTake = int(round(stepProgress - self.stepsTaken))
        self.stepsTaken = stepProgress
        direction = False
        if(stepsToTake < 0): direction = True
        #print("Steps to take:", stepsToTake)
        self.motor.motor_go(direction, "Full" , abs(stepsToTake), 0.01 , False, .0)
        return self.angle
        #this.motor.motor_go(True, "Full" , steps, 0.01 , False, .05)




