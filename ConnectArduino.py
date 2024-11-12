import cv2, serial
uno = serial.Serial("COM6",9600,timeout=0.1)
cam = cv2.VideoCapture(0)
cascade_haar = cv2.CascadeClassifier("cascad/haarcascade_frontalface_default.xml")
while True:
    frame = cam.read()[1]
    print(frame.shape)

    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = cascade_haar.detectMultiScale(gray_frame,1.3,5,1,(20,20))
    if len(faces)==1:
        (x,y,w,h) = faces[0]
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),1)
        cv2.circle(frame,(x+w//2,y+h//2),0,(0,0,0),10)
        cv2.putText(frame,f'x:{x+w//2} y:{y+h//2}',(x+w//2,y+h//2),2,1.3,(255,0,0),1)
        sendData = f"X{(x+w//2)//4}Y{(y+h//2)//3}"

        uno.write(sendData.encode())
        print(uno.readline().decode("UTF-8"))


    cv2.imshow("frame",frame)

    cv2.waitKey(1)