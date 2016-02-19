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

# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
edged = cv2.Canny(gray, 100, 300)


# find contours in the edged image, keep only the largest
# ones, and initialize our screen contour
_,cnts,_ = cv2.findContours(edged.copy(), cv2.RETR_TREE,
                            cv2.CHAIN_APPROX_SIMPLE)

allContours = image.copy()
cv2.drawContours(allContours,cnts,-1,color=(0,200,50),thickness=5)

cv2.imshow("edged",edged)
cv2.imshow("all contours",allContours)

def lenCnt(cnt):
    dist = 0.0
    for c0,c1 in zip(cnt[:-1],cnt[1:]):
        c0,c1 = c0[0],c1[0]
        dist += math.sqrt((c0[0] - c1[0])**2 + (c0[1] - c1[1])**2)
    return dist

board = max(cnts,key=lenCnt)
convexhull = image.copy()
boardCH = cv2.convexHull(board)
# cv2.drawContours(contourI,ch,-1,color=(0,200,50),thickness=5)
for p0,p1 in zip(boardCH[:-1],boardCH[1:]):
    p0,p1 = p0[0],p1[0]
    cv2.line(convexhull,tuple(p0),tuple(p1),color=(0,200,50),thickness=5)
for p in boardCH[:-1]:
    p = p[0]
    cv2.circle(convexhull,tuple(p),radius=3,color=(200,50,0),thickness=5)
cv2.imshow("convex hull",convexhull)
cv2.waitKey(0)
cv2.destroyAllWindows()
