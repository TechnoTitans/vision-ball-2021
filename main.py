import sensor
import image
import time
import math
import ustruct
from pyb import USB_VCP, CAN
import pyb

COMMS_METHOD = "usb"

# TODO: Check ball dimensions in inches
TARGET_WIDTH = 10
TARGET_HEIGHT = 10

# TODO: Check FOV Values
HFOV = 62.3  # 70.8 # horizontal field of view
VFOV = 55.6  # vertical field of view

SCREEN_CENTERP = 160  # screen center (pixels) horizontal
VERTICAL_CENTERP = 120  # screen center (pixels) vertical

# TODO: Set final thresholds
YELLOW_THRESHOLD_DBG = [(25, 88, -128, 24, 1, 127)]  # Dark Background
YELLOW_THRESHOLD_LBG = [(30, 100, -20, 127, 20, 127)]  # Light Background

usb = USB_VCP()
red = pyb.LED(1)
green = pyb.LED(2)
blue = pyb.LED(3)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

# TODO: Check if this is needed below
KMAN = 0.3 # constant for exposure setting
autoExposureSum = 0
readExposureNum = 10
for i in range(readExposureNum):
    autoExposureSum += sensor.get_exposure_us()

autoExposure = autoExposureSum/readExposureNum
manualExposure = int(autoExposure * KMAN) # scale factor for decreasing autoExposure
sensor.set_auto_exposure(False,  manualExposure)


def drawBox(img, blob):
    img.draw_rectangle(blob.x(), blob.y(), blob.w(), blob.h(), (255, 0, 0), 2)


def getDistanceVFOV(blob):  # gets the distance with the actual width/height of the target
    constant_term = (TARGET_HEIGHT * img.height()) / (2 * (math.tan(math.radians(VFOV / 2))))
    vertical_distance = constant_term / blob.h()
    # TODO: Get vertical correction values
    corrected_V_distance = vertical_distance + ((vertical_distance * 0.22018465) - 10.68580068)
    return corrected_V_distance


def getDistanceHFOV(blob):
    constant_term = (TARGET_WIDTH * img.height()) / (2 * (math.tan(math.radians(HFOV / 2))))
    horizontal_distance = constant_term / blob.w()
    corrected_H_distance = horizontal_distance + ((horizontal_distance * 0.22018465) - 10.68580068)
    return corrected_H_distance


def getAngleX(targetCX):  # gets the angle the turret needs to turn to be aligned with the target
    deltaX = float(SCREEN_CENTERP - targetCX)
    constant_term = (2.0 * (math.tan(math.radians(HFOV / 2.0))))/img.width()
    angleX = math.degrees(math.atan(constant_term * deltaX))
    return angleX


def getAngleY(targetCY):
    deltaY = float(SCREEN_CENTERP - targetCY)
    constant_term = (2.0 * (math.tan(math.radians(VFOV / 2.0))))/img.height()
    angleY = math.degrees(math.atan(constant_term * deltaY))
    return angleY


def beam(values):  # function that shines the LED on the camera
    if ((values[3] >= -5) and (values[3] <= 5)) and (values[3] != -1):
        green.on()
    elif values != [-1, -1, -1, -1, -1, -1]:
        blue.on()
    elif values == [-1, -1, -1, -1, -1, -1]:
        red.on()


def getValues(img):
    blobs = img.find_blobs(YELLOW_THRESHOLD_DBG)

    for blob in blobs:
        # filtering
        if blobs.roundness() < 0.77 or blobs.pixels() < 250:  # TODO: Double check pixel value
            continue

        # ===Bounding Box===
        drawBox(img, blob)

        # ===Distance===
        dv = getDistanceVFOV(blob)
        dh = getDistanceHFOV(blob)

        # ===Angle===
        angleX = getAngleX(blob.cx())
        angleY = getAngleY(blob.cy())

        # returns the final values
        valuesRobot = [blob.cx(), blob.cy(), dh, angleX, angleY, blob.w()]

        return valuesRobot

    return [-1, -1, -1, -1, -1, -1]


while True:
    img_main = sensor.snapshot()
    img = img_main.lens_corr(strength=1.1)  # TODO: Check if lens correction needed for ball

    values = getValues(img)

    if COMMS_METHOD == "print":
        print(values)
    elif COMMS_METHOD == "usb": # sending the data via USB serial to the robot
        # values = memoryview(values)
        usb.send(ustruct.pack("d", values[0], values[1], values[2], values[3], values[4], values[5]))
    elif COMMS_METHOD == "can":
        pass
