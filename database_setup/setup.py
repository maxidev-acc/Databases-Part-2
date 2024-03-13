import random, string

import names
from raw_data import letters, lands, cities
import sqlite3
import string
from hashlib import sha256
from tqdm import tqdm

import random
import uuid


class DB_Access():

    def __init__(self):
        pass
    def execute(self,sql, arg =()):
        con = sqlite3.connect("C:/Users/maxim/Documents/GitHub/DatenbankenFluggesellschaft/instance/db.db")
        cur = con.cursor()
        con.execute("PRAGMA foreign_keys = 1")
        if arg != ():
            res = cur.execute(sql, arg)
        else:
            res = cur.execute(sql)

        con.commit()
        ret = res.fetchall()
        con.close()
        return ret


class FLATTEN():
    def __init__(self):
        pass
    def returnFlat(self, tuple):
        res = []
        for k in tuple:
            res.append(k[0])

        return res


personen = """ 
CREATE TABLE IF NOT EXISTS "personen" (

    "svn" INT(10),
	"first_name" TEXT(50)
	CONSTRAINT fn_nn NOT NULL,
	"last_name" TEXT(50)
	CONSTRAINT ln_nn NOT NULL,
	"postal" NUMBER(4),
	"location" TEXT(20),
	"street" TEXT(30),
	"houseNr" NUMBER(3),
	"birthdate" INTEGER
	CONSTRAINT bd_nn NOT NULL,
	"email" TEXT(30) CONSTRAINT mail_nn NOT NULL, 
	"password" TEXT CONSTRAINT pw_nn NOT NULL, 
	CONSTRAINT pk_Personen PRIMARY KEY (svn)
);"""



bank = """ CREATE TABLE bank (
 "BLZ" TEXT,
  "name" TEXT,
  CONSTRAINT employees_pk PRIMARY KEY (BLZ)
);"""



telNo = """ CREATE TABLE telNo (
 "svn" INT(10),
  "telNo" TEXT, 
  CONSTRAINT telpk PRIMARY KEY (svn, telNo),
  CONSTRAINT fk FOREIGN KEY (svn) REFERENCES personen(svn)

);"""



def genTel():
    per = FLATTEN().returnFlat(DB_Access().execute("SELECT svn FROM personen"))

    for pers in per:
        number = "+"+ str(random.randint(1000000000000, 9000000000000))
        data = (pers, number)
        DB_Access().execute("INSERT INTO telNO VALUES(?,?)", data)





employees = """ CREATE TABLE employees (
  "svn" INTEGER ,
  "employee_id" VARCHAR UNIQUE NOT NULL,
  "BLZ" TEXT NOT NULL, 
  "balance" INT NOT NULL,   
  CONSTRAINT svn_pk PRIMARY KEY (svn),
  CONSTRAINT fk FOREIGN KEY (BLZ) REFERENCES bank(BLZ),
  CONSTRAINT fk_pk FOREIGN KEY (svn) REFERENCES personen(svn)
  
  );"""

pilot = """ CREATE TABLE pilots (
  "svn" INTEGER,
  "pilot_no" VARCHAR UNIQUE NOT NULL,
  "flight_hours" VARCHAR NOT NULL,  
    CONSTRAINT svn_ PRIMARY KEY (svn),
    CONSTRAINT  fk_pk FOREIGN KEY (svn) REFERENCES personen(svn)


);"""


anschluss = """ CREATE TABLE flight_awaits (
    "flightNo" TEXT,
    "flightNo2" TEXT,
    CONSTRAINT pk PRIMARY KEY (flightNo, flightNo2),
    CONSTRAINT fk FOREIGN KEY (flightNo) REFERENCES flights(flightNo),
    CONSTRAINT fk2 FOREIGN KEY (flightNo) REFERENCES flights(flightNo2)

     
);"""

from datetime import datetime, timedelta 

