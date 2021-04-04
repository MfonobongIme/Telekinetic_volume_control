#import libraries

import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode = False, maxHands = 2, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode #creates an object, and the object will have its own variable
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        #create object from our class hands
        self.mpHands = mp.solutions.hands #formailty before using mediapipe model
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon) #create hands object

        self.mpDraw = mp.solutions.drawing_utils #helps us draw the points on the hands

    def findHands(self, img, draw = True): #detect hands



        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #convert to rgb because the object only uses rgb images
        self.results = self.hands.process(imgRGB) #processes the frame for us and gives us the result
        #print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks: #if true,we go in
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS) #draws the landmarks and connects them together

        return img #return image if we have drawn on it

    def findPosition(self, img, handNo = 0, draw = True): #find position of landmark

        lmList = [] #this list will have all the landmarks list
        if self.results.multi_hand_landmarks:  # if true,we go in
            myHand = self.results.multi_hand_landmarks[handNo] #gets the hand

            # find id and landmark inside myhand.landmark
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape  # get the height, width and center of image
                cx, cy = int(lm.x * w), int(lm.y * h)  # multiply landmark position with img
                #print(id, cx, cy)  # prints the id number of the landmark and its positions
                lmList.append([id, cx, cy]) #append the values of the landmark position into lmList
                #if id == 4:  # the first landmark
                if draw: #if draw is True....
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)  # draw circle on the specified landmark

        return lmList

def main():
    pTime = 0  # previous time
    cTime = 0  # current time

    cap = cv2.VideoCapture(0)
    detector = handDetector() #create detector object

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        findPosition(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])


        cTime = time.time()  # this will give us the current time
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3)

        cv2.imshow("image", img)
        cv2.waitKey(1)





if __name__ == "__main__":
    main()
