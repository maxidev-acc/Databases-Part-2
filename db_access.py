
import sqlite3




def registration(data):
    try:
        con = sqlite3.connect("instance/db.db") 
        cur = con.cursor()
        #cur.execute("DELETE FROM person WHERE svn == '23212211'")
        #con.commit()

        print(data)
        cur.execute("INSERT INTO person VALUES(?, ?, ?, ?,?,?)", data)
        con.commit()
        con.close()
        print("returning true")
        return True
    except:
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
