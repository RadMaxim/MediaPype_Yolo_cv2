import cv2
cam = cv2.VideoCapture(0)
cv2.namedWindow("setting")
def noth(n):
    pass
cv2.createTrackbar("hh", "setting", 0, 255, noth)
cv2.createTrackbar("sh", "setting", 0, 255, noth)
cv2.createTrackbar("vh", "setting", 0, 255, noth)
cv2.createTrackbar("hl", "setting", 0, 255, noth)
cv2.createTrackbar("sl", "setting", 0, 255, noth)
cv2.createTrackbar("vl", "setting", 0, 255, noth)
cv2.createTrackbar("sMin", "setting", 0, 10000, noth)
cv2.createTrackbar("mode", "setting", 0, 1, noth)

searchHighHSV = (108, 255, 255)
searchLowHSV = (0, 120, 125)
while True:
    hh = cv2.getTrackbarPos("hh", "setting")
    sh = cv2.getTrackbarPos("sh", "setting")
    vh = cv2.getTrackbarPos("vh", "setting")
    hl = cv2.getTrackbarPos("hl", "setting")
    sl = cv2.getTrackbarPos("sl", "setting")
    vl = cv2.getTrackbarPos("vl", "setting")
    sMin = cv2.getTrackbarPos("sMin", "setting")
    mode = cv2.getTrackbarPos("mode", "setting")
    img = cam.read()[1]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv_min = (hh, sh, vh)
    hsv_max = (hl, sl, vl)
    thresh = cv2.inRange( hsv, searchLowHSV, searchHighHSV )
    contour,hierarchy =cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for cont in contour:
        s = cv2.contourArea(cont)
        if s > sMin:
            if mode==0:
                cv2.drawContours(img, [cont], -1, (255, 0, 0), 4)
            if mode==1:
                cv2.drawContours(img, [cont], -1, (255, 0, 0), -1)
    cv2.imshow("img",img)
    cv2.imshow("mask",thresh)
    cv2.waitKey(1)