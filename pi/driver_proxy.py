#!/usr/bin/env python3 

import sys
from a_star import AStar
from time import sleep

def motor_go(arduino_handle,speed_left,speed_right,sleep_sec):
    print(f'speed left={speed_left} speed right = {speed_right}')
    arduino_handle.motors(speed_left,speed_right)
    sleep(sleep_sec)
   
baseboard = AStar()
sleep_val = 1
torque = 50
baseboard.leds(0,0,1)
while (speed<=300):
    motor_go(baseboard,speed,speed,sleep_val)
    speed+=50
speed-=100
while (speed>=-300):
    motor_go(baseboard,speed,speed,sleep_val)
    speed-=50
speed+=100
while (speed<=0):
    motor_go(baseboard,speed,speed,sleep_val)
    speed+=50
baseboard.leds(0,0,0)  
