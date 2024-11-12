import cv2
cv2.namedWindow("setting")
def noth(n):
    pass

cv2.createTrackbar("minV", "setting", 0, 255, noth)
cv2.createTrackbar("maxV", "setting", 0, 255, noth)
cv2.createTrackbar("accuracy", "setting", 2, 1000, noth)
cv2.createTrackbar("gaussian", "setting", 0, 100, noth)

while True:
    img_figure = cv2.imread("./img/figure2.jpg")
    img_figure = cv2.resize(img_figure,(1000,500))
    gaussian = cv2.getTrackbarPos("gaussian", "setting")

    minV = cv2.getTrackbarPos("minV", "setting")
    maxV = cv2.getTrackbarPos("maxV", "setting")
    acc = cv2.getTrackbarPos("accuracy", "setting")
    gray_figure = cv2.cvtColor(img_figure,cv2.COLOR_BGR2GRAY)
    gray_figure = cv2.GaussianBlur(gray_figure,(21,21),gaussian)
    _,thresh = cv2.threshold(gray_figure,minV,maxV,1)
    contours,_ = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        epsilon = 0.01/acc * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        if len(approx)==4:
            cv2.putText(img_figure,"rectangle",(x,y),1,1.3,(0,0,255),1)
        if len(approx)==3:
            cv2.putText(img_figure, "triangle", (x, y), 1, 1.3, (0, 0, 255), 1)
        if len(approx)>7:
            cv2.putText(img_figure, "circle", (x, y), 1, 1.3, (0, 0, 255), 1)

        cv2.drawContours(img_figure,[approx],-1,(0,0,255),2)

    print(contours)
    result_gray = cv2.hconcat([gray_figure,thresh])

    cv2.imshow("setting",result_gray)
    cv2.imshow("original",img_figure)
    cv2.waitKey(1)
