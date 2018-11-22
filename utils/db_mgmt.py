import sqlite3
import random

DB_FILE="./data/api.db"

def create_db():
    '''
    Creates the db.
    '''
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops

    # c.execute('CREATE TABLE user (username TEXT PRIMARY KEY, password TEXT)')
    # c.execute('CREATE TABLE story_edits (username TEXT, title TEXT)')
    # c.execute('CREATE TABLE stories (title TEXT PRIMARY KEY, story TEXT, last_edit TEXT)')

    db.commit()
    db.close()
