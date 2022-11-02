# Peter Yu
import sqlite3
import random
import time
import login
import songactions
import playlistactions


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
    new_data = []
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
            for info in data:
                if [info, 1] not in new_data and info[0] is not None:
                    new_data.append([info, 1])
                elif [info, 1] in new_data:
                    for i in new_data:
                        if i[0] == info:
                            i[1] += 1
            # sorted by amount of keywords contained
            new_data.sort(key=takeSecond, reverse=True)
            if new_data[0] is not None:
                for i in range(0, 5):
                    if new_data[i][0][0].find('s'):
                        print(i+1, ". playlist", new_data[i][0])
                    else:
                        print(i + 1, ". song", new_data[i][0])
            else:
                print("No results found. Please search another keyword.")
                new_data = []
                continue
            break
    page = 5
    while True:
        selection = input("Please select one of the songs/playlists or enter r to see the next page of results: ")
        if selection == 'r' and page < len(new_data):
            end = page+5 if page+5 < len(new_data) else len(new_data)-1
            for i in range(page, end):
                if new_data[i][0][0].find('s'):
                    print(i + 1, ". playlist", new_data[i][0])
                else:
                    print(i + 1, ". song", new_data[i][0])
            page += 5
            continue
        elif selection == 'r' and page > len(new_data):
            print("All results have been shown. ")
            continue
        else:
            # songs actions
            id = new_data[int(selection)-1][0]
            if id[0][0] == 's':
                songactions.menu(uid, id[0], session)
            elif id[0][0] == 'p':
                playlistactions.showInfo(uid, session, id[0])
            break


def search_a(uid):
    keywords = []
    index = 0
    new_data = []
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
                    """SELECT a.name,a.nationality,COUNT(p2.sid) AS c FROM artists a,perform p1, perform p2,songs s WHERE s.title LIKE ? AND p1.sid=s.sid AND a.aid=p1.aid AND p2.aid=p1.aid UNION SELECT a.name,a.nationality,COUNT(p.sid) AS c FROM artists a,perform p WHERE a.name LIKE ? AND p.aid=a.aid;""",
                    ('%' + keywords[i] + '%', '%' + keywords[i] + '%',))
                data += login.cursor.fetchall()
            # deal with duplicates
            for info in data:
                if [info, 1] not in new_data and info[0] is not None:
                    new_data.append([info, 1])
                # update amount of keywords matched
                elif [info, 1] in new_data:
                    for i in new_data:
                        if i[0] == info:
                            i[1] += 1
            # sorted by amount of keywords contained
            new_data.sort(key=takeSecond, reverse=True)
            for i in range(0, 5):
                print(new_data[i][0])
            break
    page = 5
    songs = []
    while True:
        selection = input("Please select one of the artists or enter r to see the next page of results: ")
        if selection == 'r' and page < len(new_data):
            end = page + 5 if page + 5 < len(new_data) else len(new_data) - 1
            for i in range(page, end):
                print(new_data[i][0])
            page += 5
            continue
        elif selection == 'r' and page > len(new_data):
            print("All results have been shown. ")
            continue
        else:
            n = int(selection)
            name = new_data[n-1][0]
            login.cursor.execute(
                """SELECT s.sid,s.title,s.duration FROM songs s, artists a,perform p WHERE a.name = ? AND p.aid=a.aid AND p.sid=s.sid;""",
                (name,))
            songs = login.cursor.fetchall()
            for i in range(0,len(songs)):
                print(i+1, ". ", songs[i])
            while True:
                song_select = input("Please select one of the songs: ")
                # song actions
                id = new_data[int(song_select) - 1][0]
                songactions.menu(uid, id[0], session)
                break
               
            
def end_session(uid):
    current = time.strftime('%Y-%m-%d', time.localtime())
    login.cursor.execute('UPDATE sessions SET end = ? WHERE uid = ?', {current, uid, })
    print("Your session has been successfully ended. ")
    return 0


def menu(uid):
    """Main screen of the program, also the login screen"""
    while True:
        option = input(
            "Hi Dear user. \nSelect \n1.Start a session\n2.Search for songs or playlists\n3.Search for artists\n4.End current session\n")
        if option == "1":
            session = start_session(uid)
        if option == "2":
            search_ps(uid)
        if option == "3":
            search_a(uid)
        if option == "4":
            session = end_session(uid)
