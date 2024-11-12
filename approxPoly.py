import cv2

cv2.namedWindow("setting")
def noth(n):
    pass
def createTrack():
    cv2.createTrackbar("minV", "setting", 0, 255, noth)
    cv2.createTrackbar("maxV", "setting", 0, 255, noth)
    cv2.createTrackbar("s", "setting", 0, 1000, noth)
createTrack()
while True:
    minV = cv2.getTrackbarPos("minV", "setting")
    maxV = cv2.getTrackbarPos("maxV", "setting")
    sv = cv2.getTrackbarPos("s", "setting")
    img = cv2.imread("./img/people2.jfif")
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    _, th = cv2.threshold(gray_img, minV, maxV, 1)
    contours, _ = cv2.findContours(th,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
            epsilon = sv/100000 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            cv2.drawContours(img, [approx], -1, (255, 0, 0), 4)
    result = cv2.hconcat([th,gray_img])
    cv2.imshow("setting", result)
    cv2.imshow("people", img)
    cv2.waitKey(1)
