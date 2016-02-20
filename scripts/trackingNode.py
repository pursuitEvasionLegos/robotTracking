""" The ROS Node for webcams used to track robots """

import rospy
import std_msgs
import cv2
import numpy as np




class TrackingNode(object):
    def __init__(self,name="tracking_node",hz=30):
        rospy.init_node(name,anonymous=False)

        self.pub = rospy.Publisher("locations",
                                   std_msgs.msg.String,
                                   queue_size=10)

        self.hz = hz
        self.rate = rospy.Rate(hz)

        self.shape_orig = (864,480)
        self.sepShape = 10

        ## colors to track
        self.greenlower = (38,50,50)
        self.greenupper = (48,255,255)
        self.bluelower = (100,50,50)
        self.blueupper = (110,255,255)
        self.redlower = (0,50,50)
        self.redupper = (5,255,255)



    def track(self):
        camera = cv2.VideoCapture(1)
        camera.set(3,self.shape_orig[0])
        camera.set(4,self.shape_orig[1])

        shape = tuple(map(int,(camera.get(3),camera.get(4))))

        greenCircle = blueCircle = redCircle = None


        done = False

        while not done:
            grabbed, frame = camera.read()

            if grabbed:
                blurred = cv2.GaussianBlur(frame,(11,11),sigmaX=0)
                hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

                greenCircle,greenInRange = self.findRobot(self.greenlower,
                                                          self.greenupper,
                                                          hsv)
                blueCircle,blueInRange = self.findRobot(self.bluelower,
                                                        self.blueupper,
                                                        hsv)
                redCircle,redInRange = self.findRobot(self.redlower,
                                                      self.redupper,
                                                      hsv)

                if greenCircle:
                    self.circleRobot(frame,*greenCircle)
                if blueCircle:
                    self.circleRobot(frame,*blueCircle)
                if redCircle:
                    self.circleRobot(frame,*redCircle)

                vertSep = np.zeros((self.sepShape,shape[0],3),
                                   dtype=np.uint8)
                horrSep = np.zeros((shape[1],self.sepShape,3),
                                   dtype=np.uint8)
                middSep = np.zeros((self.sepShape,self.sepShape,3),
                                   dtype=np.uint8)


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
            done = rospy.is_shutdown() or (key == ord("q"))

            msg = ("Circles: " + str(greenCircle)
                   + str(blueCircle) + str(redCircle))

            self.pub.publish(msg)

            self.rate.sleep()

        camera.release()
    cv2.destroyAllWindows()


    def findRobot(self,lower,upper,hsv):
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

    def circleRobot(self,image,xy,radius):
        cv2.circle(image, xy, radius,
                   (0, 255, 255), 2)
        cv2.circle(image, xy, 5, (0, 0, 255), -1)






if __name__ == "__main__":
    tn = TrackingNode()
    tn.track()
