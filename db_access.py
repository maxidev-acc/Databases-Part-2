
import sqlite3


class DB_Access():

    def __init__(self):
        pass
    def executeFetchOne(self,sql, arg =()):
        print(sql)
        print(arg)
        try:
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
        
        except Exception as e:
            print(e)
    


    def executeFetchSingle(self,sql, arg =()):
            print(sql)
            print(arg)
            try:
                con = sqlite3.connect("instance/db.db")
                cur = con.cursor()
                con.execute("PRAGMA foreign_keys = 1")
                if arg != ():
                    res = cur.execute(sql, arg)
                else:
                    res = cur.execute(sql)
                con.commit()
                returnTuple = res.fetchone()
                res = returnTuple[0]
                cur.close()
                con.close()
                return  res
            except Exception as e:
                print(e)
   
            


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
        con.commit()
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
        return True
