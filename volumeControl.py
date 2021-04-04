#import libraries
import cv2
import time
import numpy as np
import handTrackingModule as htm #import hand tracking module
import math

#import libraries for pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

########
wCam, hCam = 640, 480 #initialize the width and height of our camera

cap = cv2.VideoCapture('for.mp4') #read video
cap.set(3, wCam) #set the width of the video
cap.set(4, hCam) #set the height of the video
pTime = 0 #initialize the previous time to zero

detector = htm.handDetector(detectionCon=0.8) #load the hand detector function and change the detection confidence to 0.8 to make things smoother

#code for pycaw library to help us change the button
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange() #get our volume range
minVol = volRange[0] #get our minimum volume
maxVol = volRange[1] #get our maximum volume
vol = 0
volBar = 400
volPer = 0



while True:
    success, img = cap.read()
    img = detector.findHands(img) #find the hand in the image and save it in the image variable
    lmList = detector.findPosition(img, draw = False) #get the position of the landmarks

    #make sure there are some points
    if len(lmList) != 0:
        #print(lmList[4], lmList[8]) #this prints just the 4th and 8th desired landmark

        x1, y1 = lmList[4][1], lmList[4][2] #sets the x and y position of the landmarks
        x2, y2 = lmList[8][1], lmList[8][2]  # sets the x and y position of the landmarks
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2 #gets the center between the two landmarks

        #draw circle on the desired landmark
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3) #draw a line betweem the two desired landmarks
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)#get the center of the drawn line

        length = math.hypot(x2-x1, y2-y1) #find the length of the line
        #print(length)

        # HAND RANGE 50 - 300
        # VOLUME RANGE -65 -0

        # Now we need to convert hand range into volume range
        vol = np.interp(length,[50,300],[minVol, maxVol]) #this converts the hand range to volume range
        volBar = np.interp(length,[50,300],[400, 150]) #change the range for our volume bar to be within the frame
        volPer = np.interp(length, [50, 300], [0, 100]) #set the percentage volume

        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)  # sets the master volume level as our volume

        #if length is the less than 50 we want to change the color of center circle
        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3) #create a rectangle
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED) #fill the rectangle with the volume bar
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 250, 0), 2) #Add percentage

    #write the frame rate
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2) #put text on the image


    cv2.imshow("img", img)
    cv2.waitKey(1)