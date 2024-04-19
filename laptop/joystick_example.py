import pygame
from time import sleep, time
import sys

if __name__ == '__main__':
    pygame.init()
    win = pygame.display.set_mode((640, 480))

    x = 320
    y =  400
    radius = 3
    vel = 15

    if (pygame.joystick.get_init()):
        print("Joystick Initialized")
        js = pygame.joystick.Joystick(0)
        print(js.get_name())
        print(js.get_numaxes())

    else: 
        print("Could not find Joystick")


    while True:
        # for i in range(js.get_numaxes()):
            #print(js.get_axis(i),end=" ")
        # print("")
        right_x = js.get_axis(2)
        right_y = js.get_axis(3)
        throttle = js.get_axis(4)
        if js.get_button(4):
            print(-((throttle+1)/2))
        else:
            print((throttle+1)/2)
    

      #  if (right_x > 5) or (right_x < -5) or (right_y > 5) or (right_y < -5):
            #print(right_x,right_y)
        win.fill((0, 0, 0))
        pygame.draw.circle(win, (255, 0, 0), (int(x), int(y)), radius)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit("Game Over")
        pygame.time.delay(10)
        pygame.display.update()