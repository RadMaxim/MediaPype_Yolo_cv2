import cv2
import numpy as np
video_cars = cv2.VideoCapture("video/cars_video.mp4")


# используется для загрузки предварительно обученной нейронной сети (DNN) из внешнего файла на диске.
# #подключили модель от yolo(веса-вероятность, конфигурация)
net = cv2.dnn.readNet('./res/yolov2-tiny.weights','./res/yolov2-tiny.cfg')
classes = [] #готовим список имен, на которая обучена сеть
with open("./res/coco.names") as allElement:# читаем содержимое файла
    for name in allElement: # пробегаемся по файлу, по строкам
        classes.append(name[:-1])
print(classes)
while True:
    imgPlane = video_cars.read()[1]#читаем картинку
    h, w,_ = imgPlane.shape # определили размер картинки
    imgPlane = cv2.resize(imgPlane,(416,416))
    blob = cv2.dnn.blobFromImage(imgPlane, (1/255),(416,416),(0,0,0),swapRB=True, crop=False)
    net.setInput(blob)#загружаем данные в нейронку
    search_names = net.getUnconnectedOutLayersNames()
    # print(search_names)
    search_output = net.forward(search_names)
    # print(search_output)
    boxes = []#создаем пустой массив для записи x, y, w, h
    conf = []
    idElem = []
    for output in search_output:
        # print(output)
        for detection in output:

            newDetection = detection[5:]
            class_id = np.argmax(newDetection)
            conf1 = newDetection[class_id]
            if conf1>0.2:
                centerX = int(detection[0]*416)
                centerY = int(detection[1]*416)
                w = int(detection[2]*416)
                h = int(detection[3]*416)
                boxes.append([centerX-w//2,centerY-h//2,w,h])
    for box in boxes:
        cv2.rectangle(imgPlane, (box[0], box[1]), ((box[0] + box[2]), (box[1] + box[3])), (0, 0, 0),1)
    cv2.imshow("frame",imgPlane)
    cv2.waitKey(1)