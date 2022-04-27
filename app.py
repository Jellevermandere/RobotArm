from xmlrpc.client import Boolean
from flask import Flask, request, redirect, render_template
from flask_socketio import SocketIO
from flask_cors import CORS
import numpy as np

from robotarm import RobotArm

app = Flask(__name__)
#socketio = SocketIO(app)
CORS(app)


robot = RobotArm()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def test():
    robot.test_movement()
    return "<p>Testing the Robot arm!</p>"

@app.route("/websocket")
def websocket():
    return render_template('websocket.html')

@app.route("/control",methods = ['POST'])
def control():
    pass



@app.route("/sliders", methods=['GET', 'POST'])
def sliders():
    if request.method == 'POST':
        print("received POST request",request.form.get("smooth"))
        baseYaw = float(request.form.get("BaseYaw"))
        basePitch = float(request.form.get("BasePitch"))
        elbowPitch = float(request.form.get("ElbowPitch"))
        wristPitch = float(request.form.get("WristPitch"))
        wristRoll = float(request.form.get("WristRoll"))
        smooth = request.form.get("smooth")
    
        if(smooth.lower() == "true"): robot.motorController.set_smooth_motors([baseYaw,basePitch,elbowPitch,wristPitch, wristRoll])
        else: robot.motorController.set_angles([baseYaw,basePitch,elbowPitch,wristPitch, wristRoll])
        return "POST Succes"

    else:
        return render_template('sliders.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 80)
    #socketio.run(app,host='0.0.0.0', port= 80)

    #/home/pi/Documents/RobotArm/app.py

    #sudo -E app.py