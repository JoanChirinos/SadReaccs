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
    password = c.fetchone()
    db.commit()
    db.close()
    return password[0]

def getSearches(user):
    '''
    returns all searches of a specific user in a dictionary of longitude, latitude, city name, and time
    '''
    dict = {'long':[], 'lat':[], 'city':[], 'time':[]}

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    print("THIS WORKS")
    c.execute("SELECT long FROM searches WHERE username = '{0}'".format(user))
    dict['long'] = c.fetchall()
    c.execute("SELECT lat FROM searches WHERE username = '{0}'".format(user))
    dict['lat'] = c.fetchall()
    c.execute("SELECT city FROM searches WHERE username = '{0}'".format(user))
    dict['city'] = c.fetchall()
    c.execute("SELECT time FROM searches WHERE username = '{0}'".format(user))
    dict['time'] = c.fetchall()
    print("THIS WORKS")
    db.commit()
    db.close()

    return dict

def register(user, pw):
    '''
    inputs username and password into the users database
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO users VALUES('{0}','{1}')".format(user,pw))
    db.commit()
    db.close()
    return True

def addSearch(user, long, lat, city):
    '''
    creates entry in searches database of longitude, latitude, city name, username, and timestamp
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    #c.execute("SELECT long FROM searches WHERE username = '{0}' WHERE NOT EXISTS (SELECT * FROM searches WHERE username = '{0}', longitude = '{1}')".format(user, long))
    c.execute("UPDATE searches SET time = '{2}' WHERE username = '{0}' AND city = '{1}'".format(user, city, datetime.utcnow()))
    c.execute("INSERT INTO searches SELECT '{0}', '{1}', '{2}', '{3}', '{4}' WHERE NOT EXISTS (SELECT city from searches WHERE username = '{0}' AND city = '{3}')".format(user, long, lat, city, datetime.utcnow()))
    db.commit()
    db.close()

    return True

def removeSearch(user, long, lat):
    '''
    removes entry in searches database based on username, longitude, and latitude
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("DELETE FROM searches WHERE username ='{0}' AND long = '{1}' AND lat = '{2}'".format(user, long, lat))
    db.commit()
    db.close()

    return True

if __name__ == '__main__':
    create_db()
