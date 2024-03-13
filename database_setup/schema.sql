



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
);



 CREATE TABLE telNo (
 "svn" INT(10),
  "telNo" TEXT, 
  CONSTRAINT telpk PRIMARY KEY (svn, telNo),
  CONSTRAINT fk FOREIGN KEY (svn) REFERENCES personen(svn)

);



 CREATE TABLE employees (
  "svn" INTEGER ,
  "employee_id" VARCHAR UNIQUE NOT NULL,
  "BLZ" TEXT NOT NULL, 
  "balance" INT NOT NULL,   
  CONSTRAINT svn_pk PRIMARY KEY (svn),
  CONSTRAINT fk FOREIGN KEY (BLZ) REFERENCES bank(BLZ),
  CONSTRAINT fk_pk FOREIGN KEY (svn) REFERENCES personen(svn)
  
  );





CREATE TABLE pilots (
  "svn" INTEGER,
  "pilot_no" VARCHAR UNIQUE NOT NULL,
  "flight_hours" VARCHAR NOT NULL,  
    CONSTRAINT svn_ PRIMARY KEY (svn),
    CONSTRAINT  fk_pk FOREIGN KEY (svn) REFERENCES personen(svn)


);



CREATE TABLE technicans (
  "svn" INTEGER,
  "license_no" VARCHAR UNIQUE NOT NULL,
  "edu" TEXT, 
  "typeNo" VARCHAR NOT NULL, 
    CONSTRAINT tp FOREIGN KEY (typeNo) REFERENCES airplane_type (typeNo),
    CONSTRAINT svn_ PRIMARY KEY (svn),
    CONSTRAINT  fk_pk FOREIGN KEY (svn) REFERENCES personen(svn)


);

 CREATE TABLE passenger (
  "svn" INT,
  "passNo" TEXT NOT NULL UNIQUE,
    CONSTRAINT fk FOREIGN KEY (svn) REFERENCES personen (svn),
    CONSTRAINT pk PRIMARY KEY (svn)



);

 CREATE TABLE bank (
 "BLZ" TEXT,
  "name" TEXT,
  CONSTRAINT employees_pk PRIMARY KEY (BLZ)
);



CREATE TABLE manufacturer (
  "name" TEXT,
   CONSTRAINT svn_ PRIMARY KEY (name)
  
);


CREATE TABLE airplane_type (
  "typeNo" TEXT,
  "staff_no" INTEGER NOT NULL,
  "seats" INTEGER NOT NULL, 
  "name" TEXT, 
CONSTRAINT manu FOREIGN KEY (name) REFERENCES manufacturer (name),
CONSTRAINT pk PRIMARY KEY (typeNo)
    


);



 CREATE TABLE airplane_exemplar (
  "inventoryNo" TEXT,
  "manu_year" INTEGER NOT NULL,
  "fl_hours" INTEGER NOT NULL, 
  "typeNo" TEXT, 
  "blackbox_id" TEXT UNIQUE NOT NULL, 
 CONSTRAINT tp FOREIGN KEY (typeNo) REFERENCES airplane_type (typeNo),
 CONSTRAINT pk PRIMARY KEY (inventoryNo)
    


);



CREATE TABLE blackbox (
  "employee_id" VARCHAR,
  "blackbox_id" TEXT,  
  "is_available" TEXT,
 CONSTRAINT tpz FOREIGN KEY (employee_id) REFERENCES employees (employee_id),
 CONSTRAINT tpk FOREIGN KEY (blackbox_id) REFERENCES airplane_exemplar (blackbox_id),
 CONSTRAINT pk PRIMARY KEY (blackbox_id)
);






CREATE TABLE flights (
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
    
);



 CREATE TABLE flight_awaits (
    "flightNo" TEXT,
    "flightNo2" TEXT,
    CONSTRAINT pk PRIMARY KEY (flightNo, flightNo2),
    CONSTRAINT fk FOREIGN KEY (flightNo) REFERENCES flights(flightNo),
    CONSTRAINT fk2 FOREIGN KEY (flightNo2) REFERENCES flights(flightNO)

    
);


CREATE TABLE bookings (
  "bookingNo" TEXT,
  "passNo" TEXT NOT NULL,
  "flightNo" NOT NULL, 
  "class" TEXT NOT NULL,
 CONSTRAINT tpz FOREIGN KEY (passNo) REFERENCES passenger (passNo),
 CONSTRAINT tpk FOREIGN KEY (flightNo) REFERENCES flights (flightNo),
 CONSTRAINT pk PRIMARY KEY (bookingNo)
    
);



