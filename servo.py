
class Servo:
    pin = 0
    startAngle = 0
    angle = 0
    targetAngle = 0
    moving = False
    progress = 0
    
    def __init__(this, pin, angle):
        this.pin = pin
        this.startAngle = angle
        this.angle = angle

    def set_angle(this, targetAngle):
        this.targetAngle = targetAngle
        this.startAngle = this.angle
        this.moving = True
        this.progress = 0
        #print("Servo at pin:", this.pin, " is set for:" , this.targetAngle, "current angle:", this.angle)

    def move_servo(this, progress = 1):
        """Returns the angle the servo is on it's path to the target"""
        this.progress = progress

        if(progress >= 1):
            #the servo is arrived, return the target angle
            this.progress = 0
            this.moving = False
            this.angle = this.targetAngle
            return this.targetAngle
        else:
            this.angle = lerp(this.startAngle, this.targetAngle, this.progress)
            return this.angle

        




def lerp(start, end, value):
    return (value * end) + ((1-value) * start)
