import  cv2

cam = cv2.VideoCapture("./video/faces.mp4")
faces_cascad = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")
oko_cascad = cv2.CascadeClassifier("./haarcascade_eye.xml")
while True:
    frame = cam.read()[1]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faces_cascad.detectMultiScale(gray, 1.3,3,0,(10,10))

    for face in faces:
        [x,y,w,h] = face
        cv2.rectangle(frame,(x,y),(x+w, y+h),(0,0,0),2)
    eyes = oko_cascad.detectMultiScale(gray, 1.3, 10, 0, (2,2))
    for eye in eyes:
        (x,y,w,h) = eye
        cv2.circle(frame, (x+w//2, y+h//2), 10, (200, 200, 200),-1)
    print(faces)

    cv2.imshow("frame", frame)
    # cv2.imshow("gray", gray)
    # print(frame)
    cv2.waitKey(5)