# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 01:43:14 2020

@author: Yunus Emre DEMİRDAĞ
"""

import tkinter as tk
import pymongo
import numpy as np
import time
import cv2
from functools import partial

class History_:
    
    def __init__(self,user_name):
        
        self.top = tk.Tk()
        self.hist = self.Get_Data(user_name)
        self.create_Button()
        self.top.mainloop()
    
    def Get_Data(self,user_name):
        self.Client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.Database = self.Client["Users"]
        self.Time_col = self.Database["Time_Action"]
        list_ = list()
        print(user_name)
        for user in self.Time_col.find({"name": user_name}).sort("c_time",-1):
            list_.append(user["time"])
        
        return list_
    
    def btn_click(self,name):
        path = "images/" + str(name[:13]) + "_" + str(name[15:17]) + ".png"
        image = cv2.imread(path)
        cv2.imshow(name,image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def create_Button(self):
        btn_ = list()
        for time_ in self.hist:
            btn = tk.Button(self.top,text = time_,command=partial(self.btn_click,time_),activeforeground="blue",activebackground="pink",pady = 10)
            btn_.append(btn)
        
        for btn in btn_:
            btn.grid()