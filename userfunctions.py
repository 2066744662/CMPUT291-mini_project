# Peter Yu
import sqlite3
import random
import time
import login
import songactions
import playlistactions
from time import sleep

global sno


def start_session(uid):
    # make sure session number to be unique
    global sno
    if sno is not None:
        return sno
    while True:
        sno = random.randint(10000, 100000)
        login.cursor.execute("""
                Select *
                FROM  sessions
                WHERE uid = :id
                AND sno = :s
                """, {'id': uid, "s": sno})
        data = login.cursor.fetchall()
        if not data:
            break
    # get current time as start date
    current = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
    login.cursor.execute('INSERT INTO sessions VALUES (:id,:sno,:start,:end)',
                         {"id": uid, "sno": sno, "start": current, "end": None})
    login.connection.commit()
    # current session info
    print("Your session has been started !\nStart date:%s" % (current))
    return sno


def search_ps(uid):
    """
    Search for playlists and songs from keywords entered by user
    :param uid: user id (int)
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
    script += "ORDER BY type\n) GROUP BY sid, type\nORDER BY c DESC\nLIMIT 6\nOFFSET 0"  # output one more to see if have next page
    page = 1
    while True:
        script = script[:-1] + str((page - 1) * 5)
        login.cursor.execute(script)
        rows = login.cursor.fetchall()
        length = min(len(rows), 5)
        if rows is None:
            print("No result Found!")
            return
        print("Page " + str(page))
        print('─' * 25)
        for i in range(length):
            print(
                str(i + 1) + ": " + rows[i][1] + " id = " + str(rows[i][0]) + " (" + rows[i][3] + ") duration: " + str(
                    rows[i][2]))
        print('─' * 25)
        prompt = "Please enter the index(1-" + str(length) + ") to select one of the songs/playlists\n"
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
        elif mode == "n" and len(rows) > 5:
            page += 1
            continue
        else:
            break


def search_a(uid):
    """
    Search for artists and songs from keywords entered by user
    :param uid: user id (int)
    :return: None
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
    script = "SELECT aa.aid,  aa.name, aa.nationality, IFNULL(bb.Nsong,0), COUNT(*) as Nmatch \nFROM (\n"
    for i in range(len(keyword)):
        script += "SELECT a.aid, a.name, a.nationality\nFROM artists a\nWHERE a.name LIKE \"%" + keyword[i] + "%\""
        script += "\nUNION ALL\n"
        script += """SELECT a2.aid, a2.name, a2.nationality FROM artists a2, perform p, songs s 
                        WHERE a2.aid = p.aid AND p.sid = s.sid AND s.title LIKE \"%{}%\"
                    """.format(keyword[i])
        if i != len(keyword) - 1:
            script += "\nUNION ALL\n"
    script += """) as aa\nLEFT OUTER JOIN (
    SELECT a.aid, COUNT(p.sid) as Nsong
    FROM artists a, perform p 
    WHERE a.aid = p.aid 
    GROUP BY a.aid
    ) as bb
    ON aa.aid = bb.aid
    GROUP BY aa.aid
    ORDER BY Nmatch DESC
    LIMIT 6
    OFFSET 0"""
    page = 1
    while True:
        script = script[:-1] + str((page - 1) * 5)
        login.cursor.execute(script)
        rows = login.cursor.fetchall()
        length = min(len(rows), 5)
        if not rows:
            print("No result Found!")
            return
        print("Page " + str(page))
        print('─' * 25)
        for i in range(length):
            print(str(i + 1) + ": " + rows[i][1] + "(id: " + rows[i][0] + ", nationality: " + rows[i][
                2] + ") who has " + str(rows[i][3]) + " songs.")
        print('─' * 25)
        prompt = "Please enter the index(1-" + str(length) + ") to select an artist\n"
        if len(rows) == 6:
            prompt += "enter \"n\" to go to next page"
            if page > 1:
                prompt += ", "
        if page > 1:
            prompt += "enter \"p\" to go to previous page"
        mode = input(prompt + ", enter anything else to quit: ")
        if mode in ["1", "2", "3", "4", "5"]:
            if rows[int(mode) - 1][3] == 0:
                print("This artist have no songs in record\nBack to search menu...")
                sleep(2)
                return
            aid = rows[int(mode) - 1][0]
            choose_song_from_artist(uid, aid)
        elif mode == "p" and page > 1:
            page += -1
            continue
        elif mode == "n" and len(rows) > 5:
            page += 1
            continue
        else:
            return
def choose_song_from_artist(uid, aid):
    # show all songs
    login.cursor.execute("""
    SELECT s.sid, s.title, s.duration
    FROM perform p, songs s
    WHERE p.aid = :aid AND s.sid = p.sid
    """, {"aid": aid})
    rows = login.cursor.fetchall()
    print("The artist has following songs:")
    print("_" * 25)
    for i in range(len(rows)):
        print(str(i + 1) + ": " + rows[i][1] + " id:" + str(rows[i][0]) + " duration: " + str(rows[i][2]) + "s")
    while True:
        prompt = input("Please enter the index(1-" + str(len(rows)) + ") to select an song, or enter \'e\' to exit\n")
        if prompt in ["e", "E"]:
            print("Back to search page...")
            sleep(1)
            continue
        try:
            prompt = int(prompt)
        except ValueError:
            print("Plase enter a number")
            continue
        if 0 < prompt < len(rows):
            songactions.menu(uid, rows[prompt-1][0], sno)


def end_session(uid):
    global sno
    if sno is None:
        print("You don't have a session currently.")
        return
    current = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
    login.cursor.execute('UPDATE sessions SET end = ? WHERE uid = ? and sno = ?', (current, uid, sno))
    login.connection.commit()
    print("Your session has been successfully ended. ")
    sno = None


def menu(uid):
    """Main screen of the program, also the login screen"""
    global sno
    sno = None
    while True:
        option = input(
            "Hi user. \nSelect \n1.Start a session\n2.Search for songs or playlists\n3.Search for artists\n4.End current session\n5. Log out\n6.Exit the program\n")
        if option == "1":
            start_session(uid)
        if option == "2":
            search_ps(uid)
        if option == "3":
            search_a(uid)
        if option == "4":
            end_session(uid)
        if option == "5":
            return 1
        if option == "6":
            return 0
        else:
            continue
if __name__ == "__main__":
    search_ps("u1")
