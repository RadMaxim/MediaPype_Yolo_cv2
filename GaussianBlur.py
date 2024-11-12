import cv2

cv2.namedWindow("setting")


def noth(n):
    pass


cv2.createTrackbar("hmin", "setting", 0, 255, noth)
cv2.createTrackbar("hmax", "setting", 0, 255, noth)
cv2.createTrackbar("vmin", "setting", 0, 255, noth)
cv2.createTrackbar("vmax", "setting", 0, 255, noth)
cv2.createTrackbar("smin", "setting", 0, 255, noth)
cv2.createTrackbar("smax", "setting", 0, 255, noth)
cv2.createTrackbar("Bmin", "setting", 0, 100, noth)
cv2.createTrackbar("Bmax", "setting", 0, 100, noth)
cv2.createTrackbar("Cmin", "setting", 0, 255, noth)
cv2.createTrackbar("Cmax", "setting", 0, 255, noth)
def morph(img):
    v = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10))
    res = cv2.morphologyEx(img,cv2.MORPH_CROSS, v)
    return res



def settingHSV():
    return [(cv2.getTrackbarPos("hmin", "setting"),
             cv2.getTrackbarPos("smin", "setting"),
             cv2.getTrackbarPos("vmin", "setting")),
            (cv2.getTrackbarPos("hmax", "setting"),
             cv2.getTrackbarPos("smax", "setting"),
             cv2.getTrackbarPos("vmax", "setting"))]


def convertationImgMask(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, settingHSV()[0], settingHSV()[1])
    print(settingHSV())
    return mask


def blurTrack():
    [bMin, bMax] = [cv2.getTrackbarPos("Bmin", "setting"), cv2.getTrackbarPos("Bmax", "setting")]
    if bMin % 2 == 0:
        bMin += 1
    if bMax % 2 == 0:
        bMax += 1
    return bMin, bMax
def settingCanny():
    return [cv2.getTrackbarPos("Cmin","setting"),cv2.getTrackbarPos("Cmax","setting")]
def convertCanny(img):
    canny = cv2.Canny(img,settingCanny()[0],settingCanny()[1])
    return canny



def settingBlur(img):
    blur = cv2.GaussianBlur(img, (blurTrack()), 0)
    return blur


while True:
    img = cv2.imread("img/cats1.jpg")
    img = cv2.resize(img, (500, 300))
    img = settingBlur(img)
    mask = convertationImgMask(img)
    canny = convertCanny(img)
    canny = morph(canny)
    mask = morph(mask)
    cv2.imshow("setting", mask)
    cv2.imshow("canny",canny)
    cv2.waitKey(1)
