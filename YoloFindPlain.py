import cv2
import numpy as np
weights='./res/yolov3.weights'
config='./res/yolov3.cfg'
classes='./res/coco.names'
image = cv2.imread("img/planes.jpg")
image = cv2.resize(image,(416,416))
width = image.shape[1]
height = image.shape[0]
scale = 0.00392
names = open(classes).read().splitlines()
net = cv2.dnn.readNet(weights, config)
blob = cv2.dnn.blobFromImage(image, scale,(416,416), True, crop=False)
get_blob = blob.reshape(blob.shape[2], blob.shape[3], blob.shape[1])
cv2.imshow('Blob', get_blob)
cv2.imshow("Original",image)
net.setInput(blob)
def get_output_layers(net):
   layer_names = net.getLayerNames()
   output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
   return output_layers
outs = net.forward(get_output_layers(net))

score_threshold = 0.5
nms_threshold = 0.4
cv2.namedWindow("setting")
def noth(n):
    pass
cv2.createTrackbar("v","setting",0,100,noth)
while True:
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
       for detection in out:
           scores = detection[5:]
           class_id = np.argmax(scores)
           confidence = scores[class_id]
           v = cv2.getTrackbarPos("v","setting")
           if confidence > 0.01:
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

    for i in indices:
       #i = i[0]
       box = boxes[i]

       x = int(box[0])
       y = int(box[1])
       w = int(box[2])
       h = int(box[3])
       cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,0),2)


    cv2.imshow("setting", image)
    cv2.waitKey(1)
