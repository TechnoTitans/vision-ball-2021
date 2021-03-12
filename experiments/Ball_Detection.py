#Untitled - By: HP - Mon Mar 1 2021

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

KMAN = 0.3 # constant for exposure setting
autoExposureSum = 0
readExposureNum = 10
for i in range(readExposureNum):
    autoExposureSum += sensor.get_exposure_us()

autoExposure = autoExposureSum/readExposureNum
manualExposure = int(autoExposure * KMAN) # scale factor for decreasing autoExposure
sensor.set_auto_exposure(False,  manualExposure)

yellow_threshold_BBG = [(25, 88, -128, 24, 1, 127)] #Dark Background
yellow_threshold_WBG = [(30, 100, -20, 127, 20, 127)] #Light Background

while(True):
    clock.tick()

    img = sensor.snapshot()

    for blobs in img.find_blobs(yellow_threshold_BBG): #change threshold depending on which background
        if(blobs.roundness() > 0.77 and blobs.pixels() > 250):
            img.draw_rectangle(blobs.x(), blobs.y(), blobs.w(), blobs.h(), (255, 0, 0), 2)


# TODO: Remeasure threshold and pixels in cafe
