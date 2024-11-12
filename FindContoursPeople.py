import cv2
cv2.namedWindow("people")
def noth(n):
    pass


cv2.createTrackbar("min", "people", 0, 255, noth)
cv2.createTrackbar("max", "people", 0, 255, noth)
cv2.createTrackbar("minS","people",0,10000,noth)
cv2.createTrackbar("maxS","people",0,10000,noth)
while True:
    people_img = cv2.imread("./img/people.jfif")
    minV = cv2.getTrackbarPos("min", "people")
    maxV = cv2.getTrackbarPos("max", "people")
    minS = cv2.getTrackbarPos("minS","people")
    maxS = cv2.getTrackbarPos("maxS","people")
    gray_people = cv2.cvtColor(people_img, cv2.COLOR_BGR2GRAY)
    ret, threshold = cv2.threshold(gray_people, minV, maxV, 0)
    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    people_count = 0
    for contour in contours:
        s = cv2.contourArea(contour)
        print(s)

        if minS < s < maxS:
            people_count+=1
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(people_img, (x, y), (x + w, y + h), (70, 0, 0), 1)
            cv2.putText(people_img,str(s),(x,y),1,0.5,(255,0,0),1)
    cv2.putText(people_img,str(f"Finding search: {people_count}"),(50,50),1,1.0,(0,0,0),2)
    result = cv2.hconcat([gray_people, threshold])
    cv2.imshow("people", result)
    cv2.imshow("about",people_img)
    cv2.waitKey(1)
