import cv2
import time
cap = cv2.VideoCapture(0)
videoSave = cv2.VideoCapture("./video/manyPeople.mp4")
face = cv2.CascadeClassifier("cascad/haarcascade_frontalface_default.xml")
eye = cv2.CascadeClassifier("cascad/haarcascade_eye.xml")
from playsound import playsound
def task1():
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
# task1()

def task2():
    no_eyes_timer = 0
    no_eyes_threshold = 4  # seconds
    while True:

        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = eye.detectMultiScale(gray, 1.3, 10, 0, (10, 10))
        if len(eyes) == 0:
            no_eyes_timer += 1
            if no_eyes_timer >= no_eyes_threshold * 10:  # check every 0.1 second
                playsound("audio/87f6a412389aba1.mp3")
                no_eyes_timer = 0  # reset the timer
        for (x, y, w, h) in eyes:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
        cv2.imshow('img', frame)
        cv2.waitKey(1)
# task2()
def task3():
    global videoSave
    while True:
       ret, frame = videoSave.read()
       if not ret:  # Check if the video has ended
           print("Video ended. Restarting...")
           videoSave.release()  # Release the current video capture object
           videoSave = cv2.VideoCapture("./video/manyPeople.mp4")  # Restart the video
           continue  # Go to the next iteration of the loop

       gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
       faces = face.detectMultiScale(gray, 1.3, 3, 0, (30, 30))
       for (x, y, w, h) in faces:
           length = 70*360/(h*0.26458)
           cv2.putText(frame, "distance  - "+str(round(length)),(x-30,y+h+20),1,1,(255,0,0),2)
           if length<340:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 4)
           else:
               cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)

       cv2.imshow('img', frame)
       cv2.waitKey(1)
task3()