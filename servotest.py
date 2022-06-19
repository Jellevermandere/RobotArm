from robotarmcontrol.motorcontrol import MotorController
import time

servoList = [0,1,2,3]

controller = MotorController()
controller.setup_servos(servoList, 180)
#time.sleep(0.5)
controller.log_angles()
controller.set_smooth_motors([90,90,90,90])
#time.sleep(0.5)
controller.log_angles()
#controller.set_smooth_servos([90,129,45,90])
#time.sleep(0.5)
#controller.log_angles()
#time.sleep(0.5)
#controller.set_smooth_servos([180,90,135,180])
#controller.log_angles()
#time.sleep(0.5)
#controller.set_smooth_servos([0,0,0,0])
#controller.log_angles()