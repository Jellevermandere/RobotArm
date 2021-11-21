# This is the main control script for the robot arm
import numpy as np
import math

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

# the coordinate sytem: -Z: forward, X: right Y: up

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
        print("Initialised controller")

    
    def move_robot(this, targetPosition: np.array, endOffset : float = None, endRotation : np.array = None ):
        """Moves the robot head with a given target position, offset and rotation"""

        # Check if position is valid (e.g. if the Y position > 0)
        if(targetPosition[1] < 0):
            return False

        groundDirection = np.array([targetPosition[0],0,targetPosition[2]])
        endRad = math.radians(endRotation)
        offsetDirection = groundDirection * math.cos(endRad) + np.array([0,1,0]) * math.sin(endRad)

        wristTargetPos = targetPosition - offsetDirection * endOffset

        # create the angleList for the servoController
        angles = [0] * len(this.servoController.servos)

        # Step 1: aim the base (0 deg is right, rotating clockwise)
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

        print("These are the angles for position: " + str(targetPosition))
        print("Base: Yaw: " + str(baseYaw * 180 / math.pi) + ", Pitch:" + str(basePitch* 180 / math.pi))
        print("elbow: Pitch: " + str(elbowPitch* 180 / math.pi))
        print("")

        # Step 3: aim the wrist at the target
        wristPitch = 

        # Step 4: apply all the angles to the controllers
        angles[0] = rad_to_servo(baseYaw)
        angles[1] = rad_to_servo(basePitch, True)
        angles[2] = rad_to_servo(elbowPitch)
        angles[3] = 90

        this.servoController.set_smooth_servos(angles)

def rad_to_servo(rad, sup = False):
    if(sup):
        return max(0,min(180, 180 - math.degrees(rad)))
    else:
        return max(0,min(180,math.degrees(rad)))



