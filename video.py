#!/usr/bin/env python
import cv2
import numpy as np
import math

bgModel = cv2.createBackgroundSubtractorMOG2()
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    mask = bgModel.apply(frame, learningRate=0)
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    frame = cv2.bitwise_and(frame, frame, mask=mask)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (41, 41), 0)
    ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)

    cv2.imshow("", thresh)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
