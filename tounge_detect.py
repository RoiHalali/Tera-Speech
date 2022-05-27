"Name       : Roi Halali & Dor Kershberg "
"Titel      : edge and color detect      "


import cv2
import numpy as np
import mediapipe as mp
import time
import matplotlib.pyplot as plt
from skimage import morphology
from opencvcoloredge import *


NUM_FACE = 1
            
class FaceLandMarks():
    def __init__(self, staticMode=False,maxFace=NUM_FACE, minDetectionCon=0.5, minTrackCon=0.5):
        self.staticMode = staticMode
        self.maxFace =  maxFace
        self.minDetectionCon = minDetectionCon
        self.minTrackCon = minTrackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.staticMode, self.maxFace, self.minDetectionCon, self.minTrackCon)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1)

    def findFaceLandmark(self, img, draw=False):
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(self.imgRGB)

        faces = []
        
        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACE_CONNECTIONS, self.drawSpec, self.drawSpec)

                face = []
                for id, lm in enumerate(faceLms.landmark):
                    # print(lm)
                    ih, iw, ic = img.shape
                    x, y = int(lm.x * iw), int(lm.y * ih)
                    # cv2.putText(img, str(id), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0,255,0), 1)
                    # print(id, x, y)
                    face.append([x,y])
                faces.append(face)
        return img, faces

def simple_edge_detection(image): 
   edges_detected = cv2.Canny(image , 100, 200) 
   images = [image , edges_detected]
   
 
def dist(x1,y1,x2,y2):
    distance= np.sqrt(np.square(x1-x2)+np.square(y1-y2))
    return distance 
   
def cropp_img(full_img,x,y,h,w):
    # Convert into grayscale
    # Draw rectangle around the faces and crop the faces
    cropped_face = full_img[(y-300):y + h+300, x:x + w]
    return(cropped_face)


# framewidth=1912     
# framehight=1072  
# cap=cv2.VideoCapture(0)
# cap.set(3,framewidth)
# cap.set(4,framehight)
def tounge(img):
    i=0
    factor=0.5
    tounge_state = 'down'
    
    # success, img = cap.read()
    if i % 10 == 0 :
        cropp, cleaned, bottom_cor = tounge_down(img, factor, tounge_state)
   
    if len(cleaned) != 0:
        output = cv2.connectedComponentsWithStats(cleaned, 8, cv2.CV_32S)
        num_labels = output[0]
        ton_down=dist(points[17,0],points[17,1],bottom_cor[0],points[1,1])
        if (bottom_cor[1]>points[17,1]) and (i%10==0)and (num_labels==2) :
            cv2.putText(img,"down" ,(25,100),2,1,(255,0,0)) 
        # if((i % 10 == 0) and (num_labels == 2)):
        #     print_dots(cropp,cleaned)
    
        # elif(bottom_cor[1]<points[17,1]) and (i%10==0)and (num_labels==2) :
        #     cv2.putText(img,"up" ,(25,100),2,1,(255,0,0)) 
        #     print_dots(cropp,cleaned)
        # if((i%10==0)and (num_labels==2)):
            # print_dots(cropp,cleaned)
    
        # cv2.imshow('img', img)
        # cv2.resizeWindow('img', 400, 400)
        
        # key = cv2.waitKey(1)                    #end loop in esq
        # if key == 27:
        #     break
        
        # cap.release()
        # cv2.destroyAllWindows() 
        # print_dots(cropp,cleaned)
        return cleaned
    else: return cropp

 




