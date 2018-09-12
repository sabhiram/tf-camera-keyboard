#!/usr/bin/env python

import cv2
import numpy as np
import math
import copy

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)

bg = None
show_orig = False

while True:
    ret, frame = cap.read()
    if frame is None:
        break

    if bg is None:
        bg = np.copy(frame)

    diff = cv2.absdiff(frame, bg)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (41, 41), 0)
    ret, thresh = cv2.threshold(blur, 30, 255, cv2.THRESH_BINARY)
    t = copy.deepcopy(thresh)
    _, cont, hier = cv2.findContours(t, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    output = copy.deepcopy(frame)
    for res in cont:
        hull = cv2.convexHull(res)
        cv2.drawContours(output, [res], 0, (0, 255, 0), 2)
        cv2.drawContours(output, [hull], 0, (0, 0, 255), 3)

    if show_orig:
        cv2.imshow("", frame)
    else:
        cv2.imshow("", output)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
