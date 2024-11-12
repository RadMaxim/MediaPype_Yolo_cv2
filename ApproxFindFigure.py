import cv2
def noth(p):
    pass
cv2.namedWindow("setting")
cv2.createTrackbar("minS", "setting", 0, 1000, noth)
# cv2.createTrackbar("maxT", "setting", 0, 255, noth)
while True:
    minS = cv2.getTrackbarPos("minS", "setting")
    img = cv2.imread("./readmeImg/figure1.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        s = cv2.contourArea(cnt)
        if minS<s:
           epsilon=0.01 * cv2.arcLength(cnt, True)
           approx = cv2.approxPolyDP(cnt,epsilon, True)
           x=approx.ravel()[0]
           y=approx.ravel()[1]
           print(x)
           print(approx)
           cv2.drawContours(img, [approx], 0, (0, 0, 0), 3)
           if len(approx) == 3:
               cv2.putText(img, "Triangle", (x, y), 1, 1, (255,0,0),3)
           elif len(approx) == 4:
               cv2.putText(img, "Rectangle", (x, y), 1, 1,(255,0,0),3)
           elif len(approx) == 5:
               cv2.putText(img, "Pentagon", (x, y), 1, 1, (255,0,0),3)
           elif 6 < len(approx) < 15:
               cv2.putText(img, "Ellipse", (x, y), 1, 1, (255,0,0),3)
           else:
               cv2.putText(img,"Circle",(x, y), 1,1, (255,0,0),3)
    cv2.imshow("setting", img)
    cv2.waitKey(1)