# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 14:25:22 2020

@author: Yunus Emre DEMİRDAĞ
"""

import pymongo

Client = pymongo.MongoClient("mongodb://localhost:27017/")
Users_db = Client["Users"]
col = Users_db["Time_Action"]

col.delete_many({})