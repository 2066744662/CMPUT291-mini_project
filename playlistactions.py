import songactions
import login
import sqlite3


def showInfo(uid, sno, pid):
    login.cursor.execute(
        """SELECT s.sid,s.title,s.duration FROM songs s, playlists p, plinclude pl WHERE p.pid=:pid AND pl.pid=p.pid AND s.sid=pl.sid""",
        {"pid": pid})
    songs = login.cursor.fetchall()
    # list all songs in the playlist
    print("Songs in the playlist:\n")
    for i in range(0, len(songs)):
        print(i + 1, ". ", songs[i])
    # call of song actions
    selection = input("Please select the song you like: ")
    sid = songs[int(selection)-1][0]
    songactions.menu(uid, sid, sno)
