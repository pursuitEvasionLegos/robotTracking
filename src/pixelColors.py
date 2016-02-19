""" Get colors of pixels in an image """

import cv2
import numpy as np
import argparse
import imutils


# ap = argparse.ArgumentParser()
# ap.add_argument("--image","-i")

# args = vars(ap.parse_args())



def print_mouse(event,x,y,flags,param):
    if event == 1:
        param["down"] = (y,x)
    elif event == 4:

        print "down: %s" % str(param["down"])
        print "up: %s" % str((x,y))
        y0 = min(param["down"][0],y)
        y1 = max(param["down"][0],y)+1
        x0 = min(param["down"][1],x)
        x1 = max(param["down"][1],x)+1

        mean = np.mean(param["hsv"][y0:y1,x0:x1,:],axis=(0,1))
        lower = np.percentile(param["hsv"][y0:y1,x0:x1,:],2.5,axis=(0,1))
        upper = np.percentile(param["hsv"][y0:y1,x0:x1,:],97.5,axis=(0,1))

        print "HSV mean:  [% 4d,% 4d,% 4d]" % tuple(mean)
        print "HSV lower: [% 4d,% 4d,% 4d]" % tuple(lower)
        print "HSV upper: [% 4d,% 4d,% 4d]" % tuple(upper)



camera = cv2.VideoCapture(2)
grabbed,frame = camera.read()
frame = imutils.resize(frame, width=600)
hsvFrame = cv2.cvtColor(frame.copy(),cv2.COLOR_BGR2HSV)

param = {"down":None,"hsv":hsvFrame.copy()}

cv2.namedWindow("bgr")
cv2.namedWindow("hsv")
cv2.setMouseCallback("bgr",print_mouse,param=param)
cv2.setMouseCallback("hsv",print_mouse,param=param)

while True:
    cv2.imshow("bgr",frame)
    cv2.imshow("hsv",hsvFrame)
    k = cv2.waitKey(20) & 0xFF
    if k == ord("q"):
        break
    elif k == ord("r"):
        grabbed,frame = camera.read()
        frame = imutils.resize(frame, width=600)
        hsvFrame = cv2.cvtColor(frame.copy(),cv2.COLOR_BGR2HSV)
        param["hsv"] = hsvFrame.copy()

cv2.destroyAllWindows()
