import numpy as np
import time

from robotarm import RobotArm


robot = RobotArm()

robot.motorController.set_angles([0,0,0,0,0])
time.sleep(1)
robot.motorController.set_smooth_motors([0,90,0,0,0])
time.sleep(1)
robot.motorController.set_smooth_motors([0,90,180,0,0])
time.sleep(1)
robot.motorController.set_smooth_motors([0,90,0,0,0])
time.sleep(1)
robot.motorController.set_smooth_motors([0,0,0,0,0])
#robot.motorController.set_angles([180,0,90,90,0]
#time.sleep(1)
#robot.motorController.set_angles([180,180,90,90,0])
#time.sleep(1)
##robot.motorController.set_smooth_motors([0,0,0,0,0]
##robot.move_robot(np.array([1,1,1]))
##robot.motorController.reset_motors()
##time.sleep(1)
#robot.motorController.set_angles([0,0,0,0,0])
#time.sleep(1)

#robot.motorController.set_smooth_motors([0,0,0,0,0])
#time.sleep(1)
#robot.motorController.set_smooth_motors([180,180,180,180,0])
#time.sleep(1)
#robot.motorController.set_smooth_motors([180,0,90,90,0])
#time.sleep(1)
#robot.motorController.set_smooth_motors([90,90,90,90,0])
#time.sleep(1)
##robot.motorController.set_smooth_motors([0,0,0,0,0]
##robot.move_robot(np.array([1,1,1]))
##robot.motorController.reset_motors()
##time.sleep(1)
#robot.motorController.set_smooth_motors([0,0,0,0,0])
#time.sleep(1)

#while True:
#   robot.motorController.set_smooth_motors([0,0,0,0,0])
#   time.sleep(1)
#   robot.motorController.set_smooth_motors([0,180,180,180,180])
#   #robot.motorController.set_smooth_motors([0,45,0,0,0])
#   time.sleep(1)
