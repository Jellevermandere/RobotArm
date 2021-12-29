from flask import Flask, request, redirect
import numpy as np

from robotarm import RobotArm

app = Flask(__name__)
robot = RobotArm()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def test():
    robot.test_movement()
    return "<p>Testing the Robot arm!</p>"

@app.route("/sliders", methods=['GET', 'POST'])
def sliders():
    if request.method == 'POST':
        print("received POST request")
        baseYaw = float(request.form.get("BaseYaw"))
        basePitch = float(request.form.get("BasePitch"))
        elbowPitch = float(request.form.get("ElbowPitch"))
        wristPitch = float(request.form.get("WristPitch"))
        robot.servoController.set_smooth_servos([baseYaw,basePitch,elbowPitch,wristPitch])
        return "POST Succes"

    else:
        return '''
        <!doctype html>
        <title>Control Servos</title>
        <h1>Control the servo's with sliders</h1>
        <form onsubmit="return fetchpost()" enctype=multipart/form-data>
        <h3> BaseYaw: </h3>
        <input type="range" min="0" max="180" value="0" class="slider" name="BaseYaw" id = "BaseYaw">
        <br/>
        <h3> BasePitch: </h3>
        <input type="range" min="0" max="180" value="0" class="slider" name="BasePitch" id = "BasePitch">
        <br/>
        <h3> ElbowPitch: </h3>
        <input type="range" min="0" max="180" value="0" class="slider" name="ElbowPitch" id = "ElbowPitch">
        <br/>
        <h3> WristPitch: </h3>
        <input type="range" min="0" max="180" value="0" class="slider" name="WristPitch" id = "WristPitch">
        <br/>
        <input type=submit value=Upload>
        </form>

        <script>
        function fetchpost(){
        // (A) GET FORM DATA
        let data = new URLSearchParams();
        data.append("BaseYaw", document.getElementById("BaseYaw").value);
        data.append("BasePitch", document.getElementById("BasePitch").value);
        data.append("ElbowPitch", document.getElementById("ElbowPitch").value);
        data.append("WristPitch", document.getElementById("WristPitch").value);
        
        // (B) FETCH
        fetch("/sliders", {
            method: 'post',
            body: data
        })
        .then(function (response) {
            return response.text();
        })
        .then(function (text) {
            console.log(text);
        })
        .catch(function (error) {
            console.log(error)
        });
        
        // (C) PREVENT HTML FORM SUBMIT
        return false;
        }
        </script>
        '''

app.run(host='0.0.0.0', port= 80)