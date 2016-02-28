"""Read a QR code from a webcam
"""


import cv2
import numpy as np
import argparse
import imutils
import zbar
import Image
import sh

shape = (1920,1080)

camera = cv2.VideoCapture(2)
camera.set(3,shape[0])
camera.set(4,shape[1])


def print_mouse(event,x,y,flags,param):
    if event == 1:
        param["down"] = (y,x)
    elif event == 4:

        print "down: %s" % str(param["down"])
        print "up: %s" % str((y,x))
        y0 = min(param["down"][0],y)
        y1 = max(param["down"][0],y)+1
        x0 = min(param["down"][1],x)
        x1 = max(param["down"][1],x)+1

        frame = param["rgb"][y0:y1,x0:x1,:]

        cv2.imshow("selection",cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))

        getQr(frame)


def getQr(frame):
    scanner = zbar.ImageScanner()

    frame_str = cv2.imencode("png",frame)[1].tostring()
    image = zbar.Image(frame.width,frame.height,"Y800",frame_str)
    scanner.scan(image)
    for symbol in image:
        print symbol


param = {"rgb": None}

cv2.namedWindow("picture")
cv2.namedWindow("selection")
cv2.setMouseCallback("picture",print_mouse,param=param)

while True:
    grabbed,frame = camera.read()
    if grabbed:
        # frame = imutils.resize(frame)
        # frame = cv2.GaussianBlur(frame,(11,11),sigmaX=0)
        rgb = cv2.cvtColor(frame.copy(),cv2.COLOR_BGR2RGB)
        param["rgb"] = rgb
        cv2.imshow("picture",frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
