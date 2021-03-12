import numpy as np
import cv2
cap = cv2.VideoCapture(0)
def print_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(frame[y][x])
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    ret, frame = cap.read()
    cv2.imshow('Frame', frame)

    blur = cv2.GaussianBlur(frame, (15, 15), 0)
    cv2.imshow('Gaussian Blur Image', blur)

    hsv_frame = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    cv2.setMouseCallback('Gaussian Blur Image', print_color)

    lowbound = np.array([145, 0, 231])
    upbound = np.array([194, 112, 255])

    color_mask = cv2.inRange(hsv_frame, lowbound,upbound)
    cv2.imshow('Mask Image', color_mask)

    contours, hierarchy = cv2.findContours(color_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour_image = cv2.drawContours(frame.copy(), contours, -1, (0, 255, 0))
    cv2.imshow('Contour Image', contour_image)

    result = cv2.bitwise_and(frame, frame, mask=color_mask)
    cv2.imshow('Resulting Image', result)

    if len(contours) == 0:
        continue
    scores = np.zeros(len(contours))

    area_weight = 0.5
    ideal_area = 35000
    orientation_weight = 0
    aspect_ratio_weight = 1
    ideal_aspect_ratio = 1

    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        score = np.clip(area / ideal_area, 0, 1)
        try:
            (x, y), (MA, ma), angle = cv2.fitEllipse(contours[i])
            orientation_score = np.abs((1 / 90) * (angle - 90))
        except:
            orientation_score = 0
        try:
            rect = cv2.minAreaRect(contours[i])
            short = np.min(rect[1][0], rect[1][1])
            long = np.max(rect[1][0], rect[1][1])
            aspect_ratio = short / long
            aspect_ratio_score = -1 * np.abs((1 / ideal_aspect_ratio) * (aspect_ratio - ideal_aspect_ratio)) + 1
        except:
            aspect_ratio_score = 0
        scores[i] = area_weight * score + orientation_weight * orientation_score + aspect_ratio_weight * aspect_ratio_score
    best_contour = contours[np.argmax(scores)]
    x, y, w, h = cv2.boundingRect(best_contour)
    frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    cv2.imshow("Image with bounding box", frame)
cap.release()
cv2.destroyAllWindows()
