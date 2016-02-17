""" Track the robot by color """


# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())



# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenlower = (38,50,50)
greenupper = (48,255,255)
bluelower = (100,50,50)
blueupper = (110,255,255)
redlower = (0,50,50)
redupper = (5,255,255)

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(1)

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])


def circleRobot(lower,upper,hsv,name):
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    inRange = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(inRange, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)



    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		            cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    hsvInRange = cv2.bitwise_and(hsv,hsv,mask=inRange)
    bgrInRange = cv2.cvtColor(hsvInRange,cv2.COLOR_HSV2BGR)
    cv2.imshow(name,bgrInRange)

    # only proceed if at least one contour was found
    if len(cnts) > 0:
	# find the largest contour in the mask, then use
	# it to compute the minimum enclosing circle and
	# centroid
	c = max(cnts, key=cv2.contourArea)
	((x, y), radius) = cv2.minEnclosingCircle(c)
	M = cv2.moments(c)
	center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

	# only proceed if the radius meets a minimum size
	if radius > 2:
	    # draw the circle and centroid on the frame,
	    # then update the list of tracked points
	    cv2.circle(frame, (int(x), int(y)), int(radius),
		       (0, 255, 255), 2)
	    cv2.circle(frame, center, 5, (0, 0, 255), -1)





# keep looping
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
	break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), sigmaX=0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    circleRobot(greenlower,greenupper,hsv,"green")
    circleRobot(bluelower,blueupper,hsv,"blue")
    circleRobot(redlower,redupper,hsv,"red")

    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
	break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
