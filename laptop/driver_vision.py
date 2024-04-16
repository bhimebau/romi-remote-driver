import pygame
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
    r = redis.Redis('romiu', port=6379, db=0, password='e101class')
    pygame.init()
    win = pygame.display.set_mode((640, 480))

    x = 320
    y =  400
    radius = 3
    vel = 15
    motor_speed = 0
    motor_diff = 0
    r_motor = 0
    l_motor = 0
    motor_stop = 1
    speed_inc = 20
    turning_inc = 10

    run = True
    while run:
        fnum, img = fromRedis(r,'latest')
        # print(f"read image with shape {img.shape} frame={fnum} delta={delta_time} mS frame rate={int(1/(delta_time/1000))} fps")
        # v2.imshow('image', img)
        key = cv2.waitKey(1) & 0xFF

        win.fill((0, 0, 0))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.rot90(img)
        img = pygame.surfarray.make_surface(img)
        img = pygame.transform.flip(img,True,False)
        win.blit(img, (0,0))
        pygame.draw.circle(win, (255, 0, 0), (int(x), int(y)), radius)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT:
                    motor_stop = 0
                    x -= vel
                    motor_diff -= turning_inc
                if event.key == pygame.K_RIGHT:
                    motor_stop = 0
                    x += vel
                    motor_diff += turning_inc
                if event.key == pygame.K_UP:
                    motor_stop = 0
                    y -= vel
                    motor_speed += speed_inc
                    if motor_speed > 300:
                        motor_speed = 300
                if event.key == pygame.K_DOWN:
                    motor_stop = 0
                    y += vel
                    if y>=400:
                        y=400
                    motor_speed -= speed_inc
                    if motor_speed < 0:
                        motor_speed = 0
                if event.key == pygame.K_SPACE:
                    motor_stop = 1

        print(motor_diff, l_motor, r_motor)          
        if motor_stop:
            motor_diff = 0
            motor_speed = 0
            r_motor = 0
            l_motor = 0
            x = 320
            y =  400
        else: 
            if (motor_diff > 0):
                r_motor = motor_speed - motor_diff 
                if r_motor < 0:
                    r_motor = 0
                l_motor = motor_speed 
            else:
                l_motor = motor_speed + motor_diff 
                if l_motor < 0:
                    l_motor = 0
                r_motor = motor_speed
        r.set("motor_right",r_motor)
        r.set("motor_left",l_motor)
        pygame.time.delay(10)
        pygame.display.update()