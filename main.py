import sqlite3
import login
import artist
import userfunctions

connection = None
cursor = None


def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return


def run_file(file):
    global connection, cursor
    with open(file, 'r') as f:
        script = f.read()
    cursor.executescript(script)

def create_test():
    global connection, cursor
    path = "./data.db"
    connect(path)
    run_file("prj-tables.txt")  # define table
    run_file("testdata.txt")  # test
    print("Remember to delete this")

def main():
    global connection, cursor
    #path = input("Input .db path: ")
    #connect(path)
    create_test()# delete me
    login.connect(connection, cursor)  # load global variable to other package
    while True:
        user = login.main()  # go to login screen
        if user is None:
            # Close everything
            break
        if user[0] == "users":
            # Go to user function screen
            userfunctions.menu(user[1])
            pass  # if  user decides to logout
            # break # if user decides to exit
        elif user[0] == "artists":
            # Go to artist function screen
            artist.connect(connection, cursor, user)
            ret = artist.main()
            if ret == 1:
                pass
            else:
                break
    connection.close()
    print("End.")

if __name__ == "__main__":
    main()
