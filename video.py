#!/usr/bin/env python

import cv2
import numpy as np
import math
import copy


count     = 0
show_orig = False


def method_1(frame, bg):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(frame, bg)
    blur = cv2.GaussianBlur(diff, (41, 41), 0)
    ret, thresh = cv2.threshold(blur, 45, 200, cv2.THRESH_BINARY)
    t = copy.deepcopy(thresh)
    _, cont, hier = cv2.findContours(t, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    output = copy.deepcopy(frame)
    for res in cont:
        hull = cv2.convexHull(res)
        cv2.drawContours(output, [res], 0, (0, 255, 0), 2)
        cv2.drawContours(output, [hull], 0, (0, 0, 255), 3)
    return output


def method_2(frame, bg):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bg    = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
    frame = cv2.absdiff(bg, frame)

    frame = cv2.medianBlur(frame, 5)
    frame = cv2.GaussianBlur(frame, (5, 5), 0)
    frame = cv2.bilateralFilter(frame, 15, 75, 75)
    frame = cv2.GaussianBlur(frame, (7, 7), 0)
    _, th = cv2.threshold(frame, 40, 255, cv2.THRESH_BINARY)

    global count
    count += 1
    if count == 200:
        print "Background settled!"
    return th


def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

    bg, out = None, []
    while True:
        ret, frame = cap.read()
        if frame is None:
            break

        if bg is None:
            bg = np.copy(frame)
            continue
        else:
            out = method_2(frame, bg)

        if show_orig:
            cv2.imshow("output", frame)
        else:
            cv2.imshow("output", out)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
