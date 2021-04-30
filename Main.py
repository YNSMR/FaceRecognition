# -*- coding: utf-8 -*-

import numpy as np
import tkinter as tk
import cv2
import dlib
import pymongo
import time
from functools import partial
from imutils import face_utils
from PIL import Image
from PIL import ImageTk
from History import History_

#  Database Connection
Client = pymongo.MongoClient("mongodb://localhost:27017/")
Users_db = Client["Users"]
DU_col = Users_db["Defined_Users"]
UU_col = Users_db["Undefined_Users"]
TA_col = Users_db["Time_Action"]

#  Functions
def Controll_Defined_Users(shape):
    for user in DU_col.find():
        shape_db = np.array(user["shape"])
        i = 0
        result = False
        for (x,y) in shape:
            if shape_db[i,0] - x <= 2 or shape_db[i,0] - x >= -2:
                if shape_db[i,1] - y <= 2 or shape_db[i,1] - y >= -2:
                    result = True
                else:
                    result = False
                    break
            else:
                result = False
                break
            
        if result:
            return user["name"]
        else:
            return "Undefined"
    return "Undefined"

def Controll_Undefined_Users(shape):
    for user in UU_col.find():
        shape_db = np.array(user["shape"])
        i = 0
        result = False
        for (x,y) in shape:
            if shape_db[i,0] - x <= 10 or shape_db[i,0] - x >= -10:
                if shape_db[i,1] - y <= 10 or shape_db[i,1] - y >= -10:
                    result = True
                else:
                    result = False
                    break
            else:
                result = False
                break
            
        if result:
            return user["name"]
        else:
            return "Undefined"
    
    return "Undefined"
    
def save_Database(shape):
    for i in range(100):
        print(i)
        named = Controll_Undefined_Users(shape)
        if named != "Undefined":
            return named
    
    counter=0
    for us in UU_col.find().sort("name",-1):
        name = us["name"]
        counter = counter + 1
        break
    
    if counter == 1:
        id_ = int(name)
        id_ = id_ + 1
        name = str(id_)
    else:
        name = "0"
        
    UU_col.insert_one({"name": str(name),"shape": np.array(shape).tolist()})

def Timer_Control(name, frame_):
    i = 0
    asc_time = ""
    for timer in TA_col.find({"name":name}).sort("c_time",-1):
        i = i + 1
        time_ = timer["c_time"]
        asc_time = timer["time"]
        break
    
    if i == 0:
        print(time.asctime())
        print(time.time())
        print("------------------------------------")
        TA_col.insert_one({"name":str(name),"time": str(time.asctime()),"c_time":str(time.time())})
        path = "images/" + str(asc_time[:13]) + "_" + str(asc_time[15:17]) + ".png"
        cv2.imwrite(path,frame_)
    else:
        current_timer = time.time()
        comparate = current_timer - float(time_)
        if comparate >= 60:
            print("eklendi..")
            print("*******************************")
            TA_col.insert_one({"name":name,"time": str(time.asctime()),"c_time": str(time.time())})
            path = "images/" + str(asc_time[:13]) + "_" + str(asc_time[15:17]) + ".png"
            cv2.imwrite(path,frame_)
    
def Close_():
    root.destroy()
    cap.release()
    cv2.destroyAllWindows()
    exit()

def hist__(hist_name):
    h = History_(hist_name)
    
#Tkinter Gui Operations
root = tk.Tk()
app = tk.Frame(root,bg="white")
app.grid()
lbl = tk.Label(app)
lbl.grid()
btn_close = tk.Button(app,text = "Kapat",command=Close_,activeforeground="blue",activebackground="pink",pady=10)
btn_close.grid()

def tk_btn(hist_name):
    btn_history = tk.Button(app,text = "Geçmiş",command=partial(hist__,hist_name),activeforeground="blue",activebackground="pink",pady = 10)
    btn_history.grid()

#  Operations
address = "C:\Python\Face_Recognition\lib\shape_predictor_68_face_landmarks.dat"
face_cascade = cv2.CascadeClassifier("lib/haarcascade_frontalface_default.xml")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(address)
cap = cv2.VideoCapture(0)
i=0
old_name = ""

while True:
    ret,frame = cap.read()
    img_ = frame
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=5,minSize=(20,20))
    cv2Image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGBA)
    for (x,y,w,h) in faces:
        face = gray[y:y+h,x:x+w]
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        rects = detector(face,1)
        for (i,rect) in enumerate(rects):
            shape = predictor(face,rect)
            shape = face_utils.shape_to_np(shape)
            user_name = Controll_Defined_Users(shape)
            if user_name == "Undefined":
                user_name = Controll_Undefined_Users(shape = shape)
                if user_name == "Undefined":
                    user_name = save_Database(shape)
                user_name = str(user_name)
            cv2.putText(frame,user_name,(x+10,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
            Timer_Control(user_name,img_)
            if old_name != user_name:
                tk_btn(user_name)
                old_name = user_name
    
    photo = ImageTk.PhotoImage(image = Image.fromarray(img_))
    lbl.configure(image = photo)    
    root.update()

cap.release()
cv2.destroyAllWindows()







#   Geçiş zamanlarını fotları kaydetme
#   Tkinter History Display
#
#
#


































