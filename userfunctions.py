# Peter Yu
import sqlite3
import random
import time
import login
from getpass import getpass


def start_session(uid):
    sno = random.randint(10000, 100000)
    #make sure session number to be unique
    while True:
        login.cursor.execute("""
                Select sno
                FROM  sessions
                WHERE uid = :id
                """, {'id': uid})
        data = login.cursor.fetchall()
        if sno not in data:
            break
        else:
            sno = random.randint(10000, 100000)
    #get current time as start date
    current = time.strftime('%Y-%m-%d', time.localtime())
    login.cursor.execute('INSERT INTO sessions VALUES (:id,:sno,:start,:end)',
                         {"id": uid, "sno": sno, "start": current, "end": None})
    #current session info
    print("Your session has been started !\nSession number: %d\nStart date:%s" % (sno, current))


def menu(uid):
    """Main screen of the program, also the login screen"""
    while True:
        option = input(
            "Hi Dear user. \nSelect \n1.Start a session\n2.Search for songs or playlists\n3.Search for artists\n4.End current session\n")
        if option == "1":
            start_session(uid)
        if option == "2":
            pass
        if option == "0":
            pass
        if option == "3":
            pass
