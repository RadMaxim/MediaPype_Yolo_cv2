import cv2

cap = cv2.VideoCapture("video/balloons.mp4")
cv2.namedWindow("setting")


def noth(n):
    pass


cv2.createTrackbar("blur", "setting", 0, 100, noth)
cv2.createTrackbar("blur_1", "setting", 0, 100, noth)
cv2.createTrackbar("cannyMin", "setting", 0, 255, noth)
cv2.createTrackbar("cannyMax", "setting", 0, 255, noth)
# cv2.createTrackbar("eps", "setting", 0, 1000, noth)
cv2.createTrackbar("minT", "setting", 0, 255, noth)
cv2.createTrackbar("maxT", "setting", 0, 255, noth)

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame,(600,500))
    minT = cv2.getTrackbarPos("minT", "setting")
    maxT = cv2.getTrackbarPos("maxT", "setting")
    blurXY = cv2.getTrackbarPos("blur", "setting")
    minC = cv2.getTrackbarPos("cannyMin", "setting")
    maxC = cv2.getTrackbarPos("cannyMax", "setting")

    if blurXY % 2 == 0:
        blurXY += 1
    blur_1 = cv2.getTrackbarPos("blur_1", "setting")
    blur = cv2.GaussianBlur(frame, (11, 11), 0)
    canny = cv2.Canny(blur,255, 255)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (51, 51))
    closed = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)
    cv2.imshow("setting",closed)
    contours, _ = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    squares = []
    obj = {}
    for cont in contours:
        (x, y, w, h) = cv2.boundingRect(cont)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    if not ret:
        break
    cv2.imshow("setting1", frame)
    cv2.waitKey(100)



