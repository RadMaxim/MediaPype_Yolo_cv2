

import cv2
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

mpDraw = mp.solutions.drawing_utils
drawStyles = mp.solutions.drawing_styles
drawSpec = mp.solutions.drawing_utils.DrawingSpec(thickness=1, circle_radius=1)
(h,w,d) = cap.read()[1].shape
mpHandsMash = mp.solutions.hands
handsMash = mpHandsMash.Hands()
fingerPoints = [4,8,12,16,20]
xp,yp = 0,0
imgCanvas = np.zeros((480, 640, 3), np.uint8)

RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
colorsMode = [RED,GREEN,BLUE,WHITE,RED,GREEN,BLUE,WHITE]###############################
mode = 1###############################
currentColor = WHITE
modeColor = 0
def detector(img, draw=False):
   rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
   results = handsMash.process(rgb)
   h, w, d = img.shape
   hand_landmarks = {}
   if results.multi_hand_landmarks:
       for hands in results.multi_hand_landmarks:
           if draw:
               mpDraw.draw_landmarks(frame, hands, mpHandsMash.HAND_CONNECTIONS,
                                     drawStyles.get_default_hand_landmarks_style(),
                                     drawStyles.get_default_hand_connections_style())
           for ids, lm in enumerate(hands.landmark):
               hand_landmarks[ids] = (ids, int(lm.x * w), int(lm.y * h))
               cv2.putText(img, str(ids), (hand_landmarks[ids][1], hand_landmarks[ids][2]), cv2.FONT_HERSHEY_PLAIN, 1,
                           (255, 0, 255), 2)
   return hand_landmarks
#
def fingersUp(lm):
   fingers = []

   if lm[fingerPoints[0]][1] > lm[fingerPoints[0]-1][1]:

       fingers.append(0)
   else:
       fingers.append(1)
   for i in range(1, 5):
       if lm[fingerPoints[i]][2] < lm[fingerPoints[i] - 2][2]:
           fingers.append(1)
       else:
           fingers.append(0)
   total = fingers.count(1)
   return fingers,total
def modeDraw(frame, fingersList):
    global xp,yp,mode,colorsMode,modeColor
    if fingersList[1] and not (fingersList[2]):
        if xp == 0 and yp == 0:
            xp, yp = x1, y1
        cv2.line(imgCanvas, (xp, yp), (x1, y1), colorsMode[modeColor], 60)
        xp, yp = x1, y1
        print("Drawing Mode")
        mode=1
    elif fingersList[1] and fingersList[2] and fingersList[3] == 0:
        cv2.line(frame, (xp, yp), (x1, y1), (255, 0, 0), 60)
        xp, yp = x1, y1
        print("Selection Mode")
        mode=2
        detectionColor(x1,y1)
    elif fingersList[1] and fingersList[2] and fingersList[3]:
        cv2.line(imgCanvas, (x1, y1), (xp, yp), (0, 0, 0), 60)
        xp, yp = x1, y1
        print("Стерка")
        mode=3
    print(mode)
def drawColor(frame):
    global colorsMode
    hp = 100
    wr = w//8
    cv2.line(frame,(0,hp),(w,hp),(255,255,255),3)
    for i in range(len(colorsMode)):
        cv2.rectangle(frame, (wr*i, 0), (wr * (i+1), hp), colorsMode[i], -1)
def detectionColor(x,y):
    global colorsMode,w,modeColor
    wc = w//8
    if 0 < y < 100 and mode==2:
        for i in range(len(colorsMode)):
            if x>wc*i and x<wc*(i+1):
                modeColor=i
                print(modeColor)

while True:
   frame = cap.read()[1]
   frame = cv2.flip(frame, 1)
   landmarks = detector(frame, draw=True)
   drawColor(frame)
   if len(landmarks) != 0:
       ids1, x1, y1 = landmarks[8]
       ids2, x2, y2 = landmarks[12]
       fingersList, up_fingers = fingersUp(landmarks)
       modeDraw(frame,fingersList)


   canvasGray = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
   _,canvasGrayImg =cv2.threshold(canvasGray,50,255,2)

   cv2.imshow("imgCanvas", imgCanvas)
   cv2.imshow("frame", frame)
   if cv2.waitKey(1) == 27:
       break

