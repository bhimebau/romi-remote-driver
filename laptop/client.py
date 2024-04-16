#!/usr/bin/env python3

import cv2
from time import sleep, time
import struct
import redis
import numpy as np

def fromRedis(r,n):
   imdata = r.hgetall(n)                                               # get image dictionary from the server 
   encoded = imdata[b'image']
   fnum = imdata[b'frame']
   h, w = struct.unpack('>II',encoded[:8])                             # the first 8 bytes are h,w to use in the reshape
   a = np.frombuffer(encoded, dtype=np.uint8, offset=8).reshape(h,w,3) # start at offset 8, create
                                                                       # 1-dimensional array with the image data.
                                                                       # Use reshape to make it a h,w,3 image 
   return (fnum,a)

if __name__ == '__main__':
    r = redis.Redis('abot', port=6379, db=0, password='e101class')
    key = 0
    last_time = 0
    delta_time = 0
    time_temp = 0
    while key != 27:
        time_temp = time()
        delta_time = int((time_temp - last_time) * 1000)
        last_time = time_temp
        fnum, img = fromRedis(r,'latest')
        print(f"read image with shape {img.shape} frame={fnum} delta={delta_time} mS frame rate={int(1/(delta_time/1000))} fps")
        cv2.imshow('image', img)
        key = cv2.waitKey(1) & 0xFF
