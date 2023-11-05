# import opencv
import cv2
import numpy as np
import mido 
import camFeatureExtractor as cfe
import midiGenerator as mg
import time
import imutils
from collections import deque
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

posList = []
def onMouse(event, x, y, flags, param):
   global posList
   if event == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
cv2.setMouseCallback('WindowName', onMouse)

#open a video from folder
cap = cv2.VideoCapture('/Users/silasoettinghaus/Downloads/Bildschirmaufnahme 2023-11-04 um 23.46.13.MOV')
#pla this video
pts = deque(maxlen=args["buffer"])

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        
        greenLower = (29, 86, 6)
        greenUpper = (64, 255, 255)
        frame = cfe.isolateColor(frame,greenLower,greenUpper) 

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        

        center = None
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
            if radius > 1:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),(29, 86, 6), 2)
                cv2.circle(frame, center, 5, (29, 86, 6), -1)
	        # update the points queue
                cv2.drawContours(frame, [c], -1, (29, 86, 6), 2)

        pts.appendleft(center)

        cv2.imshow('frame',frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break


if 0:
    #or load a picture
    cap = cv2.imread('/Users/silasoettinghaus/Downloads/Bildschirmfoto 2023-11-04 um 22.34.47.png')
    cv2.imshow('iso frame',cap)
    cv2.setMouseCallback("iso frame", onMouse)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    time.sleep(1)

    posNp = np.array(posList)

    #get color in cap by position
    hsv = cv2.cvtColor(cap, cv2.COLOR_BGR2HSV)

    calibration_list = hsv[posNp[:,1],posNp[:,0]]

    #get column with highest standard deviation
    std = np.std(calibration_list,axis=0)

    #get position of smallest standard deviation
    max_std_pos = np.argmax(std)

    calibration_list = calibration_list[calibration_list[:,max_std_pos].argsort()]

    greenLower = (29, 86, 6)
    greenUpper = (64, 255, 255)

    # get row with smallest sum
    sum = np.sum(calibration_list,axis=1)

    #get position of smallest sum
    min_sum_pos = np.argmin(sum)
    max_sum_pos = np.argmax(sum)

    greenisolated = cfe.isolateColor(cap,calibration_list[min_sum_pos],calibration_list[max_sum_pos])

    myisolated = cfe.isolateColor(cap,greenLower,greenUpper)

    cv2.imshow('iso frame',greenisolated)
    cv2.waitKey(0)
    cv2.imshow('iso frame',myisolated)
    cv2.waitKey(0)

    # closing all open windows 
    cv2.destroyAllWindows() 

