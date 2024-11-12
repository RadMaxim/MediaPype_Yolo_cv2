import  cv2
cap = cv2.VideoCapture("./video/cars3.mp4")
cv2.namedWindow("setting")
def noth(n):
    pass
cv2.createTrackbar("blur","setting",0,100, noth)
cv2.createTrackbar("blur_1","setting",0,100, noth)
cv2.createTrackbar("cannyMin","setting",0,255, noth)
cv2.createTrackbar("cannyMax","setting",0,255, noth)
cv2.createTrackbar("eps","setting",0,1000, noth)
cv2.createTrackbar("minT","setting",0,255,noth)
cv2.createTrackbar("maxT","setting",0,255,noth)

while True:
    ret, frame = cap.read()

    minT = cv2.getTrackbarPos("minT", "setting")
    maxT = cv2.getTrackbarPos("maxT", "setting")
    road_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(road_gray,229,255,0)

    blurXY = cv2.getTrackbarPos("blur","setting")
    minC = cv2.getTrackbarPos("cannyMin","setting")
    maxC = cv2.getTrackbarPos("cannyMax","setting")
    epsV = cv2.getTrackbarPos("eps","setting")
    if blurXY%2==0:
        blurXY+=1
    blur_1 = cv2.getTrackbarPos("blur_1","setting")
    blur = cv2.GaussianBlur(frame,(7,7),0)
    canny = cv2.Canny(blur,99,255)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (51, 1))
    closed = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)

    contours , _ = cv2.findContours(closed,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    squares =[]
    obj = {}
    for cont in contours:
        s = cv2.contourArea(cont)
        (x,y,w,h)= cv2.boundingRect(cont)
        obj[s]=(w,h,x,y)
        if w<h*5 and s>30:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.putText(frame, f"car", (x, y), 1, 1.1, (0, 0, 0), 3)
        squares.append(s)
        eps = (1/(200+1))*cv2.arcLength(cont,True)
        approx = cv2.approxPolyDP(cont,eps,True)
    if not ret:
        break
    cv2.imshow("setting1",frame)
    cv2.waitKey(1)



