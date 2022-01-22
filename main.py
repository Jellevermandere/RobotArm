import numpy as np
import time

from robotarm import RobotArm


robot = RobotArm()
#robot.motorController.set_angles([0,0,0,0,0])
robot.motorController.set_smooth_motors([0,0,0,0,0])
time.sleep(1)
robot.motorController.set_smooth_motors([0,0,90,0,0])

while True:
    robot.motorController.set_smooth_motors([0,0,90,0,0])
    time.sleep(1)
    robot.motorController.set_smooth_motors([0,0,90,90,90])
    time.sleep(1)
    robot.motorController.set_smooth_motors([0,0,90,180,180])
    time.sleep(1)
    robot.motorController.set_smooth_motors([0,0,90,0,0])

#    time.sleep(1)
#robot.test_Motors()

#for i in range (1,5):
#    robot.move_robot(np.array([0.1 + i*0.1,0.1,0]))
#    time.sleep(1)
#robot.motorController.set_smooth_motors([0,0,0,0,0])
#print(1)
#robot.motorController.set_angles([0,90,0,0,0])
#time.sleep(3)
#print(2)
#robot.motorController.set_angles([0,170,0,0,0])
#time.sleep(3)
#print(3)
#robot.motorController.set_angles([0,90,0,0,0])
#time.sleep(3)
#print(4)
#robot.motorController.set_angles([0,10,0,0,0])
#time.sleep(3)
#print(5)
#robot.motorController.set_angles([0,90,0,0,0])
#time.sleep(3)
#
#print(9)
#robot.motorController.set_angles([0,10,0,0,0])
#robot.move_robot(np.array([0.3,0.5,0]))
#time.sleep(1)
#robot.move_robot(np.array([0.3,0.25,0]))
#time.sleep(1)
#robot.move_robot(np.array([0.3,0.0,0]))
#time.sleep(1)
#robot.move_robot(np.array([0.4,0.0,0]))
#time.sleep(1)
#robot.move_robot(np.array([0.5,0.0,0]))
#time.sleep(2)
#robot.motorController.set_angles([0,10,0,0,0])
#time.sleep(0.5)
#robot.motorController.reset_motors()
#time.sleep(1)
#robot.move_robot(np.array([0.05,0.1,0]), 0.01, [90,0])
#time.sleep(1)
#robot.move_robot(np.array([0.05,0.1,0]), 0.01, [135,0])
#robot.move_robot(np.array([0.1,0.1,0]))
#time.sleep(1)
#robot.move_robot(np.array([0,0.1,0.1]))
#time.sleep(1)
#robot.move_robot(np.array([-0.1,0.1,0]))
#time.sleep(1)



