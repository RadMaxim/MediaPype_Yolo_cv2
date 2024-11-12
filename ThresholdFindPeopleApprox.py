import cv2
cv2.namedWindow("setting")
def noth(n):
    pass
cv2.createTrackbar("gray_min","setting",0,255,noth)
cv2.createTrackbar("gray_max","setting",0,255,noth)
cv2.createTrackbar("approx","setting",2,10000,noth)
while True:
    minV = cv2.getTrackbarPos("gray_min","setting")
    maxV = cv2.getTrackbarPos("gray_max","setting")
    approx_v = cv2.getTrackbarPos("approx","setting")
    figure = cv2.imread("./img/persons.jpg")
    figure = cv2.resize(figure,(500,500))
    gray_figure = cv2.cvtColor(figure,cv2.COLOR_BGR2GRAY)

    _ , thresh = cv2.threshold(gray_figure,minV,maxV,1)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cont in contours:
        print(cont)
        eps = (1/(approx_v+1))*cv2.arcLength(cont,True)
        approx = cv2.approxPolyDP(cont,eps,True)
        s = cv2.contourArea(approx)
        if s>200:

            cv2.drawContours(figure,[approx],-1,(0,0,255),3)
    cv2.imshow("gray",thresh)
    cv2.imshow("fig",figure)
    cv2.waitKey(1)