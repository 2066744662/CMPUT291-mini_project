# Robbie Feng
import sqlite3
from getpass import getpass

global connection, cursor


def connect(connection1, cursor1):
    global connection, cursor
    connection = connection1
    cursor = cursor1
    return


def login():
    """login system
    :rtype: tuple
    :return: user/artist and id
    """
    id = input("Please input your id: ")
    pwd = getpass("Please input your password: ")
    return check(id, pwd)


def check(id, pwd):
    """Check if id and pwd are valid, and find if id is aid or uid.
        :param: id, pwd
        :type: string
        :rtype: tuple
        :return: user/artist and id
        """
    # find valid user
    user = None
    cursor.execute("""
    Select uid
    FROM users u
    WHERE u.uid = :id AND u.pwd = :pwd
    """, {'id': id, 'pwd': pwd})
    data = cursor.fetchall()
    if data:
        user = ("users", data[0][0])
    # find valid artist
    cursor.execute("""
        Select aid
        FROM artists a
        WHERE a.aid = :id AND a.pwd = :pwd
        """, {'id': id, 'pwd': pwd})
    data = cursor.fetchall()
    if data and not user:
        user = ("artists", data[0][0])
    elif data:  # if both user and artist valid, prompt to choose
        option = "C"
        while True:
            option = input("Please choose your login option:\n1: user    2:artist\n")
            if option in ["1"]:
                break
            elif option in ["2"]:
                user = ("artists", data[0][0])
                break
            else:
                print("Error input! Please input either \"1\"or \"2\"\n")
    return user

def register():
    """ unregistered users sign up by providing uid, name, password"""
    uid = input("Enter your user ID: ")
    #check if user ID is unique
    while True:
        cursor.execute("""
                Select name
                FROM  users
                WHERE uid = :id
                """, {'id': uid})
        data = cursor.fetchall()
        if not data:
            break
        else:
            uid = input("User ID already exists. PLease enter another user ID: ")
    name = input("Enter your name: ")
    #check if name is valid
    while name.isalpha() == 0:
        name = input("Invalid name input, please enter a valid name: ")
    pwd = input("Enter your password: ")
    cursor.execute('INSERT INTO users VALUES (:id,:name,:pwd)', {"id": uid, "name": name, "pwd": pwd})

def main():
    """Main screen of the program, also the login screen"""
    while True:
        option = input("Welcome!\nChoose 1 to login, 2 to register a user, 3 if you forget your password, 0 to exit: ")
        if option == "1":
            user = login()
            if user is None:
                print("Invalid id or password\n")
                continue
            return user
        if option == "2":
            register()
            pass
        if option == "0":
            break
        if option == "3":
            print("So sad. But you can register a new account :).")
