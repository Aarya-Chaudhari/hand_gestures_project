import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

tipIds = [4, 8, 12, 16, 20]

while True:
    ret, frame = cap.read()
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
    if len(lmList) != 0:
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:  
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        total_fingers = fingers.count(1)
        cv2.putText(frame, f'Fingers: {total_fingers}', (50, 100),
                    cv2.FONT_HERSHEY_COMPLEX, 2, (125, 243, 213), 3)

    cv2.imshow("Finger Count", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
