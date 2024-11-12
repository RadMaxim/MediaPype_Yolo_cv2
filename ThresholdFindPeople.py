import cv2
cv2.namedWindow("setting")
def noth(n):
    pass
cv2.createTrackbar("minV", "setting", 0, 255, noth)
cv2.createTrackbar("maxV", "setting", 0, 255, noth)
while True:
    minV = cv2.getTrackbarPos("minV", "setting")
    maxV = cv2.getTrackbarPos("maxV", "setting")
    img = cv2.imread("./img/people1.jfif")
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    h, th = cv2.threshold(gray_img, minV, maxV, 1)
    contours,_ = cv2.findContours(th,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
            (x,y,w,h)=cv2.boundingRect(contour)
            cv2.rectangle(img,(x,y),(x+w,y+h),color=(0,0,255),thickness=2)
    cv2.imshow("setting", th)
    cv2.imshow("people", img)
    cv2.waitKey(1)
