
import sqlite3
import hashlib



def registration(data):
    
        con = sqlite3.connect("instance/db.db") 
        cur = con.cursor()
        #cur.execute("DELETE FROM person WHERE svn == '23212211'")
        #con.commit()
        print(data)
        cur.execute("INSERT INTO person VALUES(?, ?, ?, ?,?,?,?,?)", data)
        con.commit()
        con.close()
        print("returning true")
        return True




def authentification(auth_data):
    
        con = sqlite3.connect("instance/db.db") 
        cur = con.cursor() 
        #print(auth_data)
        cur.execute("SELECT * FROM person WHERE email == ? AND password == ?", auth_data)
        user = cur.fetchone()
        con.commit()
        if user:
            return user[0]
    
        else:
            return False
     
    



"""
    cur.execute("SELECT * FROM person")
    res = cur.fetchall()
    #so extrahiert man die variablen; abfrage wird als Liste von Tupeln (= Listen) zurückgegben


    for k in res:
        print(k)
        print(k[1])
    print(type(res))
    #print(res)
    con.close()

"""
