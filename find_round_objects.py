import sensor
import image
import time
import math
import ustruct
from pyb import USB_VCP, CAN
import pyb

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE) #changing it from RGB565 to GRAYSCALE
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    img = img.gaussian(1) # applying gaussian blur
    circles = img.find_circles() #finds the circular objects

    for circle in circles:
        img.draw_circle(circle.x(), circle.y(), circle.r(), thickness = 4 ) # draws circles for every circle found
