import random

global connection, cursor, aid


def connect(connection1, cursor1, user1):
    global connection, cursor, aid
    connection = connection1
    cursor = cursor1
    aid = user1[1]
    return


def add():
    """Add a song to database, prompy user for song info
            :rtype: tuple
            :return: user/artist and id
            """
    # prompt for info
    global connection, cursor, aid
    title_valid = False
    while True:
        if not title_valid:
            title = input("Please input song title: ")
        duration = input("Please input song duration in seconds: ")
        # check song info
        try:
            duration = int(duration)
        except ValueError:
            print("Error duration input. Please enter a number, do not include unit")
            title_valid = True
            continue
        if duration <= 0:
            print("Error. Duration cannot be less than 1.")
            title_valid = True
        elif check(title, duration):
            print("You have already uploaded a song with same title and duration!")
            mode = input("Input 1 if you want to re-enter song details, input 2 if you still wants to add it as a new "
                         "song, input anything else if you want to reject it:")
            if mode == "1":
                continue
            elif mode == "2":
                break
            else:
                return
        else:
            break
    # insert to db
    sid = create_sid()  # it is unique
    cursor.execute(
        """
        Insert Into songs Values (:s, :t, :d)
        """, {"s": sid, "t": title, "d": duration}
    )
    cursor.execute(
        """
        Insert Into perform Values (:a, :s)
        """, {"s": sid, "a": aid}
    )
    connection.commit()
    print("Success\n")

def check(title, duration):
    """Check if title and duration already exist in db.
            :param: title, duration
            :type: title: string, duration: int
            :rtype: tuple
            :return: song detail if exsit, None if not exist
            """
    global connection, cursor, aid
    cursor.execute("""
        Select * FROM perform p, songs s
        Where p.aid = :a AND p.sid = s.sid AND s.title = :t AND s.duration = :d
        """, {"a": aid, "t": title, "d": duration})
    data = cursor.fetchall()
    return data


def create_sid():
    """Create new sid for current artist.
        :rtype: int
        :return: sid. random 8 digit.
    """
    while True:
        sid = random.randrange(0, 100000000)
        cursor.execute("SELECT * FROM perform WHERE aid = :a AND sid = :s", {"a": aid, "s": sid})
        if not cursor.fetchall():
            return sid

def find_top_fans():
    """Find top fans and playlists."""
    global connection, cursor, aid
    cursor.execute(
        """
        SELECT u.uid, SUM(l.cnt) * so.duration
        FROM users u, sessions se, listen l, songs so, perform p
        WHERE u.uid = se.uid 
        AND se.sno = l.sno 
        AND u.uid = l.uid
        AND l.sid = p.sid 
        AND p.aid = :aid
        AND l.sid = so.sid
        GROUP BY u.uid
        ORDER BY SUM(l.cnt) * so.duration DESC
        LIMIT 3;
        """, {"aid": aid}
    )
    rows = cursor.fetchall()
    if not rows:
        print("Sorry, no users have listen to your songs.")
        return
    print("Id of top 3 users who listen to your songs the longest time are:", end=" ")
    for row in rows:
        print(row[0], end=" | ")
    print("")



def main():
    global connection, cursor, aid
    while True:
        mode = input("Welcome! You have signed in as " + aid +
                     "(artist).\nChoose 1 to add a new song, choose 2 to find top fans and playlists, 3 to logout, "
                     "else to exit program: ")
        if mode == "1":
            add()
        elif mode == "2":
            find_top_fans()
        elif mode == "3":
            return 1
        else:
            return 0
