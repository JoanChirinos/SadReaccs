import sqlite3
import random
from datetime import datetime

DB_FILE="./data/sadreaccs.db"

def create_db():
    '''
    Creates the db.
    '''
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops

    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS searches(username TEXT, long INTEGER, lat INTEGER, city TEXT, time TEXT)")

    db.commit()
    db.close()

def isUser(user):
    '''
    returns boolean of whether user is already in the database
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT username FROM users WHERE username = '{0}'".format(user))
    name = c.fetchone()
    db.commit()
    db.close()
    if name != None and len(name) > 0:
        return True
    return False

def getPw(user):
    '''
    returns passwords of specific user
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT password FROM users WHERE username = '{0}'".format(user))
    x = c.fetchone()
    db.commit()
    db.close()
    return x[0]

def getSearches(user):
    '''
    returns all searches of a specific user
    '''
    x = {'long', 'lat', 'city', 'time'}

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("SELECT long FROM searches WHERE username = '{0}'".format(user))
    x['long'].append(c.fetchall())
    c.execute("SELECT lat FROM searches WHERE username = '{0}'".format(user))
    x['lat'].append(c.fetchall())
    c.execute("SELECT city FROM searches WHERE username = '{0}'".format(user))
    x['city'].append(c.fetchall())
    c.execute("SELECT timestamp FROM searches WHERE username = '{0}'".format(user))
    x['time'].append(c.fetchall())

    db.commit()
    db.close()

    return x

def register(user, pw):
    '''
    inputs username and password into the users database
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO users VALUES('{0}','{1}')".format(user,pw))
    db.commit()
    db.close()

def addSearch(user, long, lat, city):
    '''
    creates entry in searches database of search text, username, and timestamp
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO searches VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(user, long, lat, city, datetime.utcnow()))
    db.commit()
    db.close()

    return True

if __name__ == '__main__':
    create_db()
