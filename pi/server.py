#!/usr/bin/env python3

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

if __name__ == '__main__':

    r = redis.Redis('localhost', port=6379, db=0, password='e101class')
    cam = cv2.VideoCapture(0)
    cam.set(3, 320)
    cam.set(4, 240)

    key = 0
    count = 0
    while key != 27:
        ret, img = cam.read()
        key = cv2.waitKey(1) & 0xFF
        toRedis(r, img, 'latest',count)
        count += 1
        print(count)
