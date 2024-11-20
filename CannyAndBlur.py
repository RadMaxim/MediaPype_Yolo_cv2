import cv2
cam = cv2.VideoCapture(0)
def noth(n):
    pass
cv2.namedWindow("frame")
cv2.createTrackbar("hl","frame",0,255,noth)
cv2.createTrackbar("sl","frame",0,255,noth)
cv2.createTrackbar("vl","frame",0,255,noth)
cv2.createTrackbar("hh","frame",0,255,noth)
cv2.createTrackbar("sh","frame",0,255,noth)
cv2.createTrackbar("vh","frame",0,255,noth)
cv2.createTrackbar("sigma","frame",8,255,noth)
cv2.createTrackbar("canMin","frame",0,255,noth)
cv2.createTrackbar("canMax","frame",0,255,noth)
while True:
    frame1 = cam.read()[1]
    sigma = cv2.getTrackbarPos("sigma", "frame")
    canMin = cv2.getTrackbarPos("canMin", "frame")
    canMax = cv2.getTrackbarPos("canMax", "frame")
    if sigma%2==0:
        sigma+=1
    frame = cv2.GaussianBlur(frame1, (sigma, sigma), 100)
    canny = cv2.Canny(frame, canMin, canMax)
    hl = cv2.getTrackbarPos("hl", "frame")
    sl = cv2.getTrackbarPos("sl", "frame")
    vl = cv2.getTrackbarPos("vl", "frame")
    hh = cv2.getTrackbarPos("hh", "frame")
    sh = cv2.getTrackbarPos("sh", "frame")
    vh = cv2.getTrackbarPos("vh", "frame")
    minV = (hl, sl, vl)
    maxV = (hh, sh, vh)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,minV,maxV)
    contours,_ = cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        epsilon = 0.01 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        cv2.putText(frame,"finding",(x,y),1,1.0,(0,0,0),2)
        if x>frame.shape[1]//2:
            print("right")
        else:
            print("left")
        cv2.drawContours(frame,[approx],-1,(255,0,255),3)
    print(frame.shape)
    cv2.line(frame,(frame.shape[1]//2,0),(frame.shape[1]//2,frame.shape[0]-1),(100,200,255),3)
    res = cv2.hconcat([canny, mask])
    cv2.imshow("frame",res)

    cv2.waitKey(1)