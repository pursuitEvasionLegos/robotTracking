""" Transform pixel point to object point """

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

cv2.namedWindow("frame")
cv2.setMouseCallback("frame",mouse_callback,

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
