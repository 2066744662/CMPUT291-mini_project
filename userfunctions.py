# Peter Yu
import sqlite3
import random
import time
import login
import songactions
import playlistactions
global sno

def start_session(uid):
    #make sure session number to be unique
    global sno
    while True:
        sno = random.randint(10000, 100000)
        login.cursor.execute("""
                Select *
                FROM  sessions
                WHERE uid = :id
                AND sno = :s
                """, {'id': uid, "s":sno})
        data = login.cursor.fetchall()
        if not data:
            break
    #get current time as start date
    current = time.strftime('%Y-%m-%d', time.localtime())
    login.cursor.execute('INSERT INTO sessions VALUES (:id,:sno,:start,:end)',
                         {"id": uid, "sno": sno, "start": current, "end": None})
    login.connection.commit()
    #current session info
    print("Your session has been started !\nStart date:%s" % (current))
    return sno
def search_ps(uid):
    """
    Search for playlists and songs from keywords entered by user
    :param uid:
    :return:
    """
    global sno
    # Prompt for keywords
    keyword = [input("Please enter the keyword you would like to search: ")]
    while True:
        s = input("Enter the next keyword, or enter \":e\" to end: ")

        if s in [":e"]:
            break
        keyword.append(s)
    # Build script
    script = "SELECT *, COUNT(*) as c FROM ("
    for i in range(len(keyword)):
        script += "SELECT *,\'song\' as type FROM songs s WHERE s.title LIKE \"%" + keyword[i] + "%\""
        script += "\nUNION ALL\n"
        script += """
                    SELECT a.pid, a.title, IFNULL(b.dur,0), a.type FROM
                    (SELECT *,'playlist' as type FROM playlists p WHERE p.title LIKE '%{}%') as a
                    LEFT OUTER JOIN
                    (SELECT *, SUM(s.duration) as dur
                    FROM playlists p2, plinclude pl, songs s 
                    WHERE p2.pid = pl.pid 
                    AND pl.sid = s.sid 
                    GROUP BY p2.pid) as b
                    ON a.pid = b.pid
                """.format(keyword[i])
        if i != len(keyword) - 1:
            script += "\nUNION ALL\n"
    script += "ORDER BY type\n) GROUP BY sid, type\nORDER BY c DESC\nLIMIT 6\nOFFSET 0" #output one more to see if have next page
    page = 1
    while True:
        script = script[:-1] + str((page - 1) * 5)
        login.cursor.execute(script)
        rows = login.cursor.fetchall()
        length = min(len(rows), 5)
        if rows is None:
            print("No result Found!")
            return
        print("Page "+str(page))
        print('─' * 25)
        for i in range(length):
            print(str(i+1) +": " + rows[i][1]+ " ("+ rows[i][3]+") duration: "+str(rows[i][2]))
        print('─' * 25)
        prompt = "Please enter the index(1-"+str(length)+") to select one of the songs/playlists\n"
        if len(rows) == 6:
            prompt += "enter \"n\" to go to next page"
            if page > 1:
                prompt += ", "
        if page > 1:
            prompt += "enter \"p\" to go to previous page"
        mode = input(prompt + ", enter anything else to quit: ")
        if mode in ["1", "2", "3", "4", "5"]:
            if rows[int(mode) - 1][3] == "song":
                songactions.menu(uid, rows[int(mode) - 1][0], sno)
            else:
                playlistactions.showInfo(uid, sno, rows[int(mode) - 1][0])
        elif mode == "p" and page > 1:
            page += -1
            continue
        elif mode == "n":
            page += 1
            continue
        else:
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
    sno = None


def menu(uid):
    """Main screen of the program, also the login screen"""
    global sno
    sno = None
    while True:
        option = input(
            "Hi Dear user. \nSelect \n1.Start a session\n2.Search for songs or playlists\n3.Search for artists\n4.End current session\n")
        if option == "1":
            start_session(uid)
        if option == "2":
            search_ps(uid)
        if option == "3":
            search_a(uid)
        if option == "4":
            end_session(uid)

if __name__ == "__main__":
    search_ps("u1")