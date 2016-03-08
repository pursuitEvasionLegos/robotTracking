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


def mouse_callback(event,x,y,flags,param):
    if event == 1:
        click = param["click"]
        if click < 0:
            if all(param[i]["point"] for i in range(4)):
                src = np.array([[(x,y)]],
                               dtype="float32")
                dst = cv2.perspectiveTransform(src=src,
                                              m=param["mat"])
                pts = tuple([x,y] + list(dst[0][0]))
                print "Transform: (%d,%d) --> (%f,%f)" % pts

            else:
                print "Need to calibrate points."

        else:
            param[click]["point"] = (x,y)
            param["click"] = click + 1
            if param["click"] == 4:
                param["click"] = -1

                src = np.array([param[i]["point"] for i in range(4)],
                               dtype="float32")
                param["mat"] = cv2.getPerspectiveTransform(src=src,
                                                           dst=param["dst"])


clickToCoords = [(0,0),(0,1),(1,0),(1,1)]

data = {"click": -1,
        "point": None,
        "dst": np.array(clickToCoords,dtype="float32"),
        -1: None}

for i in range(4):
    data[i] = {"asked": False,
               "point":None}

cv2.namedWindow("frame")
cv2.setMouseCallback("frame",mouse_callback,param=data)








while True:
    if cam is not None:
        grabbed,frame = cam.read()
        if grabbed:
            frame = imutils.resize(frame,width=1200)
            cv2.imshow("frame",frame)

    k = cv2.waitKey(20) & 0xFF
    if k == ord("q"):
        break

    elif k == ord("c"):
        data["click"] = 0
        for i in range(4):
            data[i] = {"asked":False,
                       "point":None}

    if data["click"] >= 0:
        if not data[data["click"]]["asked"]:
            data[data["click"]]["asked"] = True

            print "Select (%d,%d)" % clickToCoords[data["click"]]




cam.release()

cv2.destroyAllWindows()
