import math

import numpy as np

from robotarmcontrol.baseMotor import BaseMotor
from robotarmcontrol.helper import clamp, lerp, q_lerp


class Servo(BaseMotor):

    def move(self, progress = 1):
        """Returns the angle the servo is on it's path to the target"""
        lastAngle = self.motor.angle
        super().move(progress)

        self.motor.angle = clamp(self.angle, 0,180)
            #min(lastAngle, self.targetAngle),
            #max(lastAngle, self.targetAngle))
        return self.angle



    

