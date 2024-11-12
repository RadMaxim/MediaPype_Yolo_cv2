import cv2
cam = cv2.VideoCapture(0)
cv2.namedWindow("frame")
def noth(n):
    pass
cv2.createTrackbar("hl","frame",0,255,noth)
cv2.createTrackbar("sl","frame",0,255,noth)
cv2.createTrackbar("vl","frame",0,255,noth)
cv2.createTrackbar("hh","frame",0,255,noth)
cv2.createTrackbar("sh","frame",0,255,noth)
cv2.createTrackbar("vh","frame",0,255,noth)
cv2.createTrackbar("square","frame",0,10000,noth)
while True:
    hl = cv2.getTrackbarPos("hl", "frame")
    sl = cv2.getTrackbarPos("sl", "frame")
    vl = cv2.getTrackbarPos("vl", "frame")
    hh = cv2.getTrackbarPos("hh", "frame")
    sh = cv2.getTrackbarPos("sh", "frame")
    vh = cv2.getTrackbarPos("vh", "frame")
    sq = cv2.getTrackbarPos("square", "frame")
    frame = cam.read()[1]
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    minV = (hl,sl,vl)
    maxV = (hh,sh,vh)
    mask = cv2.inRange(hsv,minV,maxV)
    contours, h = cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        epsilon = sq / 100000 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        cv2.drawContours(frame, [approx], -1, (255, 0, 0), 4)
    cv2.imshow("hsv",hsv)
    cv2.imshow("mask",mask)
    cv2.imshow("frame",frame)
    cv2.waitKey(1)
