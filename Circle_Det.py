import cv2
import numpy as np

Img = cv2.VideoCapture (0)

while True:
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    Success, cap = Img.read()
    cv2.imshow("camera", cap)


    grayscale = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray scale', grayscale)


    cimg = cv2.cvtColor(grayscale, cv2.COLOR_GRAY2BGR)
    circles = cv2.HoughCircles(grayscale, cv2.HOUGH_GRADIENT, 2, 50)


    try:
        for i in circles[0, :]:
            cv2.circle(cimg, (round(i[0]), round(i[1])), round(i[2]), (0, 255, 0), 2)
            cv2.circle(cimg, (round(i[0]), round(i[1])), 2, (0, 0, 255), 3)
    except:
        pass

    cv2.imshow('detected circles', cimg)


cv2.destroyAllWindows()