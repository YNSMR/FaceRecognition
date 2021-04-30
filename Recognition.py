# -*- coding: utf-8 -*-

import numpy as np
import cv2
import dlib
from bson.binary import Binary
from imutils import face_utils, resize
import pymongo
import pickle

name = input("İsim Giriniz : ")

#   Database Connections
Client = pymongo.MongoClient("mongodb://localhost:27017/")
Users_db = Client["Users"]
DU_col = Users_db["Defined_Users"]
UU_col = Users_db["Undefined_Users"]
TA_col = Users_db["Time_Action"]

#  Functions
def save_to_database(shape):
    x = DU_col.insert_one({"name" : name,"shape" : np.array(shape).tolist()})
    print(str(x) + " kodlu id ile VeriTabanına kaydedildi.")
    
address = "C:\Python\Face_Recognition\lib\shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(address)
face_cascade = cv2.CascadeClassifier("lib/haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)


while True:    
    ret,frame = cap.read()   
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=5,minSize=(20,20))   
    for (x,y,w,h) in faces:       
        face = gray[y:y+h,x:x+w]
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)       
        rects = detector(face,1)
        for (i,rect) in enumerate(rects):
            shape = predictor(face, rect)
            shape = face_utils.shape_to_np(shape)
            for (xp,yp) in shape:
                cv2.circle(frame,(x+xp,y+yp),1,(0,0,255),-1)
            save_to_database(shape)
    
    cv2.imshow("Frame",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()