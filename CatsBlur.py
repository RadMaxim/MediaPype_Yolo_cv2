import  cv2
cv2.namedWindow("setting")
def noth(n):
    pass
cv2.createTrackbar("blurX","setting",0,100,noth)
cv2.createTrackbar("blurY","setting",0,100,noth)
cv2.createTrackbar("cannyMin","setting",0,255,noth)
cv2.createTrackbar("cannyMax","setting",0,255,noth)
while True:

    img = cv2.imread("./img/cats1.jpg")
    img = cv2.resize(img,(700,500))

    blurX = cv2.getTrackbarPos("blurX","setting")
    blurY = cv2.getTrackbarPos("blurY","setting")
    cannyMin = cv2.getTrackbarPos("cannyMin","setting")
    cannyMax = cv2.getTrackbarPos("cannyMax","setting")
    print(blurX,blurY)
    if blurX%2==0:
        blurX+=1
    if blurY%2==0:
        blurY+=1
    blur = cv2.GaussianBlur(img,(blurX,blurY),1)
    # blur = cv2.GaussianBlur(img,(59,59),1)
    canny1 = cv2.Canny(img,0,255)
    canny2 = cv2.Canny(blur,cannyMin,cannyMax)
    # canny2 = cv2.Canny(blur,255,255)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (57, 57))
    closed = cv2.morphologyEx(canny2, cv2.MORPH_CLOSE, kernel)
    cv2.imshow("cl",closed)
    contours, _ = cv2.findContours(closed,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    for cont in contours:
        (x,y,w,h)= cv2.boundingRect(cont)
        s = cv2.contourArea(cont)
        if s>5:
            eps = (1/50)*cv2.arcLength(cont,True)
            approx = cv2.approxPolyDP(cont,eps,True)
            cv2.drawContours(img,[approx],-1,(255,0,0),2)
    result = cv2.hconcat([canny1,canny2])
    cv2.imshow("img",img)
    cv2.imshow("img1",blur)

    cv2.imshow("setting",result)
    cv2.waitKey(1)