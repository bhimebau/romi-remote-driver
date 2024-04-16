#!/usr/bin/env python3 

import sys
from a_star import AStar
from time import sleep
import cv2
import struct
import redis
import numpy as np

def toRedis(r,a,n,fnum):
   h, w = a.shape[:2]             # Shape of the h, w and not the 3 colors in the depth of the image
   shape = struct.pack('>II',h,w) # Pack the height and the width variables into variable shape
                                  # Big Endian  
   encoded = shape + a.tobytes()  # concatenate the shape variable and the encoded image
   r.hmset(n,{'frame':fnum,'image':encoded})
   return

def motor_go(arduino_handle,speed_left,speed_right,sleep_sec):
    print(f'speed left={speed_left} speed right = {speed_right}')
    arduino_handle.motors(speed_left,speed_right)
    sleep(sleep_sec)
   
if __name__ == '__main__':
    baseboard = AStar()
    sleep_val = 1

    r = redis.Redis('localhost', port=6379, db=0, password='e101class')
    cam = cv2.VideoCapture(0)
    cam.set(3, 320)
    cam.set(4, 240)

    count = 0
    speed = 50
    led_val = 0;
    while True:
        ret, img = cam.read()
        toRedis(r, img, 'latest',count)
        count += 1
        print(count)
        motor_go(baseboard,speed,speed,sleep_val)
        if (led_val==0):
            led_val = 1
            baseboard.leds(0,0,led_val)
        else:
            led_val = 0
            baseboard.leds(0,0,led_val)