def generienrAnschluss():
    start = datetime.now()

    for k in range(1,40):
        
        #try:
            fl1_dep = start+ timedelta(days=k)
            fl1_arr = fl1_dep + timedelta(days=2)
            fl2_dep =fl1_arr
            fl2_arr = fl2_dep + timedelta(days=2)
            flights1 = FLATTEN().returnFlat(DB_Access().execute("SELECT flightNo FROM flights WHERE depaturetime > ? AND depaturetime <? ", (str(fl1_dep),str(fl1_arr))))
            flights2 = FLATTEN().returnFlat(DB_Access().execute("SELECT flightNo FROM flights WHERE depaturetime > ? AND depaturetime <? ", (str(fl2_dep),str(fl2_arr))))
            k = random.choice(flights1)
            j = random.choice(flights2)
            print(k)
            print(j)
            DB_Access().execute("INSERT INTO flight_awaits VALUES(?,?)",(k,j))
        #except:
            pass








technican = """ CREATE TABLE technicans (
  "svn" INTEGER,
  "license_no" VARCHAR UNIQUE NOT NULL,
  "edu" TEXT, 
  "typeNo" VARCHAR NOT NULL, 
    CONSTRAINT tp FOREIGN KEY (typeNo) REFERENCES airplane_type (typeNo),
    CONSTRAINT svn_ PRIMARY KEY (svn),
    CONSTRAINT  fk_pk FOREIGN KEY (svn) REFERENCES personen(svn)


);"""



manu = """ CREATE TABLE manufacturer (
  "name" TEXT,
   CONSTRAINT svn_ PRIMARY KEY (name)
  
);"""




passe = """ CREATE TABLE passenger (
  "svn" INT,
  "passNo" TEXT NOT NULL UNIQUE,
    CONSTRAINT fk FOREIGN KEY (svn) REFERENCES personen (svn),
    CONSTRAINT pk PRIMARY KEY (svn)



);"""



airpl = """ CREATE TABLE airplane_type (
  "typeNo" TEXT,
  "staff_no" INTEGER NOT NULL,
  "seats" INTEGER NOT NULL, 
  "name" TEXT, 
CONSTRAINT manu FOREIGN KEY (name) REFERENCES manufacturer (name),
CONSTRAINT pk PRIMARY KEY (typeNo)
    


);"""



airpl_exemp = """ CREATE TABLE airplane_exemplar (
  "inventoryNo" TEXT,
  "manu_year" INTEGER NOT NULL,
  "fl_hours" INTEGER NOT NULL, 
  "typeNo" TEXT, 
  "blackbox_id" TEXT UNIQUE NOT NULL, 
 CONSTRAINT tp FOREIGN KEY (typeNo) REFERENCES airplane_type (typeNo),
 CONSTRAINT pk PRIMARY KEY (inventoryNo)
    


);"""





def genManuFacturers():
    names = ["Embraer ", "Lockheed Martin (LMT)", "Airbus (EADSY)", "Boeing (BA)" ]
    for name in names:
        DB_Access().execute("INSERT INTO manufacturer VALUES (?)", (name,))
    





def gen_airplane_type():
    manufacturers  = FLATTEN().returnFlat(DB_Access().execute("SELECT name FROM manufacturer"))
    print(manufacturers)
    for k in range(0,10):
            typeNo = "TYP - " + str(random.randint(100,999))
            staff = random.randint(1,7)
            seats = random.randint(150,180)
            name = random.choice(manufacturers)
            print((typeNo, staff, seats, name))
            DB_Access().execute("INSERT INTO airplane_type VALUES(?,?,?,?)", (typeNo, staff, seats, name))







def genAirplaneExemp():
    typeNo  = FLATTEN().returnFlat(DB_Access().execute("SELECT typeNo from airplane_type"))
    print(typeNo)
    for k in range(0,100):
            invNo = "Obj " + str(random.randint(150,180)) +" -Item " + str(random.randint(100,900))
            year = random.randint(1999,2012)
            hours = random.randint(0,10000)
            typeNo1 = random.choice(typeNo)
            bb = "BlackBoxNo. " + str(random.randint(20,40)) +"-" + str(random.randint(20,40))
            print(invNo, year, hours, typeNo1, bb)
            DB_Access().execute("INSERT INTO airplane_exemplar VALUES(?,?,?,?,?)", (invNo, year, hours, typeNo1, bb))








