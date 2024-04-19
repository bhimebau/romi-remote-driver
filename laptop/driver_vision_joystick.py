import pygame
import cv2
from time import sleep, time
import struct
import redis
import numpy as np
import sys

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
    r = redis.Redis('romiu', port=6379, db=0, password='e101class')
    pygame.init()
    pygame.font.init()
    win = pygame.display.set_mode((640, 480),pygame.RESIZABLE)
    pygame.display.set_caption('E321 Joystick Driver')

    js = pygame.joystick.Joystick(0)

    fobj = pygame.font.SysFont('ariel', 50)

    motor_max = 380

    run = True
    while run:
        fnum, img = fromRedis(r,'latest')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.rot90(img)
        img = pygame.surfarray.make_surface(img)
        img = pygame.transform.flip(img,True,False)
        img = pygame.transform.scale(img,win.get_size())
        win.blit(img, (0,0))

        size = win.get_size()
        pygame.draw.line(win, (255, 0, 0), (size[0]/2,size[1]*.25),(size[0]/2,size[1]*.75))
        pygame.draw.line(win, (255, 0, 0), (size[0]*.25,size[1]/2),(size[0]*.75,size[1]/2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit("Game Over")

        right_x = js.get_axis(2)
        throttle = (js.get_axis(4)+1)/2
        reverse = (js.get_axis(5)+1)/2 
        print(throttle,reverse)
        if reverse > 0.1:
            throttle = -reverse

        r_motor = motor_max * throttle 
        l_motor = motor_max * throttle

        if (right_x > 0):
            r_motor = r_motor - (r_motor*right_x*.5)
        else: 
            l_motor = l_motor -(l_motor*(-right_x)*.5)

        r.set("motor_right",int(r_motor))
        r.set("motor_left",int(l_motor))

        lspd = fobj.render(f"{int(l_motor)}", True, (0,0,255))
        rspd = fobj.render(f"{int(r_motor)}", True, (0,0,255))
        lsize = lspd.get_size()
        rsize = rspd.get_size()
        win.blit(lspd, (size[0]*.4-rsize[0]/2,size[1]/2-lsize[1]))
        win.blit(rspd, (size[0]*.6,size[1]/2-lsize[1]))
        pygame.display.update()