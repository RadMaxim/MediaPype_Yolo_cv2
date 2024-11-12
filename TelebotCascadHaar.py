import cv2
import numpy as np
import telebot

bot = telebot.TeleBot("6792660579:AAGLClvQcKzdQeitbzNJV-kiVAOf4RySwbo")
bot_id = 563747470  # узнаем id через бота
bot.send_message(bot_id, "hello")
cascade = cv2.CascadeClassifier("cascad/haarcascade_frontalface_default.xml")
cam = cv2.VideoCapture(0)
winName = "Movement"
cv2.namedWindow(winName)
frame = cam.read()[1]
prev_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
arr = [0, 0, 0, 0]
stateFace = False
stateMove = False


def diffImg(f1, f2):
    d1 = cv2.absdiff(f1, f2)
    d3 = np.ravel(d1)
    d4 = np.count_nonzero(d3)
    return d4, d1


def cascadMethod(frame, frame_gray):
    global arr
    global stateFace
    find_faces = cascade.detectMultiScale(frame_gray, 1.3, 5, 1, (40, 40))
    for face in find_faces:
        arr = [x, y, w, h] = face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 2)

        stateFace = True


while True:
    current_frame = cam.read()[1]
    current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    [prev_x, prev_y, prev_w, prev_h] = arr

    cascadMethod(current_frame, current_frame_gray)

    nonzero, result = diffImg(prev_frame, current_frame_gray)
    cv2.imwrite("img/move.jpg", current_frame)
    if nonzero > 270000:
        bot.send_photo(bot_id, open("img/move.jpg", 'rb'))
    print(nonzero)

    if prev_w - arr[2] > 15 and prev_h - arr[3] > 15:
        print("Дальше от компьютера")
    elif -prev_w + arr[2] > 15 and -prev_h + arr[3] > 15:
        print("Ближе к компьютеру")
    if prev_x - arr[0] > 15:
        print("Наклонился влево")
    if -prev_x + arr[0] > 15:
        print("Наклонился вправо")
    cv2.imshow(winName, result)
    cv2.imshow("frame", current_frame)
    cv2.waitKey(1)
    prev_frame = current_frame_gray
