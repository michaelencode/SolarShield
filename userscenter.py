import sqlite3

from datetime import datetime
import encryption as ep
from werkzeug.security import generate_password_hash, check_password_hash

def initialize():
    conn = sqlite3.connect('secure_database.db')
    c = conn.cursor()
    c.execute('CREATE table IF NOT EXISTS userscenter (userid CHARACTER(20) NOT NULL PRIMARY KEY, name CHARACTER(50), password VARCHAR(255) NOT NULL,email VARCHAR(50) NOT NULL,status BLOB NOT NULL,timestamp CHARACTER(30) NOT NULL)')
    conn.commit()
    conn.close()

def getinfo():
    conn = sqlite3.connect('secure_database.db')
    c = conn.cursor()
    c.execute('SELECT rowid,* FROM userscenter')
    results=c.fetchall()
    conn.commit()
    conn.close()
    return results



def checkuser(userid,email,password):
    checked=False
    if userid and email:
        if len(password)>8:
            checked=True
    return checked

def timestamp():
    datetime_format = "%m/%d/%Y %H:%M:%S"
    now = datetime.now()
    timestamp = now.strftime(datetime_format)
    return timestamp

def checkold(userid,oldpassword):
    checkold=False
    conn = sqlite3.connect('secure_database.db')
    c = conn.cursor()
    sqlstatement='SELECT password FROM userscenter WHERE userid="{}"'.format(userid)

    c.execute(sqlstatement)
    pwd=c.fetchone()[0][2:-1]
    depwd=ep.decry(pwd)
    if depwd==oldpassword:
        checkold=True

    conn.commit()
    conn.close()

    return checkold

def getpassword(userid):
    conn = sqlite3.connect('secure_database.db')
    c = conn.cursor()
    sqlstatement = 'SELECT password FROM userscenter WHERE userid="{}"'.format(userid)
    c.execute(sqlstatement)
    pwd = c.fetchone()[0][2:-1]
    depwd = ep.decry(pwd)
    conn.commit()
    conn.close()
    return depwd

def getuser():
    conn = sqlite3.connect('secure_database.db')
    c = conn.cursor()
    sqlstatement = 'SELECT rowid,userid,password FROM userscenter WHERE status=True'
    c.execute(sqlstatement)
    results=c.fetchall()
    user=[]
    for result in results:

        rowid=result[0]
        userid=result[1]
        pwd = result[2][2:-1]
        depwd = ep.decry(pwd)
        user.append({"id":rowid,"name":userid,"password":generate_password_hash(depwd)})

    conn.commit()
    conn.close()
    return user


def changepassword(userid,newpassword):
    conn = sqlite3.connect('secure_database.db')
    enpwd=ep.encry(newpassword)
    c = conn.cursor()
    sqlstatement = 'UPDATE userscenter SET password="{}" WHERE userid="{}"'.format(enpwd,userid)
    c.execute(sqlstatement)
    conn.commit()
    conn.close()


def adduser(userid,name,email,password):
    enpwd=ep.encry(password)
    time=timestamp()
    status=True
    conn = sqlite3.connect('secure_database.db')
    c = conn.cursor()
    sqlstatement='INSERT INTO userscenter VALUES("{userid}","{name}","{enpwd}","{email}",{status},"{timestamp}")'.format(userid=userid,name=name,enpwd=enpwd,email=email,status=status,timestamp=time)

    c.execute(sqlstatement)
    conn.commit()
    conn.close()

def edstatus(id,value):
    if "true" in value:
        status=True
    else:
        status=False

    conn = sqlite3.connect('secure_database.db')
    c = conn.cursor()
    sqlstatement = 'UPDATE userscenter SET status={status} WHERE userid="{id}"'.format(status=status,id=id)

    c.execute(sqlstatement)
    conn.commit()
    conn.close()

