# This is the main control script for the robot arm
import numpy as np
import math
import time

from servocontrol import ServoController


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

UPPER_ARM_LENGTH = 0.1
LOWER_ARM_LENGTH = 0.07
SPEED = 180
FRAME_TIME = 0.016
SERVO_LIST = [0,1,2,3]

class RobotArm:

    servoController: ServoController = None

    def __init__(this):
        """Create a new instance of a RobotArm with the motors configured"""
        this.servoController = ServoController()
        this.servoController.setup_servo_controller(SERVO_LIST, SPEED, FRAME_TIME)
        print("Initialised controller with parameters:")
        print("Servos Pins:", SERVO_LIST)
        print("Speed:", SPEED, "deg/s")
        print("fps:", round(1/FRAME_TIME))

    
    def move_robot(this, targetPosition: np.array, endOffset : float = 0, endRotation : np.array = [0,0], smooth = True ):
        """Moves the robot head with a given target position, offset and rotation"""

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
        angles = [0] * len(this.servoController.servos)

        # Step 1: aim the base (0 deg is right, rotating counter clockwise)
        baseYaw = math.atan2(targetPosition[2], targetPosition[0])
        
        # Step 2: Determine the distance to the target point
            # if further than the lenght: go straight
            # else: calculate the elbow and base angle
        targetDistance = np.linalg.norm(wristTargetPos)
        print("TargetDistance: " +  str(targetDistance))
        if(np.linalg.norm(groundDirection) == 0):
            basePitch = math.pi/2
        else:
            basePitch = math.atan(wristTargetPos[1] / np.linalg.norm(groundDirection))
        elbowPitch = math.pi
        if((UPPER_ARM_LENGTH + LOWER_ARM_LENGTH) > targetDistance):
            #the target is withing reach of the robot arm
            print("The distance is within reach")
            a = UPPER_ARM_LENGTH
            b = LOWER_ARM_LENGTH
            c = targetDistance
            basePitch += math.acos((pow(b,2) - pow(c,2) - pow(a,2))/(-2 * a * c))
            elbowPitch = math.acos((pow(c,2) - pow(a,2) - pow(b,2))/(-2 * a * b))

        # Step 3: aim the wrist at the target
            # first set the wrist horizontal
            # then add the endrotation
        wristPitch = basePitch + elbowPitch -math.pi
        print("wristPitch:", math.degrees(wristPitch))
        #if(wristPitch < 0): wristPitch = -wristPitch
        wristPitch += math.radians(endRotation[0]) + math.pi/2

        # Step 4: apply all the angles to the controllers
        angles[0] = rad_to_servo(baseYaw)
        angles[1] = rad_to_servo(basePitch, True)
        angles[2] = rad_to_servo(elbowPitch)
        angles[3] = rad_to_servo(wristPitch)

        print("These are the angles for position: " + str(targetPosition))
        print("offset direction:", offsetDirection)
        print("WristtargetPos:", wristTargetPos)
        for angle in angles:
            print(angle)
        print("")

        if(smooth):
            this.servoController.set_smooth_servos(angles)
        else:
            this.servoController.set_servos(angles)

    def test_movement(this):
        """Moves the robot arm to check if all axis are working as intended"""

        # 0: The base, yaw (0,360)
        this.servoController.set_smooth_servos([0,0,0,0])
        this.servoController.set_smooth_servos([180,0,0,0])

        # 2: The elbow, pitch (0,180) -> starting closed -> ending fully stretched
        time.sleep(0.5)
        this.servoController.set_smooth_servos([180,0,180,180])
        # 1: The base, pitch (0,180) -> starting horizontal
        time.sleep(0.5)
        this.servoController.set_smooth_servos([180,180,180,0])
        
        # 3: The wrist, pitch (-90,90) -> starting straight -> 90deg up and down
        time.sleep(0.5)
        this.servoController.set_smooth_servos([0,90,180,90])
        # 4: The wrist, roll (0,360)
        time.sleep(0.5)
        this.servoController.set_smooth_servos([0,0,0,0])

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

