#! /usr/bin/python
# -*- coding:utf-8 -*-
from RpiMotorLib import RpiMotorLib
import time

#define GPIO pins
GPIO_pins = (14, 15, 18)    # Microstep Resolution MS1-MS3 -> GPIO Pin
direction= 21               # Direction Pin, 
step = 20                   # Step Pin
distance = 200               # Default move 1mm => 80 steps per mm
# Declare an named instance of class pass GPIO pins numbers
mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")
mymotortest.motor_go(True, "Full" , distance, 0.005 , False, .05)
