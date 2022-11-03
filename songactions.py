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
    if not info:
        return
    print("The song is in following playlists:")
    for i in info:
        print(i[0], end="  ")
    print("")




def createPlaylist(uid):
    title = input("Please enter the title of new playlist: ")
    # Create unique pid
    while True:
        pid = random.randint(1, 100000000)
        login.cursor.execute("""
        SELECT * FROM playlists WHERE pid = :pid""", {"pid": pid})
        data = login.cursor.fetchall()
        if not data:
            break
    login.cursor.execute("""INSERT INTO playlists VALUES (:pid,:title,:uid)""",
                         {"pid": pid, "title": title, "uid": uid})
    login.connection.commit()
    return pid


def addToPlaylist(uid, sid):
    login.cursor.execute("""
        SELECT pl.title, pl.pid
        FROM playlists pl
        WHERE pl.uid = :uid
    """, {"uid":uid})
    rows = login.cursor.fetchall()
    if rows:
        mode = input("Input 1 to add the song to your existing playlist, input else to add it to new playlist")
        if mode == "1":
            print('─' * 25)
            for i in range(len(rows)):
                print(str(i)+": " + rows[i][0]+" id: "+str(rows[i][1]))
            print('─' * 25)
            while True:
                mode = input("Enter the index of the playlist you want to add the song to:")
                try:
                    mode = int(mode)
                except ValueError:
                    print("Please enter a number")
                    continue
                if 0 <= mode < len(rows):
                    pid = rows[mode][1]
                    break
        else:
            pid = createPlaylist(uid)
    login.cursor.execute("""
    SELECT max(sorder)+1
    FROM plinclude
    WHERE pid = :pid
    """,{"pid": pid})
    data = login.cursor.fetchall()
    if data and data[0][0] is not None:
        order = data[0][0]
    else:
        order = 1
    login.cursor.execute("""
        SELECT *
        FROM plinclude
        WHERE pid = :pid AND sid = :sid
    """, {"pid": pid, "sid": sid})
    data = login.cursor.fetchall()
    if data:
        print("The song is already in this playlist")
        return
    login.cursor.execute("""INSERT INTO plinclude VALUES (:pid,:sid,:sorder)""",
                         {"pid": pid, "sid": sid, "sorder": order})
    login.connection.commit()


def menu(uid, sid, sno):
    while True:
        selection = input(
            "Please select one of the following actions: \n1. Listen to current song\n2. See more information about current song\n3. Add current song to a playlist\nElse to exit\n")
        if selection == '1':
            listen(uid, sid, sno)
        elif selection == '2':
            seeInfo(sid)
        elif selection == '3':
            addToPlaylist(uid, sid)
        else:
            break
    print("Back to search page...")
    sleep(2)
