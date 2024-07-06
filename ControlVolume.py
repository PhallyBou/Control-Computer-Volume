import time
import cv2
import mediapipe as mp
import os
import pyautogui

cap = cv2.VideoCapture(0)


mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

folderPath = 'Fingers'
myList = os.listdir(folderPath)
print(myList)

for imPath in myList:
    img = cv2.imread(f'{folderPath}/{imPath}')


tipIds = [4, 8, 12, 16, 20]

pTime = 0
cTime = 0

prevFingers = 0

while True:
    success, img = cap.read()



    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)
    
    

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            index_finger_0  = handLms.landmark[mpHands.HandLandmark. WRIST].yz
            index_finger_1  = handLms.landmark[mpHands.HandLandmark.THUMB_CMC].y
            index_finger_8  = handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].y
            index_finger_2  = handLms.landmark[mpHands.HandLandmark.THUMB_MCP].x  
            index_finger_6  = handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_PIP].x
            index_finger_3  = handLms.landmark[mpHands.HandLandmark.THUMB_IP].y
            index_finger_7  = handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_DIP].y
            index_finger_4  = handLms.landmark[mpHands.HandLandmark.THUMB_TIP].y
            index_finger_5  = handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_MCP].y
            index_finger_9  = handLms.landmark[mpHands.HandLandmark.MIDDLE_FINGER_MCP].y
            index_finger_10 = handLms.landmark[mpHands.HandLandmark.MIDDLE_FINGER_PIP].y
            index_finger_11 = handLms.landmark[mpHands.HandLandmark.MIDDLE_FINGER_DIP].y
            index_finger_12 = handLms.landmark[mpHands.HandLandmark.MIDDLE_FINGER_TIP].y
            index_finger_13 = handLms.landmark[mpHands.HandLandmark.RING_FINGER_MCP].y
            index_finger_14 = handLms.landmark[mpHands.HandLandmark.RING_FINGER_PIP].y
            index_finger_15 = handLms.landmark[mpHands.HandLandmark.RING_FINGER_DIP].y
            index_finger_16 = handLms.landmark[mpHands.HandLandmark.RING_FINGER_TIP].y
            index_finger_17 = handLms.landmark[mpHands.HandLandmark.PINKY_MCP].y
            index_finger_18 = handLms.landmark[mpHands.HandLandmark.PINKY_PIP].y
            index_finger_19 = handLms.landmark[mpHands.HandLandmark.PINKY_DIP].y
            index_finger_20 = handLms.landmark[mpHands.HandLandmark.PINKY_TIP].y

            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                # print(id, cx, cy)
                if id == 0:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            
    
        if len(results.multi_hand_landmarks) != 0:
            hand_gesture = ''
            fingers = []
            
            ##Thumb
            if results.multi_hand_landmarks[0].landmark[tipIds[0]].y < results.multi_hand_landmarks[0].landmark[tipIds[0]-1].y: 
                fingers.append(1)
            else:
                fingers.append(0)


            for id in range(1,5):
                if results.multi_hand_landmarks[0].landmark[tipIds[id]].y < results.multi_hand_landmarks[0].landmark[tipIds[id]-2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)


            totalFingers = 0
            for finger in fingers[1:]:
                if finger == 1:
                    totalFingers += 1

            print(totalFingers)        



            ##function run commands shortcuts
        
            if totalFingers == 1:

                if index_finger_8 > index_finger_4:    
                    hand_gesture = 'pointing down'

                if hand_gesture == 'pointing down':
                    pyautogui.press('volumedown')        
                cv2.putText(img, '1 volume down', (50, 60), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

            if totalFingers == 2:
                if index_finger_8 < index_finger_4:
                    hand_gesture = 'pointing up'

                if hand_gesture == 'pointing up':
                    pyautogui.press('volumeup')

                cv2.putText(img, '2 volume up', (50, 60), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    
                    
            if totalFingers == 3 and prevFingers != 3:
                pyautogui.hotkey('f')
                cv2.putText(img, '3 Full Screen', (50, 60), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)
   

            if totalFingers == 4 and prevFingers != 4:
                pyautogui.hotkey('k')
                cv2.putText(img, '5 Pause', (50, 60), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

                
        prevFingers = totalFingers
                
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime


    cv2.putText(img, str(int(fps)), (500, 65), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imshow("ITEG7", img)
    cv2.waitKey(1)