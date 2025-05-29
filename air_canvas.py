import cv2
import mediapipe as mp
import numpy as np

cap=cv2.VideoCapture(0)
mpHands=mp.solutions.hands
hands=mpHands.Hands(max_num_hands=1)
mpDraw=mp.solutions.drawing_utils
canvas=np.zeros((480,640,3),dtype=np.uint8)
colors=[(255,0,0),(0,255,0),(0,0,255),(0,0,0)]
color_names=["Blue","Green","Red","Eraser"]
color=colors[0]
brush_thickness=7
eraser_thickness=30

xp,yp=0,0

def get_fingers(lms):
    tips=[4,8,12,16,20]
    up=[]
    up.append(1 if lms[tips[0]][0]<lms[tips[0]-1][0] else 0)
    for i in range(1,5):
        up.append(1 if lms[tips[i]][1]<lms[tips[i]-2][1] else 0)
    return up

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    for i in range(len(colors)):
        cv2.rectangle(frame,(i*160,0),((i+1)*160,50),colors[i],-1)
        cv2.putText(frame,color_names[i],(i*160+10,40),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,255,255),2)


    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)
            lms=[]
            h,w,_=frame.shape
            for lm in handLms.landmark:
                lms.append((int(lm.x*w),int(lm.y*h)))
                if lms and len(lms)>=21:
                    fingers=get_fingers(lms)
                    x1,y1=lms[8]
                    if fingers==[0,1,0,0,0]:
                        if xp==0 and yp==0:
                            xp,yp=x1,y1
                        cv2.line(canvas,(xp,yp),(x1,y1),color,brush_thickness)
                        xp,yp=x1,y1
                    elif sum(fingers)==2 and fingers[1]==1 and fingers[2]==1:
                        color=colors[(colors.index(color)+1)%len(colors)]
                        xp,yp=0,0
                    elif sum(fingers)==5:
                        cv2.circle(canvas,(x1,y1),eraser_thickness,(0,0,0),-1)
                        xp,yp=0,0
                    else:
                        xp,yp=0,0
    else:
        xp,yp=0,0
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)  
    _, inv = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)  

    frame=cv2.bitwise_and(frame,inv)
    frame=cv2.bitwise_or(frame,canvas)
    cv2.imshow("Air Canvas",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()