flights = """ CREATE TABLE flights (
  "flightNo" TEXT,
  "depaturetime" DATETIME NOT NULL,
  "arrivaltime" DATETIME NOT NULL, 
  "depatureAirport" TEXT NOT NULL,
  "destinationAirport" TEXT NOT NULL,
  "pilot_no" TEXT, 
  "typeNo" TEXT, 
 CONSTRAINT tp FOREIGN KEY (pilot_no) REFERENCES pilots (pilot_no),
 CONSTRAINT tpP FOREIGN KEY (typeNo) REFERENCES airplane_type (typeNo),
 CONSTRAINT pk PRIMARY KEY (flightNo)
    
);"""


bookings = """ CREATE TABLE bookings (
  "bookingNo" TEXT,
  "passNo" TEXT NOT NULL,
  "flightNo" NOT NULL, 
  "class" TEXT NOT NULL,
 CONSTRAINT tpz FOREIGN KEY (passNo) REFERENCES passenger (passNo),
 CONSTRAINT tpk FOREIGN KEY (flightNo) REFERENCES flights (flightNo),
 CONSTRAINT pk PRIMARY KEY (bookingNo)
    
);"""



blackbox1 = """ CREATE TABLE blackbox (
  "employee_id" VARCHAR,
  "blackbox_id" TEXT,  
  "is_available" TEXT,
 CONSTRAINT tpz FOREIGN KEY (employee_id) REFERENCES employees (employee_id),
 CONSTRAINT tpk FOREIGN KEY (blackbox_id) REFERENCES airplane_exemplar (blackbox_id),
 CONSTRAINT pk PRIMARY KEY (blackbox_id)
);"""
def setup_bb():
    boxes = DB_Access().execute("SELECT blackbox_id FROM airplane_exemplar ")
    res = []
    for k in boxes:
        res.append(k[0])

    for box in res:
        t = True
        emp = None
        val = (emp, box, t)
        DB_Access().execute("INSERT INTO blackbox VALUES (?,?,?)",val )




import uuid
def genBooking():
    passenger= FLATTEN().returnFlat(DB_Access().execute("SELECT passNo FROM passenger"))
    flights= FLATTEN().returnFlat(DB_Access().execute("SELECT flightNo FROM flights"))

    classes = ['A', 'B', 'C']


    for flight in flights:
        for k in range(1,random.randint(10,30)):
            id ="BookingID-" + str(uuid.uuid1())
            passNO = random.choice(passenger) 
            classN = random.choice(classes)
            data = (id, passNO, flight, classN)
            print(data)
            DB_Access().execute("INSERT INTO bookings VALUES(?,?,?,?)", data)
 




from datetime import datetime, timedelta




def gen_flights():
    pilots = FLATTEN().returnFlat(DB_Access().execute("SELECT pilot_no from pilots"))
    typeNo = FLATTEN().returnFlat(DB_Access().execute("SELECT typeNo from airplane_type"))
    print(pilots)
    today = datetime.now()
    
    for k in range(30,160):
        for pilot in pilots:
            try:
                start_date = today + timedelta(days=k)
                end_date = start_date + timedelta(days=1)
                flightNo = "FlightNo " + str(uuid.uuid1())
                depAir = random.choice(cities) 
                arrAir = random.choice(cities)
                assert(depAir != arrAir)
                pil = random.choice(pilots)
                typeNo1 = random.choice(typeNo)
                data1 = (flightNo, str(start_date),str(end_date), depAir,arrAir, pil, typeNo1)
            
                DB_Access().execute("INSERT INTO flights VALUES(?,?,?,?,?,?,?)", data1)
            except:
                print("Wieder ein Flug kaputt")
    print("Next day______")











