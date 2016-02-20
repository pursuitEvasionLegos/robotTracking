""" Convert BGR to HSV colorspace """

import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("--blue","-b","-B",type=int)
ap.add_argument("--green","-g","-G",type=int)
ap.add_argument("--red","-r","-R",type=int)


args = vars(ap.parse_args())

try:
    bgr = np.uint8([[[args.get("blue"),args.get("green"),args.get("red")]]])
    hsv = cv2.cvtColor(bgr,cv2.COLOR_BGR2HSV)

    print "BGR: [% 4d,% 4d,% 4d]" % tuple(bgr[0,0])
    print "HSV: [% 4d,% 4d,% 4d]" % tuple(hsv[0,0])
except:
    ap.print_help()
