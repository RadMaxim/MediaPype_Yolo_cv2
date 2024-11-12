import cv2
import numpy as np
weights = './res/yolov3.weights'

config = './res/yolov3.cfg'
classes = './res/coco.names'
# подключение настроек для нейронной сети
net = cv2.dnn.readNet(weights, config)
# считываем строки с файла и преобразуем его в массив
classes = open(classes).read().splitlines()
# cv2.namedWindow("setting")
# def noth(p):
#     pass
# cv2.createTrackbar("hl", "setting",0,255,noth)
# cv2.createTrackbar("sl", "setting",0,255,noth)
# cv2.createTrackbar("vl", "setting",0,255,noth)
# cv2.createTrackbar("hh", "setting",0,255,noth)
# cv2.createTrackbar("sh", "setting",0,255,noth)
# cv2.createTrackbar("vh", "setting",0,255,noth)
# cv2.createTrackbar("minG", "setting",0,255,noth)
# cv2.createTrackbar("maxG", "setting",0,255,noth)
# cap = cv2.VideoCapture('http://192.168.0.105:81/stream')
cap = cv2.VideoCapture("video/test3.mp4")
font = cv2.FONT_HERSHEY_PLAIN
# cap = cv2.imread("")
(frame_height, frame_width, frame_deep) = cap.read()[1].shape
#генерация рондомных чисел 100 кортежей размером 3 в диапазоне от 0 до 255
colors = np.random.uniform(0, 255, size=(100, 3))

lower_red1 = (0, 100, 100)
# print(lower_red1)
upper_red1 = (10, 255, 255)
lower_red2 = (160, 100, 100)
upper_red2 = (180, 255, 255)
lower_green = (40, 50, 50)
upper_green = (90, 255, 255)
lower_yellow = (15, 100, 100)
upper_yellow = (35, 255, 255)

# lower_yellow = np.array([15, 150, 150])
# upper_yellow = np.array([35, 255, 255])

prev_color = ''


def auto_steering(traffic_color):
    if traffic_color == 'RED':
        action = 'STOP'
    elif traffic_color == 'YELLOW':
        action = 'SLOW_SPEED'
    elif traffic_color == 'GREEN':
        action = 'NORMAL_SPEED'
    else:
        action = 'SLOW_SPEED'
    print(traffic_color, action)


def detect_circles(img):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    maskg = cv2.inRange(hsv, lower_green, upper_green)
    masky = cv2.inRange(hsv, lower_yellow, upper_yellow)
    maskr = cv2.add(mask1, mask2)
    size = img.shape


    r_circles = cv2.HoughCircles(maskr, cv2.HOUGH_GRADIENT, 1, 80, param1=50, param2=10, minRadius=0, maxRadius=30)
    g_circles = cv2.HoughCircles(maskg, cv2.HOUGH_GRADIENT, 1, 60, param1=50, param2=10, minRadius=0, maxRadius=30)
    y_circles = cv2.HoughCircles(masky, cv2.HOUGH_GRADIENT, 1, 30, param1=50, param2=5, minRadius=0, maxRadius=30)
    bound = 0.4
    traffic_color = ''
    if r_circles is not None:
        r_circles = np.uint16(np.around(r_circles))
        for i in r_circles[0, :]:
            if i[0] > size[1] or i[1] > size[0] or i[1] > size[0] * bound:
                continue
            cv2.circle(img, (i[0], i[1]), i[2] + 10, (0, 255, 0), 2)
            cv2.circle(maskr, (i[0], i[1]), i[2] + 30, (255, 255, 255), 2)
            cv2.putText(img, 'RED', (i[0], i[1]), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
            traffic_color = 'RED'

    if y_circles is not None:
        y_circles = np.uint16(np.around(y_circles))
        for i in y_circles[0, :]:
            if i[0] > size[1] or i[1] > size[0] or i[1] > size[0] * bound:
                continue
            cv2.circle(img, (i[0], i[1]), i[2] + 10, (0, 255, 0), 2)
            cv2.circle(masky, (i[0], i[1]), i[2] + 30, (255, 255, 255), 2)
            cv2.putText(img, 'YELLOW', (i[0], i[1]), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
            traffic_color = 'YELLOW'

    if g_circles is not None:
        g_circles = np.uint16(np.around(g_circles))
        for i in g_circles[0, :]:
            if i[0] > size[1] or i[1] > size[0] or i[1] > size[0] * bound:
                continue
            cv2.circle(img, (i[0], i[1]), i[2] + 10, (0, 255, 0), 2)
            cv2.circle(maskg, (i[0], i[1]), i[2] + 30, (255, 255, 255), 2)
            cv2.putText(img, 'GREEN', (i[0], i[1]), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
            traffic_color = 'GREEN'
    return img, traffic_color

def detectObject(layerOutputs):
    global prev_color
    boxes = []
    confidences = []
    class_ids = []
    for output in layerOutputs:
        for detection in output:
            scores = detection[5:] # у нас всего 80 объектов, мы находим максимальную вероятность в виде индекса
            class_id = np.argmax(scores)

            confidence = scores[class_id]
            if confidence > 0.2 and class_id==9:
                center_x = int(detection[0] * frame_width)
                center_y = int(detection[1] * frame_height)
                w = int(detection[2] * frame_width)
                h = int(detection[3] * frame_height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)
    #подавления немаксимумов к набору прямоугольников для удаления дублирующихся и перекрывающихся областей обнаружения объектов.

    indexes = cv2.dnn.NMSBoxes(boxes, confidences,score_threshold=0.1, nms_threshold=0.1)
    # кортеж из координат, ширины и высоты, вероятности соответствующих прямоугольников,
    #score_threshold Пороговое значение для уверенности (вероятности), выше которого прямоугольники будут рассматриваться в качестве действительных областей обнаружения.
    #nms_threshold Пороговое значение для применения алгоритма Non-Maximum Suppression, который удаляет дублирующиеся области с уверенностью ниже порога.
    if len(indexes) > 0:
        for i in indexes:
            x, y, w, h = boxes[i]
            crop = frame[y:y + h, x: x + w]
            frame_with_light, color_light = detect_circles(crop)

            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i], 2))
            color = colors[i]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 5)
            cv2.putText(frame, label + " " + confidence, (x, y + 20), font, 1, (255, 255, 255), 2)

            if color_light != prev_color:
                auto_steering(color_light)
            prev_color = color_light

            cv2.imshow(f'Crop', crop)

while True:
    # hl = cv2.getTrackbarPos("hl","setting")
    # sl = cv2.getTrackbarPos("sl","setting")
    # vl = cv2.getTrackbarPos("vl","setting")
    # hh = cv2.getTrackbarPos("hh","setting")
    # sh = cv2.getTrackbarPos("sh","setting")
    # vh = cv2.getTrackbarPos("vh","setting")
    # minG = cv2.getTrackbarPos("minG","setting")
    # maxG = cv2.getTrackbarPos("maxG","setting")
    # if minG%2==0:
    #     minG+=1
    # if maxG%2==0:
    #     maxG+=1
    frame = cap.read()[1]
    # frame = cv2.imread("img/traffic-light-876047.jpg")
    # формирование входных данных для нейронной сети
    blob = cv2.dnn.blobFromImage(frame, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
    # загружаем обработанные данные в нейронную сеть
    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    # обработанные данные
    layerOutputs = net.forward(output_layers_names)
    detectObject(layerOutputs=layerOutputs)
    frame = cv2.resize(frame,(900,500))
    cv2.imshow('Traffic light', frame)
    cv2.waitKey(1)


