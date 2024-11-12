import threading

import cv2
import numpy as np

cam = cv2.VideoCapture("video/peopless.mp4")
weights = './res/yolov2-tiny.weights'

config = './res/yolov2-tiny.cfg'
classes = './res/coco.names'
# image = cv2.imread(image)
width = cam.read()[1].shape[1]
height = cam.read()[1].shape[0]
# нормализуются (превращение значений пикселей в диапазон от 0 до 1)
# перед прохождением через сеть. Таким образом, значение шкалы 0,00392 – это не что иное,
# как 1/255. Деление каждого значения пикселя на 255 (что эквивалентно умножению на 0,00392) приводит их в диапазон от 0 до 1.

scale = 0.00392
# список всех имен в списке
names = open(classes).read().splitlines()

score_threshold = 0.5
nms_threshold = 0.4

# загрузить данные нейросети с параметрами настройки
# Функция cv2.dnn.readNet в библиотеке OpenCV (cv2)
# для Python используется для загрузки предварительно обученной нейронной сети
# (DNN) из внешнего файла на диске. Это позволяет загружать модели нейронной сети,
# которые были обучены на больших наборах данных для решения различных задач компьютерного зрения,
# таких как детекция объектов, сегментация, классификация и другие.
net = cv2.dnn.readNet(weights, config)


# Формируем блоб для нейросети со следующими параметрами
# Функция cv2.dnn.blobFromImage в OpenCV (cv2) в Python используется для предварительной обработки изображений перед их передачей
# через глубокую нейронную сеть (DNN). Эта функция помогает создавать блоб (бинарный большой объект) из изображения, чтобы сделать
# его подходящим для ввода в нейронную сеть.
# size - входной размер для изображения, которое получит нейросеть, теперь доступны размеры 224×224, 227×227, 299×299, 416х416
# mean – булевой параметр, указывающий нужно ли делать разницу R и B каналов (зависит от обученной модели)
# crop – булевой параметр, указывающий нужно ли изменять размер входного изображения или его обрезать для создания блоба
# def get_output_layers(net):
#     # используется для получения списка имен всех слоев(layers)
#     # в предварительно загруженной нейронной сети
#     layer_names = net.getLayerNames()
#     # print(layer_names)
#     output_layers = []
#
#     # выходные слои, через которые происходит получение финальных выходных данных нейронной сети.
#     for i in net.getUnconnectedOutLayers():
#         output_layers.append(layer_names[i - 1])
#     return output_layers

#
# def draw_prediction(img, class_id, confidence, x, y, x1, y1):
#     label = str(names[class_id])
#     cv2.rectangle(img, (x, y), (x1, y1), (255, 0, 0), 2)
#     cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)


while True:
    boxes = []
    class_ids = []
    confidences = []
    frame = cam.read()[1]
    cv2.resize(frame, (416, 416))
    blob = cv2.dnn.blobFromImage(frame, scale, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    getName = net.getUnconnectedOutLayersNames()
    # Этот метод запускает процесс передачи входных данных через сеть, обработку данных
    # слоями нейронной сети и получение выходных результатов.
    outs = net.forward(getName)

    for out in outs:
        for detection in out:

            scores = detection[5:]
            print(scores)
            # используется для поиска индекса элемента
            # с наибольшим значением в массиве
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])
        indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold, nms_threshold)
        # Функция cv2.dnn.NMSBoxes  библиотеке OpenCV(cv2) для Python используется для
        # применения алгоритма подавления немаксимумов(Non - Maximum Suppression, NMS) к  обнаруженным
        # объектам для удаления дубликато и повторяющихся прямоугольников, оставляя только
        # наиболее уверенные(наиболее вероятные) области обнаружения.
        if len(boxes) > 0:
            for i in indices:
                label = str(names[class_ids[i]])

                [x, y, w, h] = boxes[i]
                x = int(x)
                y = int(y)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                # cv2.putText(frame,"wef",(x,y),1,)
                cv2.putText(frame, str(label) + ": " + str(round(confidences[i] * 100)) + "%", (x, y + 30), 1, 1.0,
                            (255, 255, 255), 2)

    cv2.imshow("Original", frame)
    cv2.waitKey(1)
# cv2.waitKey(0)


#
#
# cv2.imshow("object detection", image)
# cv2.waitKey(0)
