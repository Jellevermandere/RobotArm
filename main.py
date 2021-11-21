
import numpy as np
import time

from robotarm import RobotArm


robot = RobotArm()
time.sleep(1)
robot.move_robot(np.array([0.,0.2,0.]))
#time.sleep(1)
##robot.move_robot(np.array([0,0.1,0]))
#time.sleep(1)
##robot.move_robot(np.array([0.15,0.1,0.1]))
#time.sleep(1)
#robot.move_robot(np.array([-0.15,0.1,0.1]))

