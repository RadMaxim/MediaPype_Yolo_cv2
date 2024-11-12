import cv2
import mediapipe as mp
cam = cv2.VideoCapture(0)#подключение видеокамеры
mpDraw = mp.solutions.drawing_utils #подключение утилиты
drawStylesHands = mp.solutions.drawing_styles #стиль для отрисовки линий между контрольными точками
drawSpec = mp.solutions.drawing_utils.DrawingSpec(thickness=1,circle_radius=2)#стили для отрисовки контрольных точек
drawStylesFace = mp.solutions.drawing_styles.get_default_face_mesh_tesselation_style()
mpHandsMesh = mp.solutions.hands
handsMesh = mpHandsMesh.Hands()
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh()
while True:
    frame = cam.read()[1]#переменная для видеокадров
    rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)# преобразование в палитру RGB
    results_face = faceMesh.process(rgb)#нахождение лиц на изображении
    results_hands = handsMesh.process(rgb)# нахождение рук на изображении
    if results_face.multi_face_landmarks:# проверка на наличие лиц
        for face in results_face.multi_face_landmarks:
            mpDraw.draw_landmarks(frame,face,mpFaceMesh.FACEMESH_TESSELATION, drawStylesFace,drawStylesFace)

    if results_hands.multi_hand_landmarks:# проверка на наличие рук
        for hand in results_hands.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame,hand,mpHandsMesh.HAND_CONNECTIONS,drawStylesHands.get_default_hand_landmarks_style(),drawStylesHands.get_default_hand_connections_style())
            obj ={}
            for id,lm in enumerate(hand.landmark,0):
                (h,w,d) = frame.shape
                x = int(lm.x*w)
                y = int(lm.y*h)
                obj[id]=(x,y)
                cv2.putText(frame,str(id),(x,y),1,1.3,(0,0,0),1)
            print(obj)
            cv2.line(frame,(obj[4][0],obj[4][1]),(obj[8][0],obj[8][1]),(0,0,0),2)
            cv2.putText(frame,
                        str(pow(pow(obj[8][1]-obj[4][1],2)+(pow(obj[4][0]-obj[8][0],2)),0.5)),
                            (100,100),
                            1,
                            1.3,
                            (0,0,0),
                            1)


    cv2.imshow("frame",frame)
    cv2.waitKey(1)