def generatePersonData():
    letters = string.ascii_lowercase
    data = []
    for k in range(0, 1):
        try:
            svn = str(random.randint(1000000000, 9999999999))
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            street = "Teststraße" + str(k)
            postal = str(random.randint(1000, 9999))
            location = random.choice(cities)
            email = first_name + last_name + "@gmail.com"
            password = "technican"
            birthdate = 19042000
            #for k in range(0, 10):
             #   password = ''.join(random.choice(letters) for i in range(8))
            houseNR = random.randint(0, 9)

            hash_pw = sha256(password.encode('utf-8')).hexdigest()

            user = ((svn, first_name, last_name, postal, location,street , houseNR, birthdate , email, hash_pw))
            print(user)
            DB_Access().execute("INSERT INTO personen VALUES (?,?,?,?,?,?,?,?,?,?)",user)
            # registration((svn, first_name,last_name, adress, postal, location,email, password))
        except:
            pass




def generateEmployees():
    svns= FLATTEN().returnFlat(DB_Access().execute("SELECT svn FROM personen WHERE svn <7000000000"))
    banks = FLATTEN().returnFlat(DB_Access().execute("SELECT BLZ FROM bank"))
    for svn in svns:
            try:
                balance = random.randint(0,10000)
                id = "EMPL-" +str(random.randint(10,99))
                bank = random.choice(banks)
                empl = (svn, id, bank, balance)
                print(empl)
                DB_Access().execute("INSERT INTO employees VALUES(?,?,?,?)", empl)

            except:
                pass


def setEmployee(svn):
   
    banks = FLATTEN().returnFlat(DB_Access().execute("SELECT BLZ FROM bank"))
    
    try:
        balance = random.randint(0,10000)
        id = "EMPL-" +str(random.randint(10,99))
        bank = random.choice(banks)
        empl = (svn, id, bank, balance)
        print(empl)
        DB_Access().execute("INSERT INTO employees VALUES(?,?,?,?)", empl)
        
    except:
        pass


def generateBanks():
    for k in range(0,30):
        blz = str(random.randint(1000,9999))
        name = "BankAG" + names.get_first_name()
        bank = (blz,name)
        print(bank)
        DB_Access().execute("INSERT INTO bank VALUES(?,?)", bank)



def generatePassengers():
    svns = FLATTEN().returnFlat(DB_Access().execute("SELECT svn FROM personen"))
    emps = FLATTEN().returnFlat(DB_Access().execute("SELECT svn FROM employees"))

    for svn in tqdm(svns):

        try:

            assert( svn not in emps)
            pn = "PASS-NO-" + random.choice(letters)+ random.choice(letters)+ "-" + str(random.randint(100, 999))

            passenger = (svn, pn)
            DB_Access().execute("INSERT INTO passenger VALUES (?,?)", passenger)
        except:
            pass





def generatePilots():
    svns = FLATTEN().returnFlat(DB_Access().execute("SELECT svn FROM employees WHERE svn <2000000000"))
    print(len(svns))
    print(svns)

    for svn in svns:
        try:
            Np = "PIL-NO-" + str(random.randint(10, 99))
            hours = random.randint(10000, 100000)
            pilot = (svn, Np, hours)
            DB_Access().execute("INSERT INTO pilots VALUES (?,?,?)", pilot)
        except:
           pass



def generateTech():
    svns = FLATTEN().returnFlat(DB_Access().execute("SELECT svn FROM employees WHERE svn >5000000000"))
    print(len(svns))
    typesf = FLATTEN().returnFlat(DB_Access().execute("SELECT typeNo FROM airplane_type"))
    print(typesf)
    titles = ['Matura', 'Diplom', 'HTL-Matura', 'DiplIng']


    for svn in svns:

            lic = "TECH-NO-" + str(random.randint(10, 99))
            edu = random.choice(titles)
            ty =random.choice(typesf)
            tech = (svn, lic,  edu, ty)
            print(tech)
            DB_Access().execute("INSERT INTO technicans VALUES(?,?,?,?)", tech)



def setTech(svn):
 
   
    typesf = FLATTEN().returnFlat(DB_Access().execute("SELECT typeNo FROM airplane_type"))
    print(typesf)
    titles = ['Matura', 'Diplom', 'HTL-Matura', 'DiplIng']
    lic = "TECH-NO-" + str(random.randint(10, 99))
    edu = random.choice(titles)
    ty =random.choice(typesf)
    tech = (svn, lic,  edu, ty)
    print(tech)
    DB_Access().execute("INSERT INTO technicans VALUES(?,?,?,?)", tech)















