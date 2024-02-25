
import sqlite3



con = sqlite3.connect("instance/db.db") 
cur = con.cursor()
cur.execute("DELETE FROM person WHERE svn == '23212211'")
con.commit()


"""for k in data:
    print(k)
    cur.execute("INSERT INTO person VALUES(?, ?, ?, ?,?,?)", k)
    con.commit()"""

cur.execute("SELECT * FROM person")
res = cur.fetchall()

for k in res:
    print(k)
    print(k[1])
print(type(res))
#print(res)
con.close()

