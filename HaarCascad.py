import cv2
cap = cv2.VideoCapture(0)
face = cv2.CascadeClassifier("cascad/haarcascade_frontalface_default.xml")

while True:
   _, frame = cap.read()
   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   faces = face.detectMultiScale(gray, 1.3, 3, 0, (30, 30))
   for (x, y, w, h) in faces:
       length = 70*360/(h*0.26458)
       cv2.putText(frame, "distance  - "+str(round(length)),(x-30,y-20),1,2,(255,0,0),3)
       if length<340:
            cv2.putText(frame, "ruin your eyesight", (x, y +h+ 30), 1, 2, (0, 0, 255), 3)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 4)
       else:
           cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
   cv2.imshow('img', frame)
   cv2.waitKey(1)

# 2150 примерный реальный размер моего лица
# 700 3600
# 350 7200