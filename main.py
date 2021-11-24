
import numpy as np
import time

from robotarm import RobotArm


robot = RobotArm()
while True:
    time.sleep(1)
    robot.test_movement()
#robot.move_robot(np.array([0,0.1,0]), 0., [0,0])
#time.sleep(1)
#robot.move_robot(np.array([0,0.1,0]), 0., [45,0])
#time.sleep(1)
#robot.move_robot(np.array([0,0.1,0]), 0., [90,0])
#time.sleep(1)
#robot.move_robot(np.array([0,0.1,0]), 0., [135,0])
##robot.move_robot(np.array([0,0.1,0]))
#time.sleep(1)
##robot.move_robot(np.array([0.15,0.1,0.1]))
#time.sleep(1)
#robot.move_robot(np.array([-0.15,0.1,0.1]))

