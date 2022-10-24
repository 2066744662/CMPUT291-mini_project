import sqlite3
import login

connection = None
cursor = None
user = None


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


def main():
    global connection, cursor, user
    path = "./data.db"
    connect(path)
    run_file("prj-tables.txt")  # define table
    run_file("testdata.txt")  # test
    login.connect(connection, cursor) # load global variable to other package
    while True:
        user = login.main() # go to login screen
        if user is None:
            # Close everything
            print("End.")
            break
        if user[0] == "users":
            #Go to user function screen
            print("WIP")
            pass #if  user decides to logout
            #break # if user decides to exit
        elif user[0] == "artists":
            #Go to artist function screen
            print("WIP")
            pass  # if  user decides to logout
            #break  # if user decides to exit

if __name__ == "__main__":
    main()
