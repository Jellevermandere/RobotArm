
class Servo:
    pin = 0
    startAngle = 0
    angle = 0
    targetAngle = 0
    smoothness = 0.3
    
    def __init__(this, pin, angle):
        this.pin = pin
        this.startAngle = angle
        this.angle = angle

    def set_angle(this, targetAngle):
        this.targetAngle = targetAngle
        this.startAngle = this.angle

    def move_servo(this, progress = 1):
        """Returns the angle the servo is on it's path to the target"""

        if(progress >= 1):
            #the servo is arrived, return the target angle
            this.angle = this.targetAngle
        else:
            this.angle = lerp(this.startAngle, this.targetAngle, q_lerp(this.progress,smoothness,smoothness))
        return this.angle


def lerp(start, end, value):
    return (value * end) + ((1-value) * start)

def q_lerp(value : float, easeIn : float, easeOut : float):
    """convert a linear value to an eased value accrding to the smoothness (0->1)"""
    P0 = [0,0]
    P1 = [1,1]
    PIn = [easeIn,0]
    POut = [1-easeOut,1]

    A = lerp(P0,PIn, value)
    B = lerp(PIn,POut, value)
    C = lerp(POut,P1, value)
    D = lerp(A,B, value)
    E = lerp(B,C, value)
    return lerp(D,E, value)

