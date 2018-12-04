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
    c.execute("CREATE TABLE IF NOT EXISTS searches(username TEXT, long INTEGER, lat INTEGER, city TEXT, time TEXT, region TEXT, country TEXT, PRIMARY KEY (long, lat))")

    db.commit()
    db.close()

def isUser(user):
    '''
    returns boolean of whether user is already in the database
    '''
    command_tuple = (user)
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT username FROM users WHERE username=?",command_tuple)
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

    command_tuple = (user)
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT password FROM users WHERE username=?", command_tuple)
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

    command_tuple= (user)

    print("THIS WORKS")
    c.execute("SELECT long FROM searches WHERE username=?",command_tuple)
    dict['long'] = c.fetchall()
    c.execute("SELECT lat FROM searches WHERE username=?",command_tuple)
    dict['lat'] = c.fetchall()
    c.execute("SELECT city FROM searches WHERE username=?",command_tuple)
    dict['city'] = c.fetchall()
    c.execute("SELECT time FROM searches WHERE username=?",command_tuple)
    dict['time'] = c.fetchall()

    db.commit()
    db.close()

    return dict

def register(user, pw):
    '''
    inputs username and password into the users database
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    command_tuple = (user, pw)
    c.execute("INSERT INTO users VALUES(?,?)", command_tuple)

    db.commit()
    db.close()
    return True

def addSearch(user, long, lat, city, region=None, country):
    '''
    creates entry in searches database of longitude, latitude, city name, username, and timestamp
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    command_tuple = (datetime.utcnow(), user, long, lat)
    c.execute("UPDATE searches SET time=? WHERE username=? AND long=? AND lat=? ", command_tuple)
    command_tuple = (user, long, lat, city, datetime.utcnow(), region, country, user, city, long, lat)
    c.execute("INSERT INTO searches SELECT ?,?,?,?,?,?,? WHERE NOT EXISTS (SELECT city from searches WHERE username=? AND city=? AND long=? AND lat=?)", command_tuple)

    db.commit()
    db.close()

    return True

def removeSearch(user, long, lat):
    '''
    removes entry in searches database based on username, longitude, and latitude
    '''
    command_tuple = (user, long, lat)

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("DELETE FROM searches WHERE username=? AND long=? AND lat=?", command_tuple)
    db.commit()
    db.close()

    return True

if __name__ == '__main__':
    create_db()
