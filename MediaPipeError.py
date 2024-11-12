

import cv2
import mediapipe as mp
import numpy as np
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

mpDraw = mp.solutions.drawing_utils
drawStyles = mp.solutions.drawing_styles
drawSpec = mp.solutions.drawing_utils.DrawingSpec(thickness=1, circle_radius=1)

mpHandsMash = mp.solutions.hands
handsMash = mpHandsMash.Hands()
fingerPoints = [8, 12, 16, 20, 4]

imgCanvas = np.zeros((720, 1280, 3), np.uint8)
xp, yp = 0, 0

RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

currentColor = WHITE


def detector(image, draw=False):
   rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
   results = handsMash.process(rgb)
   h, w, d = image.shape
   landmarks = {}
   if results.multi_hand_landmarks:
       for hands in results.multi_hand_landmarks:
           if draw:
               mpDraw.draw_landmarks(frame, hands, mpHandsMash.HAND_CONNECTIONS,
                                     drawStyles.get_default_hand_landmarks_style(),
                                     drawStyles.get_default_hand_connections_style())
           for ids, lm in enumerate(hands.landmark):
               landmarks[ids] = (ids, int(lm.x * w), int(lm.y * h))
               cv2.putText(image, str(ids), (landmarks[ids][1], landmarks[ids][2]), cv2.FONT_HERSHEY_PLAIN, 1,
                           (255, 0, 255), 2)
   return landmarks


def fingersUp(lm):
   fingers = []
   if lm[fingerPoints[4]][1] > lm[fingerPoints[4] - 1][1]:
       fingers.append(1)
   else:
       fingers.append(0)
   for i in range(0, 4):
       if lm[fingerPoints[i]][2] < lm[fingerPoints[i] - 1][2]:
           fingers.append(1)
       else:
           fingers.append(0)
   total = fingers.count(1)
   return fingers, total


while True:
   frame = cap.read()[1]
   frame = cv2.flip(frame, 1)
   landmarks = detector(frame, draw=True)

   # print(len(landmarks))
   if len(landmarks) != 0:
       ids1, x1, y1 = landmarks[8]
       ids2, x2, y2 = landmarks[12]
       fingersList, up_fingers = fingersUp(landmarks)
       print(fingersList)
       if fingersList[1] and not (fingersList[2]):
           if xp == 0 and yp == 0:
               xp, yp = x1, y1
           cv2.circle(frame, (x1, y1), 15, currentColor, cv2.FILLED)
           if currentColor == BLACK:
               cv2.line(imgCanvas, (xp, yp), (x1, y1), currentColor, 60)
           else:
               cv2.line(imgCanvas, (xp, yp), (x1, y1), currentColor, 10)
           xp, yp = x1, y1
           print("Drawing Mode")
       if fingersList[1] and fingersList[2]:
           cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 4)
           xp, yp = 0, 0
           print("Selection Mode")
           if y1 < 125:
               if 110 < x1 < 350:
                   cv2.rectangle(frame, (185, 11), (300, 115), WHITE, 2)
                   currentColor = RED
               if 360 < x1 < 650:
                   cv2.rectangle(frame, (435, 11), (550, 115), WHITE, 2)
                   currentColor = GREEN
               if 660 < x1 < 900:
                   cv2.rectangle(frame, (685, 11), (800, 115), WHITE, 2)
                   currentColor = BLUE
               if 915 < x1 < 1140:
                   cv2.rectangle(frame, (935, 11), (1050, 115), WHITE, 2)
                   currentColor = WHITE
               if 1130 < x1 < 1280:
                   cv2.rectangle(frame, (1140, 5), (1256, 120), WHITE, 2)
                   currentColor = BLACK
       cv2.putText(frame, str(up_fingers), (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2)

   if cv2.waitKey(1) == ord("r"):
       imgCanvas = np.zeros((720, 1280, 3), np.uint8)

   canvasGrey = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
   ret, threshold = cv2.threshold(canvasGrey, 50, 255, cv2.THRESH_BINARY_INV)
   canvasBGR = cv2.cvtColor(threshold, cv2.COLOR_GRAY2BGR)
   frame = cv2.bitwise_and(frame, canvasBGR)
   frame = cv2.bitwise_or(frame, imgCanvas)

   cv2.imshow("frame", frame)
   cv2.imshow("Canvas", imgCanvas)
   if cv2.waitKey(1) == 27:
       break

cap.release()
cv2.destroyAllWindows()

