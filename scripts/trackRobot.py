""" Track the robot by color """


# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-r", "--record", type=bool,
                default=False, nargs="?",
	        help="record a video")
args = vars(ap.parse_args())


shape = (864,480)
sepShape = 10

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenlower = (38,50,50)
greenupper = (48,255,255)
bluelower = (100,50,50)
blueupper = (110,255,255)
redlower = (0,50,50)
redupper = (5,255,255)


camera = cv2.VideoCapture(1)
camera.set(3,shape[0])
camera.set(4,shape[1])

size = tuple(map(int,(camera.get(3),camera.get(4))))


if args["record"]:
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    movieSize = size[0]*2 + sepShape,size[1]*2 + sepShape
    recorder = cv2.VideoWriter('simulation.avi',fourcc,20.0,movieSize)



def findRobot(lower,upper,hsv):
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

    hsvInRange = cv2.bitwise_and(hsv,hsv,mask=inRange)
    bgrInRange = cv2.cvtColor(hsvInRange,cv2.COLOR_HSV2BGR)

    # only proceed if at least one contour was found
    if len(cnts) > 0:
	# find the largest contour in the mask, then use
	# it to compute the minimum enclosing circle and
	# centroid
	c = max(cnts, key=cv2.contourArea)
	((x, y), radius) = cv2.minEnclosingCircle(c)

	# draw the circle and centroid on the frame,
	# then update the list of tracked points
        if radius > 2:
            return ((int(x),int(y)),int(radius)),bgrInRange
        else:
            return None,bgrInRange
    else:
        return None,bgrInRange

def circleRobot(image,xy,radius):
    cv2.circle(image, xy, radius,
               (0, 255, 255), 2)
    cv2.circle(image, xy, 5, (0, 0, 255), -1)





# keep looping
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    if grabbed:

        # resize the frame, blur it, and convert it to the HSV
        # color space
        frame = imutils.resize(frame)

        blurred = cv2.GaussianBlur(frame, (11, 11), sigmaX=0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        greenCircle,greenInRange = findRobot(greenlower,greenupper,hsv)
        blueCircle,blueInRange = findRobot(bluelower,blueupper,hsv)
        redCircle,redInRange = findRobot(redlower,redupper,hsv)

        if greenCircle:
            circleRobot(frame,*greenCircle)
        if blueCircle:
            circleRobot(frame,*blueCircle)
        if redCircle:
            circleRobot(frame,*redCircle)

        vertSep = np.zeros((sepShape,shape[0],3),dtype=np.uint8)
        horrSep = np.zeros((shape[1],sepShape,3),dtype=np.uint8)
        middSep = np.zeros((sepShape,sepShape,3),dtype=np.uint8)


        vertSep += 100
        horrSep += 100
        middSep += 100


        top = np.concatenate((frame,vertSep,greenInRange),axis=0)
        mid = np.concatenate((horrSep,middSep,horrSep),axis=0)
        bot = np.concatenate((redInRange,vertSep,blueInRange),axis=0)
        combined = np.concatenate((top,mid,bot),axis=1)

        # show the frame to our screen
        cv2.imshow("combined",combined)
        key = cv2.waitKey(1) & 0xFF

        if args["record"]:
            recorder.write(combined)

        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break


# cleanup the camera and close any open windows
camera.release()

if args["record"]:
    recorder.release()

cv2.destroyAllWindows()
