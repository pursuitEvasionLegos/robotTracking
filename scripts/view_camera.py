""" Get colors of pixels in an image """

import cv2
import numpy as np
import argparse
import imutils

ap = argparse.ArgumentParser()
ap.add_argument("--device","-d",type=int,default=0)
args = vars(ap.parse_args())

d = args.get("device")
cam = cv2.VideoCapture(d)
cam.set(3,1920)
cam.set(4,1080)
dVals = [ord(str(i)) for i in range(10)]


while True:
    if cam is not None:
        grabbed,frame = cam.read()
        if grabbed:
            frame = imutils.resize(frame,width=800)
            cv2.imshow("cam %d" % d,frame)

    k = cv2.waitKey(20) & 0xFF
    if k == ord("q"):
        break
    elif k in dVals:
        for i in range(10):
            if k == ord(str(i)) and i is not d:
                newCam = cv2.VideoCapture(i)
                if newCam.isOpened():
                    cv2.destroyWindow("cam %d" % d)
                    cam.release()

                    cam = newCam
                    cam.set(3,1920)
                    cam.set(4,1080)
                    d = i
                break


cam.release()

cv2.destroyAllWindows()
