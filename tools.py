from hashlib import sha256
import string
from DB_Access import DB_Access
from fpdf import FPDF
import datetime
import random
import uuid
import json
import requests
import time
from flask import session

class SESSION():
 
    def __init__(self):
        print("Session init")
        pass

    def setUser(self, user, role):
        
        session['user'] = {"svn": user[0],"first_name":user[1], "last_name": user[2], "postal": user[3], "location":user[4], "street": user[5], "houseNr": user[6], "birthdate": user[7],"email": user[8]}
        print(session['user'])
        session['id'] = user[0]
        session['role'] = role
        session['products'] = []
        self.setItemCount()

    def getUser(self,id):
            return session['user']


    def setItemCount(self):
        count = len(session['products'])
        session['itemcount'] = count

    def getSumm(self):
        sum =0
        currentproducts = session['products']
        K = len(currentproducts)
        sum = K*100
        return sum*0.9

    def deleteItemFromCart(self,flightNo):
        
        index = 0
        for item in session['products']:  
            if item[0] == flightNo:
                del session['products'][index]
                return 0
            index = index +1 

    def clearSessionProducts(self):
        session['products'] = []
        return session['products']

    def ActiveSessionPassenger(self):
        if 'id' in session:
            if session['role'] == "PASSENGER":
                return True
        else:
            return False
    
    def ActiveSessionEmployee(self):
        if 'id' in session:
            if session['role'] != "PASSENGER":
                return True
        else:
            return False

                    





class Registration():
    def __init__(self):
        pass

    def register(self, data, phone):
            data =list(data)
            pw = data[9]
            del data[9]
            hash_pw = sha256(pw.encode('utf-8')).hexdigest()
            data.append(hash_pw)
            insTuple = tuple(data)
            phoneT = (data[0], phone)
            letters = string.ascii_lowercase
            pn = "PASS-NO-" + random.choice(letters)+ random.choice(letters)+ "-" + str(random.randint(100, 999))
            try:
                
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
    def authentification(self):
        pw = self.data[1]
        email = self.data[0]
        hash_pw = sha256(pw.encode('utf-8')).hexdigest()
        userID =DB_Access().executeFetchAll("SELECT svn FROM personen WHERE email = ? AND password = ?  ", (email, hash_pw))
        if userID:
            return True
        else:
            return False
    def errormessage(self):
         return ("Error at login. Wrong credentials")        








class USER():
  
    def __init__(self):
        pass

    def user(self, arg, par):
        stmt = "SELECT * FROM personen WHERE "+ arg + " = ?"
        print(stmt)
        data = DB_Access().executeFetchOne(stmt,(par,))
        self.svn = data[0]
        return data
        
    def perm(self, svn):
        print(DB_Access().executeFetchOne("SELECT * FROM pilots WHERE svn =  ? ", (svn,)))
        if DB_Access().executeFetchOne("SELECT * FROM pilots WHERE svn =  ? ", (svn,)) !=None:
            return "PILOT"
        if DB_Access().executeFetchOne("SELECT * FROM passenger WHERE svn =  ? ", (svn,)) !=None:
            return "PASSENGER"
        elif DB_Access().executeFetchOne("SELECT * FROM technicans WHERE svn =  ? ", (svn,)) !=None:
            return "TECHNICAN"
    def update_user(self, svn, data):
        for index in data:
            sql =  "UPDATE personen SET " +index+ "= ? WHERE svn = "+ str(svn) 
            param = data[index]
            print(param+"1")
            DB_Access().executeInsert(sql,(param,))






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
            DB_Access().executeInsert("INSERT INTO bookings VALUES (?,?,?,?)", (bookingNo, passNo, flightNo, klasse))
        print("Booking  transaction successfully commited")    

class CANCEL_BOOKING():
    def __init__(self, id):#
        try:
            print("Attempt to cancel booking:" , id)
            print(id)
            DB_Access().executeInsert("DELETE FROM bookings WHERE bookingNo = ?", (id,))
        except Exception as e:
            print(e)
            

