# This is the main control script for the robot arm
import math
import time

import numpy as np
from RPi import GPIO

from robotarmcontrol.motorcontrol import MotorController

# the main control method is IK using a position as a target
# The robot arm has 5 control points:
    # 0: The base, yaw (0,360)
    # 1: The base, pitch (0,180) -> starting horizontal
    # 2: The elbow, pitch (0,180) -> starting closed -> ending fully stretched
    # 3: The wrist, pitch (-90,90) -> starting straight -> 90deg up and down
    # 4: The wrist, roll (0,360)
# It always aims straight for he target point, bending the elbow outward
# the robot can be aimed with a position and rotation offset, and a final wrist rotation

# the coordinate sytem: Z: forward, X: right Y: up

#robot settings
UPPER_ARM_LENGTH = 0.35
LOWER_ARM_LENGTH = 0.25
SPEED = 90 #degrees per second
FRAME_TIME = 0.016 #the fps of the robot

#servo settings
#SERVO_LIST = [[11,500,2400],[10, 400,1666],[9,500,2400 ],[8, 500,2200],[7,500,2400]]
#SERVO_LIST = [[0,500,2400],[4, 500,2400],[8,500,2400 ],[12, 500,2400],[15,500,2400]]
SERVO_LIST = [[11,500,2250],[10, 400,1666],[9,500,2400 ],[8, 500,2400]]

#stepper settings
GPIO_PINS = (13, 19, 26) 
STEPPER_TYPE = "A4988"
STEPPER_DIRECTION_PIN = 21
STEPPER_STEP_PIN = 20
STEPPER_RESOLUTION = 200 * 10/3 #steps per rotation
STEPPER_LIST = [[STEPPER_DIRECTION_PIN, STEPPER_STEP_PIN, STEPPER_TYPE, STEPPER_RESOLUTION]]

