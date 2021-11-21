from servocontrol import ServoController
import time

servoList = [0,1,2,3]

controller = ServoController()
controller.setup_servo_controller(servoList, 180)
#time.sleep(0.5)
controller.log_angles()
controller.set_smooth_servos([0,150,30,0])
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