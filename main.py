import numpy as np
import time

from robotarmcontrol.robotarm import RobotArm


robot = RobotArm()

robot.motorController.set_smooth_motors([0,0,0,0,0])
time.sleep(1)
robot.motorController.set_smooth_motors([0,90,0,0,0])
time.sleep(1)
robot.motorController.set_smooth_motors([0,0,0,0,0])
