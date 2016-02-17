""" Isolate the robot arena """


import numpy as np
import math
import imutils
import cv2
import sys



# load the query image, compute the ratio of the old height
# to the new height, clone it, and resize it

camera = cv2.VideoCapture(1)

grabbed, image = camera.read()
while not grabbed:
    grabbed, image = camera.read()

ratio = image.shape[0] / 300.0
orig = image.copy()
image = imutils.resize(image, height = 300)

# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
edged = cv2.Canny(gray, 30, 200)


# find contours in the edged image, keep only the largest
# ones, and initialize our screen contour
_,cnts,_ = cv2.findContours(edged.copy(), cv2.RETR_TREE,
                            cv2.CHAIN_APPROX_SIMPLE)

cv2.imshow("edged",edged)


# loop over our contours
approxCnts = []
for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    if len(approx) <= 5 and len(approx) >= 3:
        approxCnts.append(approx)

def lenCnt(cnt):
    dist = 0.0
    for c0,c1 in zip(cnt[:-1],cnt[1:]):
        c0,c1 = c0[0],c1[0]
        dist += math.sqrt((c0[0] - c1[0])**2 + (c0[1] - c1[1])**2)
    return dist

if approxCnts:

    board = max(approxCnts,key=lenCnt)

    imgCopy = image.copy()

    for p0,p1 in zip(board[:-1],board[1:]):
        p0 = p0[0]
        p1 = p1[0]

        cv2.line(imgCopy,tuple(p0),tuple(p1),color=(0,200,50),thickness=3)

    for p in board:
        p = p[0]
        cv2.circle(imgCopy,tuple(p),radius=5,color=(50,0,200),thickness=-1)

    cv2.imshow("countour",imgCopy)
    cv2.waitKey(0)

cv2.destroyAllWindows()
