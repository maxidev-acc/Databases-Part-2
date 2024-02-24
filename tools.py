
import datetime
import os
from fpdf import FPDF
import datetime
import shutil
import subprocess
import random
import uuid
import threading
import logging
import time
import json
import requests





""" 
userIn = [{"name":"Maximilian", "email": "admin@test.at","sex": "M", "birthDate": "1999/03/20", "origin": "AT", "SVN": "5039 290399","role": "T"}]
print(type(userIn))

for k in userIn:
    print(k["role"])

"""


class Ticket(FPDF):



    def content(self,origin, destiantion, depatureDate, flight,first_name, name , id , birthDate):
        self.ID =str(uuid.uuid1())
        self.name = self.ID+".pdf"
        self.add_page()
        self.set_font("Arial", "B", 12)
        today_date = str(datetime.date.today())
        self.image("static/bagheera-removebg-preview.png",145   ,60,50)
        self.cell(100, 10, " ", border=0, ln =0, )
        self.image("static/qrcode.jpeg",40,200,80)
        self.cell(100, 30, " ", border=0, ln =0)
        self.cell(100, 20, today_date, border=0, ln=1, align="C")
        self.cell(100, 10, "", ln=1)
        self.set_font("Arial", "B", 20)
        self.cell(180,20, "Boarding pass", border = 1, ln=1, align = "C")
        self.set_font("Arial", "B", 10)
        self.set_fill_color(0, 0, 0)
        self.cell(180,3, "" ,fill= True, ln= 1)
        self.cell(55,10, "Firstname", ln=0, border =1)
        self.cell(55,10, name, ln=1, border =1)
        self.cell(55,10, "Name", ln=0, border =1)
        self.cell(55,10, first_name, ln=1, border =1)
        self.cell(55,10, "From", ln=0, border =1)
        self.cell(55,10, origin, ln=1, border =1)
        self.cell(55,10, "To", ln=0, border =1)
        self.cell(55,10, destiantion, ln=1, border =1)
        self.cell(180,1, "" ,fill= True, ln= 1)
        self.set_font("Arial", "B", 20)
        self.cell(180, 20, "First class ticket", border =1, ln =1)
        self.cell(180,1, "",fill= True, ln= 1)
        self.set_font("Arial", "B", 10)
        self.cell(60,20, "Plane Airplane ",ln =0, border =1)
        self.cell(50,20, "", border = 1, ln = 1)
        self.cell(180,1, "",fill= True, ln= 1)
        self.set_font("Arial", "B", 10)
        self.cell(100,20, "", ln=1)
        self.cell(180,1, "" ,fill= True, ln= 1)
        self.cell(50,5,"Bagheera Airlines", ln =1)
        self.cell(100,5,"All rights reseved", ln=1)
        self.cell(180,1, "" ,fill= True, ln= 1)
        self.cell(150,5, "Unique ID:" +self.ID)

""" 
newTicket = Ticket()

newTicket.content("AUT", "DE", "01.01.1999", "EAR1-Q$3","Maximilain", "100-100" , "02.02.1999")
name = "Ticket1.pdf"
newTicket.output(dest='S').encode('latin-1', 'ignore')
newTicket.output(name)
"""

class Transaction():
    def __init__(self):
        pass
    def verify(self, bankaccount, cvv):
        r =requests.get("https://retoolapi.dev/iibcMI/transactionAPI/1")
        print(r)
        print(r.text)
        res = json.loads(r.text)
        print(res)
        if res["status"] == True and res["bankAccount"] == bankaccount and res["cvv"] ==cvv:
            print("Success with transaction ID: ", str(res["transactionID"]))
            return True
        
        else:
            return False


