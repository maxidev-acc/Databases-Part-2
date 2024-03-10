
import sqlite3
import hashlib
from hashlib import sha256
import string


class Registration():
    def __init__(self):
        pass

    def register(self, data, phone):
            data =list(data)
            pw = data[9]
            del data[9]
            print(pw)
            hash_pw = sha256(pw.encode('utf-8')).hexdigest()
            data.append(hash_pw)
            insTuple = tuple(data)
            phoneT = (data[0], phone)
            letters = string.ascii_lowercase
            pn = "PASS-NO-" + random.choice(letters)+ random.choice(letters)+ "-" + str(random.randint(100, 999))
            try:
                assert(isinstance(insTuple[0], int))
                DB_Access().executeInsert("INSERT INTO personen VALUES(?, ?, ?, ?,?,?,?,?,?,?)", insTuple)
                DB_Access().executeInsert("INSERT INTO telNo VALUES(?, ?)",phoneT)
                DB_Access().executeInsert("INSERT INTO passenger VALUES(?, ?)",(data[0], pn))

            except Exception as e:
                print(e)
                print(type(e))
                return e
            print("Registration successful")
            return True


class Authentification():
    def __init__(self,data):
        self.data = data
        print(data)
        
    def authentification(self):
        pw = self.data[1]
        con = sqlite3.connect("instance/db.db") 
        cur = con.cursor() 
        hash_pw = sha256(pw.encode('utf-8')).hexdigest()

        cur.execute("SELECT svn FROM personen WHERE email == ? AND password == ?", (self.data[0], hash_pw))
        userID = cur.fetchone()
     
        cur.close()
        con.close()
        if userID:
            return True
        else:
            return False
    def errormessage(self):
         return ("Error at login. Wrong credentials")        




def db_deletion_person(svn):
    con = sqlite3.connect("instance/db.db") 
    cur = con.cursor() 

    id = (svn,)
    cur.execute("DELETE FROM person WHERE svn == ?", id)
    con.commit()
    con.close()




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
import sqlite3


class DB_Access():

    def __init__(self):
        pass
    def executeFetchOne(self,sql, arg =()):
        print(sql)
        print(arg)
        con = sqlite3.connect("instance/db.db")
        cur = con.cursor()
        con.execute("PRAGMA foreign_keys = 1")
        if arg != ():
            res = cur.execute(sql, arg)
        else:
            res = cur.execute(sql)
        con.commit()
        returnTuple = res.fetchone()    
                
        cur.close()
        con.close()
        return  returnTuple
    


    def executeFetchSingle(self,sql, arg =()):
        print(sql)
        print(arg)
        con = sqlite3.connect("instance/db.db")
        cur = con.cursor()
        con.execute("PRAGMA foreign_keys = 1")
        if arg != ():
            res = cur.execute(sql, arg)
        else:
            res = cur.execute(sql)
        
        
        con.commit()
        returnTuple = res.fetchone()
        for k in returnTuple:
            res = k
        cur.close()
        con.close()
        return  res



    def executeFetchAll(self,sql, arg =()):
        print(sql)
        print(arg)
        con = sqlite3.connect("instance/db.db")
        cur = con.cursor()
        con.execute("PRAGMA foreign_keys = 1")
        if arg != ():
            res = cur.execute(sql, arg)
        else:
            res = cur.execute(sql)
        #con.commit()
        returnTuple = res.fetchall()

        cur.close()
        con.close()
        return  returnTuple



    def executeInsert(self,sql, arg =()):
        print(sql)
        print(arg)
        con = sqlite3.connect("instance/db.db")
        cur = con.cursor()
        con.execute("PRAGMA foreign_keys = 1")  
        cur.execute(sql, arg)
        con.commit()
        con.close()
        return  True


class USER():
  
    def __init__(self):
        pass
        
        self.first_name = ""
        self.last_name= ""

    def user(self, arg, par):
        stmt = "SELECT * FROM personen WHERE "+ arg + " = ?"
        print(stmt)
        data = DB_Access().executeFetchOne(stmt,(par,))
        self.svn = data[0]
        print(data)
        return data
        
    def perm(self, svn):
        print(DB_Access().executeFetchOne("SELECT * FROM pilots WHERE svn =  ? ", (svn,)))
        if DB_Access().executeFetchOne("SELECT * FROM pilots WHERE svn =  ? ", (svn,)) !=None:
            return "PIL"
        if DB_Access().executeFetchOne("SELECT * FROM passenger WHERE svn =  ? ", (svn,)) !=None:
            return "P"
        elif DB_Access().executeFetchOne("SELECT * FROM technicans WHERE svn =  ? ", (svn,)) !=None:
            return "TECH"
        

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


class BOOKING():
    def __init__(self, flights_in_cart, passNo):

        
        klasse = "A"

        for flight in flights_in_cart:
            bookingNo = "Booking ID -"+ str(uuid.uuid1()) + " OC"
            flightNo = flight[0]
            print((bookingNo, passNo, flightNo, klasse))
            DB_Access().executeInsert("INSERT INTO bookings VALUES (?,?,?,?)", (bookingNo, passNo, flightNo, klasse))
        print("Booking successful")    



class Ticket(FPDF):
    


    def content(self, data):


        self.ID =str(uuid.uuid1())
        self.name = self.ID+".pdf"
        self.add_page()
        

        self.set_font("Arial", "B", 12)
        today_date = str(datetime.date.today())
        self.cell(55,10, str(data), ln=1, border =1)

        self.image("static/bagheera-removebg-preview.png",145,60,50)
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
        self.cell(55,10, data[0], ln=1, border =1)
        self.cell(55,10, "Name", ln=0, border =1)
        self.cell(55,10, data[0], ln=1, border =1)
        self.cell(55,10, "From", ln=0, border =1)
        self.cell(55,10, data[0], ln=1, border =1)
        self.cell(55,10, "To", ln=0, border =1)
        self.cell(55,10, data[0], ln=1, border =1)
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

