
import sqlite3

from datetime import datetime
import encryption as ep
from werkzeug.security import generate_password_hash, check_password_hash


def getuser():
    conn = sqlite3.connect('secure_database.db')
    c = conn.cursor()
    sqlstatement = 'SELECT rowid,userid,password FROM userscenter WHERE status=True'
    c.execute(sqlstatement)
    results=c.fetchall()
    user=[]
    for result in results:
        print (result)
        rowid=result[0]
        userid=result[1]
        pwd = result[2][2:-1]
        print (pwd)
        depwd = ep.decry(pwd)
        user.append({"id":rowid,"name":userid,"password":generate_password_hash(depwd)})

    conn.commit()
    conn.close()
    return user

getuser()