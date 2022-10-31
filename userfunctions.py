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

def search_ps(uid):
    keywords = []
    index = 0
    while True:
        keywords.append(input("Please enter the keyword you would like to search: "))
        c = input("Continue? Y/N\n")
        index += 1
        if c == 'Y':
            continue
        else:
            data = []
            # search songs and playlists with keywords
            for i in range(0, index):
                login.cursor.execute(
                    """ SELECT sid,title,duration FROM songs WHERE title LIKE ? UNION SELECT p.pid,p.title,SUM(s.duration) FROM playlists p,plinclude pl,songs s WHERE p.pid=pl.pid AND pl.sid=s.sid AND p.title LIKE ?;""",
                    ('%' + keywords[i] + '%', '%' + keywords[i] + '%',))
                data += login.cursor.fetchall()
            # deal with duplicates
            new_data = []
            for info in data:
                amounts = 0
                for k in keywords:
                    if k in info[i]:
                        amounts += 1
                if info not in new_data:
                    new_data.append(info)
            # sorted by amount of keywords contained
            new_data.sort(key=takeSecond, reverse=True)
            for i in range(0, 5):
                print(new_data[i])
            break

def search_a(uid):
    keywords = []
    index = 0
    while True:
        keywords.append(input("Please enter the keyword you would like to search: "))
        c = input("Continue? Y/N\n")
        index += 1
        if c == 'Y':
            continue
        else:
            data = []
            # search songs and playlists with keywords
            for i in range(0, index):
                login.cursor.execute(
                    """SELECT a.name,a.nationality,COUNT(p2.sid) AS c FROM artists a,perform p1, perform p2,songs s WHERE s.title LIKE ? AND p1.sid=s.sid AND a.aid=p1.aid AND p2.aid=p1.aid;""",
                    ('%' + keywords[i] + '%',))
                if login.cursor.fetchall()[0] is not None:
                    data += login.cursor.fetchall()
                login.cursor.execute(
                    """SELECT a.name,a.nationality,COUNT(p.sid) AS c FROM artists a,perform p WHERE a.name LIKE ? AND p.aid=a.aid;""",
                    ('%' + keywords[i] + '%',))
                if login.cursor.fetchall()[0] is not None:
                    data += login.cursor.fetchall()
            # deal with duplicates
            new_data = []
            for info in data:
                amounts = 0
                for k in keywords:
                    if k in info[1]:
                        amounts += 1
                if info not in new_data:
                    new_data.append([info, amounts])
                else:
                    for j in new_data:
                        if j[0] == info:
                            j[1] += 1
            # sorted by amount of keywords contained
            new_data.sort(key=takeSecond, reverse=True)
            for i in range(0, 5):
                print(new_data[i][0])
            break

def menu(uid):
    """Main screen of the program, also the login screen"""
    while True:
        option = input(
            "Hi Dear user. \nSelect \n1.Start a session\n2.Search for songs or playlists\n3.Search for artists\n4.End current session\n")
        if option == "1":
            start_session(uid)
        if option == "2":
            search_ps(uid)
        if option == "0":
            pass
        if option == "3":
            pass
