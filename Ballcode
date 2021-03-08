import sensor
import image
import time
import math
import ustruct
from pyb import USB_VCP, CAN
import pyb


#speciifying communication method: "print" "usb" "can"
COMMS_METHOD = "print"
# target_width
# target_height


# make USB_VCP object
# this lets us know if targets are being
# detected without having to print it and
# we can see if the target is aligned as well
usb = USB_VCP()
red = pyb.LED(1)
green = pyb.LED(2)
blue = pyb.LED(3)

SCREEN_CENTERP = 80 # screen center (pixels) horizontal
VERTICAL_CENTERP = 60 # Screen center (pixels) vertical

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE) # changing it from RGB565 to GRAYSCALE TODO: Check if needed
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()


# setting autoexposure automatically
KMAN = 0.065 # constant for exposure setting
autoExposureSum = 0
readExposureNum = 10
for i in range(readExposureNum):
autoExposureSum += sensor.get_exposure_us()

autoExposure = autoExposureSum/readExposureNum
manualExposure = int(autoExposure * KMAN) # scale factor for decreasing autoExposure
sensor.set_auto_exposure(False,  manualExposure) # autoset exposures


HFOV = 70.8 #horzontal field of view
VFOV = 55.6 #vertical field of view

def drawCircle(img, circle):
    img.draw_circle(circle.x(), circle.y(), circle.r(), thickness = 4 ) # draws circles for every circle found

def getCenterX(circle): #getting the center of the X coordinate of the ball
    return circle.x()

def getCenterY(circle): #getting the center of the X coordinate of the ball
    return circle.y()

def getDistanceHFOV(diameter, circle, img, HFOV): # returns the distance with actual diameter of the target
    correction_value = 1 # keep it to one unless a change is required
    d_constant = (diameter * img.width())/(2*math.tan(math.radians(HFOV/2))) * correcton_value
    distance_H = d_constant/diameter
    return distance_H

def getDistanceVFOV(diameter, circle, img, VFOV): # returns the distance with actual diameter of the target
    correction_value = 1 # keep it to one unless a change is required
    d_constant = (diameter * img.height())/(2*math.tan(math.radians(VFOV/2))) * correcton_value
    distance_V = d_constant/diameter
    return distance_V


while(True):
    clock.tick()
    img = sensor.snapshot()
    img = img.gaussian(1) # applying gaussian blur TODO: Test if blur needed
    circles = img.find_circles() #finds the circular objects

    for circle in circles:
        diameter = circle.r() * 2.0

        drawCircle(img, circle) # drawing a cirlce

        circle_centerX = getCenterX(circle)
        circle_centerY = getCenterY(circle)

        circleDistH = getDistanceHFOV(diameter, circle, img, HFOV) # not quite accurate yet
        circleDistV = getDistanceVFOV(diameter, circle, img, VFOV) # not quite accurate yet

        values = [circle_centerX, circle_centerY, circleDistH, circleDistV, 0, 0] # TODO: add angle

        if(COMMS_METHOD == "print"):
            print(values)
        elif(COMMS_METHOD == "usb"): # sending the data via USB serial to the robot
            usb.send(ustruct.pack("d", values[0], values[1], values[2], values[3], values[4], values[5]))
        elif(COMMS_METHOD == "can"):
            pass
