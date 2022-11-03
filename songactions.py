# Peter Yu
import sqlite3
import random
import time
import login
import numpy as np
import userfunctions
from getpass import getpass
from time import sleep


def listen(uid, sid, sno):
    if sno is not None:
        login.cursor.execute("""SELECT cnt FROM listen WHERE uid=? AND sid=? AND sno=?""", (uid, sid, sno))
        check = login.cursor.fetchall()
        if not check:
            login.cursor.execute("""INSERT INTO listen VALUES (?,?,?,1)""", (uid, sno, sid))
        else:
            login.cursor.execute("""UPDATE listen SET cnt=cnt+1 WHERE uid=? AND sid=? AND sno=?""", (uid, sid, sno))
    else:
        sno = userfunctions.start_session(uid)
        login.cursor.execute("""INSERT INTO listen VALUES (:uid,:sno,:sid,:cnt)""",
                             {"uid": uid, "sno": sno, "sid": sid, "cnt": 1})
    login.connection.commit()


def seeInfo(sid):
    login.cursor.execute(
        """SELECT a.name, s.sid, s.title, s.duration
            FROM artists a, perform p, songs s 
            WHERE s.sid = :sid
            AND p.sid = s.sid
            AND p.aid = a.aid""",
        {"sid": sid})
    info = login.cursor.fetchall()
    print("Artist Name: " + info[0][0], end="  ")
    print("Song ID: " + str(info[0][1]), end="  ")
    print("Song Title: " + info[0][2], end="  ")
    print("Duration: " + str(info[0][3]) + "s")
    login.cursor.execute(
        """SELECT p.title FROM artists a,songs s,playlists p, plinclude pl,perform pf WHERE s.sid=:sid AND pf.sid=s.sid AND pf.aid=a.aid AND pl.sid=s.sid AND p.pid=pl.pid""",
        {"sid": sid})
    info = login.cursor.fetchall()
    print("The song is in following playlists:")
    if info:
        for i in info:
            print(i[0], end="  ")
        print("")
    else:
        print("None")

order = [1] * 10000


def createPlaylist(uid):
    pid = random.randint(1000, 10000)
    title = input("Please enter the title of new playlist: ")
    login.cursor.execute("""INSERT INTO playlists VALUES (:pid,:title,:uid)""",
                         {"pid": pid, "title": title, "uid": uid})
    login.connection.commit()
    return pid


def addToPlaylist(uid, sid):
    pid = createPlaylist(uid)
    login.cursor.execute("""INSERT INTO plinclude VALUES (:pid,:sid,:sorder)""",
                         {"pid": pid, "sid": sid, "sorder": order[pid]})
    login.connection.commit()
    order[pid] += 1


def menu(uid, id, sno):
    while True:
        selection = input(
            "Please select one of the following actions: \n1. Listen to current song\n2. See more information about current song\n3. Add current song to a playlist\nElse to exit\n")
        if selection == '1':
            listen(uid, id, sno)
        elif selection == '2':
            seeInfo(id)
        elif selection == '3':
            addToPlaylist(uid, id)
        else:
            break
    print("Back to search page...")
    sleep(2)
