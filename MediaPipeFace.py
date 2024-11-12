import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mpDraw = mp.solutions.drawing_utils
drawStyles = mp.solutions.drawing_styles.get_default_face_mesh_tesselation_style()
drawSpec = mp.solutions.drawing_utils.DrawingSpec(thickness=1, circle_radius=0)

mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh()

while True:
   frame = cap.read()[1]
   rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
   results = faceMesh.process(rgb)
   objects = []

   if results.multi_face_landmarks:

       for faces in results.multi_face_landmarks:
           mpDraw.draw_landmarks(frame, faces, mpFaceMesh.FACEMESH_TESSELATION, drawStyles, drawStyles)
   cv2.imshow("frame", frame)
   cv2.waitKey(1)