class BLACKBOX_CHECKOUT():

    def __init__(self):
        pass

    def available_blackboxes(self):
        time.sleep(0.5)
        return DB_Access().executeFetchAll("SELECT * FROM blackbox NATURAL JOIN airplane_exemplar")
    

    def blackbox_ids(self):
        
        fetch =  DB_Access().executeFetchAll("SELECT blackbox_id FROM blackbox")
        returnlist = []
        for k in fetch:
            returnlist.append(k[0])
        return returnlist
    
    def checkout(self, svn, blackbox_id):
        try:
            pilotsraw= DB_Access().executeFetchAll("SELECT svn FROM pilots")
            pilots = []
            for k in pilotsraw:
                pilots.append(k[0])

            technicansraw= DB_Access().executeFetchAll("SELECT svn FROM technicans")
            technicans = []
            for k in technicansraw:
                technicans.append(k[0])
            print(technicans)
            print(svn)
            print((svn in technicans))
            assert((svn in pilots) or (svn in technicans))
            emp_id = DB_Access().executeFetchSingle("SELECT employee_id FROM employees WHERE svn = ?", (svn,)) 
            print(emp_id)
            checkpoint =  DB_Access().executeFetchSingle("SELECT employee_id FROM blackbox WHERE blackbox_id = ?", (blackbox_id,)) 
            print("CP: ", checkpoint)
            assert(checkpoint == None)
            DB_Access().executeInsert("UPDATE blackbox SET employee_id = ?, is_available = False WHERE blackbox_id =?" , (emp_id, blackbox_id))
            print("Sucessfully checked out blackbox")
            return 0 
        except Exception as e:
            print("An error occured while checkout")
            print(e)
    
    def user_blackboxes(self, svn):
        emp_id = DB_Access().executeFetchSingle("SELECT employee_id FROM employees WHERE svn = ?", (svn,)) 
        blackboxes = DB_Access().executeFetchAll("SELECT * FROM blackbox WHERE employee_id = ?", (emp_id,)) 
        return blackboxes
    
    def return_blackbox(self, id):

        print(id)
        time.sleep(0.5)
        DB_Access().executeInsert("UPDATE blackbox SET employee_id = NULL, is_available = TRUE WHERE blackbox_id =?" , (id,))
        return 0





#('Booking ID -72fb9ac3-dfc8-11ee-ae40-2c4d544f4f1c OC', 'PASS-NO-ay-611', 'FlightNo 117380e2-dc98-11ee-83e3-2c4d544f4f1c', 'A',
# 5763170599, '2024-03-12 16:33:34.457647', '2024-03-13 16:33:34.457647', 'Sarajevo', 'Vienna', 'PIL-NO-52', 'TYP - 480', 'SystemAdmin', 'Admin', 5743, 'DE', 'Adminstraße', 29, 17051999, 'admin@gmail.com', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918')

class Ticket(FPDF):
    
    def content(self, data):
       
             
        self.set_text_color(37, 150, 190)

        dic = ["Booking-ID:", "Passenger No:", "Flight No:", "Class:", "SVN", "Depature time:", "Arrival time", "FROM", "TO", "Pilot", "Airplane Type", "Firstname", "Lastname", "Postal", "Location", "Street", " Street No", "Birthdate", "Email:" ]
        data = data[0:19]
        self.ID =str(uuid.uuid1())
        self.name = self.ID+".pdf"
        self.add_page()
        #self.set_text_color(37, 150, 190)
        self.set_draw_color(37, 150, 190)
        
        self.set_font("Arial", "B", 12)
        today_date = str(datetime.date.today())

        self.image("static/plane-icon.png",100,15,10)

        self.cell(180, 10, " ", border=0, ln =1)
        self.image("static/qrcode.jpeg",100,200,80)
       
        
        self.cell(180, 10, today_date, border=0, ln=1, align="R")
        self.set_fill_color(37, 150, 190)

        self.set_font("Arial", "B", 20)
        self.cell(184,2, "", border = 1, ln=1, align = "C" ,fill=True)
        self.cell(2,20, "", border = 1, ln=0, align = "C", fill=True)

        self.cell(180,20, "Boarding pass", border = 1, ln=0, align = "C")

    

        self.cell(2,20, "", border = 1, ln=1, align = "C", fill=True)
        self.cell(184,2, "", border = 1, ln=1, align = "C", fill=True)


        self.set_fill_color(37, 150, 190)
        self.set_font("Arial", "B", 12)
        self.set_text_color(255, 255, 255)
        self.cell(184,2, "", border = 0, ln=1, align = "C", )

        self.cell(150,12, "Flight Details", border = 0, ln=1, fill=True, align = "L")
        self.set_text_color(37, 150, 190)

        

        for k in range(0, len(data)):
            j=117
            print(dic[k])
            print(data[k])
            if k ==11:
                self.set_text_color(255, 255, 255)
                self.cell(150, 10, "Passenger Info", border=1, ln =1, fill=True)
                self.set_text_color(37, 150, 190)

            if k>10:
                j=50
                

            self.cell(1, 10, "", border=1, ln =0, fill=True)
            self.cell(30, 10, str(dic[k]), border=1, ln =0,)
            self.cell(1, 10, "", border=1, ln =0, fill=True)
            self.cell(j, 10, str(data[k]), border=1, ln =0 )
            self.cell(1, 10, "", border=1, ln =1, fill=True)


           
            if (k in [4,8,10]):
                

                self.cell(150,1, "", border = 1, ln=1, fill=True, align = "C")

            pass

        
        
        
        