class RobotArm:

    motorController: MotorController = None
    moving = False

    def __init__(this):
        """Create a new instance of a RobotArm with the motors configured"""
        this.motorController = MotorController()
        servos = this.motorController.setup_servos(SERVO_LIST, SPEED, FRAME_TIME)
        steppers = this.motorController.setup_steppers(GPIO_PINS, STEPPER_LIST)
        #motorList = [servos[4], servos[0], servos[1], servos[2], servos[3]]
        #motorList = [servos[0], servos[1], servos[2], servos[3], servos[4]]
        motorList = [steppers[0], servos[0], servos[1], servos[3], servos[2]]
        this.motorController.set_motor_order(motorList)
        this.motorController.reset_motors()
        print("Initialised controller with parameters:")
        print("Servos Pins:", SERVO_LIST)
        print("Speed:", SPEED, "deg/s")
        print("fps:", round(1/FRAME_TIME))

    
    def move_robot(this, targetPosition: np.array, endOffset : float = 0, endRotation : np.array = [0,0], smooth = True ):
        """Moves the robot head with a given target position, offset and rotation"""

        if(this.moving): return False
        
        this.moving = True
        # Check if position is valid (e.g. if the Y position > 0)
        if(targetPosition[1] < 0):
            return False

        # Offset the target position with the end offset & rotation
        groundDirection = np.array([1,0,1]) * targetPosition
        upDirection = np.array([0,1,0])
        endRad = - math.radians(endRotation[0])
        offsetDirection = normalize(groundDirection) * math.cos(endRad) + upDirection * math.sin(endRad)
        wristTargetPos = targetPosition - normalize(offsetDirection) * endOffset
        groundDirection = np.array([1,0,1]) * wristTargetPos

        # create the angleList for the servoController
        angles = [0] * len(this.motorController.motors)

        # Step 1: aim the base (0 deg is right, rotating counter clockwise)
        baseYaw = math.atan2(targetPosition[2], targetPosition[0])
        
        # Step 2: Determine the distance to the target point
            # if further than the lenght: go straight
            # else: calculate the elbow and base angle
        targetDistance = np.linalg.norm(wristTargetPos)
        #print("TargetDistance: " +  str(targetDistance))
        if(np.linalg.norm(groundDirection) == 0):
            basePitch = math.pi/2
        else:
            basePitch = math.atan(wristTargetPos[1] / np.linalg.norm(groundDirection))
        elbowPitch = math.pi
        if((UPPER_ARM_LENGTH + LOWER_ARM_LENGTH) > targetDistance):
            #the target is withing reach of the robot arm
            #print("The distance is within reach")
            a = UPPER_ARM_LENGTH
            b = LOWER_ARM_LENGTH
            c = targetDistance
            basePitch += math.acos((pow(b,2) - pow(c,2) - pow(a,2))/(-2 * a * c))
            elbowPitch = math.acos((pow(c,2) - pow(a,2) - pow(b,2))/(-2 * a * b))

        # Step 3: aim the wrist at the target
            # first set the wrist horizontal
            # then add the endrotation
        wristPitch = basePitch + elbowPitch -math.pi
        #print("wristPitch:", math.degrees(wristPitch))
        #if(wristPitch < 0): wristPitch = -wristPitch
        wristPitch += math.radians(endRotation[0]) + math.pi/2

        # Step 4: apply all the angles to the controllers
        angles[0] = rad_to_servo(baseYaw)
        angles[1] = rad_to_servo(basePitch, True)
        angles[2] = rad_to_servo(elbowPitch)
        angles[3] = rad_to_servo(wristPitch)

        #print("These are the angles for position: " + str(targetPosition))
        #print("offset direction:", offsetDirection)
        #print("WristtargetPos:", wristTargetPos)
        #for angle in angles:
        #    print(angle)
        #print("")

        if(smooth):
            this.motorController.set_smooth_motors(angles)
        else:
            this.motorController.set_angles(angles)

        this.moving = False

    def test_movement(this):
        """Moves the robot arm to check if all axis are working as intended"""

        # 0: The base, yaw (0,360)
        this.motorController.set_smooth_motors([0,0,0,0])
        this.motorController.set_smooth_motors([180,0,0,0])

        # 2: The elbow, pitch (0,180) -> starting closed -> ending fully stretched
        time.sleep(0.5)
        this.motorController.set_smooth_motors([180,0,180,180])
        # 1: The base, pitch (0,180) -> starting horizontal
        time.sleep(0.5)
        this.motorController.set_smooth_motors([180,180,180,0])
        
        # 3: The wrist, pitch (-90,90) -> starting straight -> 90deg up and down
        time.sleep(0.5)
        this.motorController.set_smooth_motors([0,90,180,90])
        # 4: The wrist, roll (0,360)
        time.sleep(0.5)
        this.motorController.set_smooth_motors([0,0,0,0])

    def test_Motors(this):
        """Moves the robot arm to check if all axis are working as intended"""

        # 0: The base, yaw (0,360)
        this.motorController.set_smooth_motors([0,0,0,0,0])
        this.motorController.set_smooth_motors([180,180,180,180,180])

        # 2: The elbow, pitch (0,180) -> starting closed -> ending fully stretched
        time.sleep(0.5)
        this.motorController.set_smooth_motors([90,90,90,90,90])
        # 1: The base, pitch (0,180) -> starting horizontal
        time.sleep(0.5)
        this.motorController.set_smooth_motors([45,45,45,45,45])
        
        # 3: The wrist, pitch (-90,90) -> starting straight -> 90deg up and down
        time.sleep(0.5)
        this.motorController.set_smooth_motors([135,135,135,135,135])
        # 4: The wrist, roll (0,360)
        time.sleep(0.5)
        this.motorController.set_smooth_motors([0,0,0,0,0])
    

def rad_to_servo(rad, sup = False):
    if(sup):
        return max(0,min(180, 180 - math.degrees(rad)))
    else:
        return max(0,min(180,math.degrees(rad)))

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

