import cv2
import mediapipe as mp
import time
import pyautogui

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

prev_x=0
gesture_cooldown=1
last_gesture_time=time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Unable to open webcam")
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    lmList = []
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

            fingers = []
            fingers.append(1 if lmList[4][1]>lmList[3][1] else 0)
            for tip in [8,12,16,20]:
                fingers.append(1 if lmList[tip][2]<lmList[tip-2][2] else 0)
            total_fingers=fingers.count(1)
            curr_x=lmList[0][1]
            diff_x=curr_x-prev_x

            if time.time()-last_gesture_time>gesture_cooldown:
                if diff_x>50:
                    pyautogui.press("right")
                    print("Swipe Right")
                    last_gesture_time=time.time()
                elif diff_x<-50:
                    pyautogui.press("left")
                    print("Swipe left")
                    last_gesture_time=time.time()
                elif total_fingers==1:
                    pyautogui.press("up")
                    print("jump")
                    last_gesture_time=time.time()
                elif total_fingers==0:
                    pyautogui.press("space")
                    print("Pause")
                    last_gesture_time=time.time()
                elif total_fingers==2:
                    pyautogui.press("down")
                    print("Crouch")
                    last_gesture_time=time.time()
            prev_x=curr_x
    cv2.imshow("Swipe & Gesture Controller",frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()