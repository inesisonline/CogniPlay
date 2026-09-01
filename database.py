import sqlite3
import bcrypt
#import os

connection = sqlite3.connect("cogniplay.db") #create db

cursor = connection.cursor() #communication with db

command = ("CREATE TABLE IF NOT EXISTS Users("
           "UserID INTEGER PRIMARY KEY AUTOINCREMENT,"
           "Username TEXT UNIQUE NOT NULL,"
           "Password TEXT NOT NULL,"
           "CreatedAt TEXT DEFAULT CURRENT_TIMESTAMP)")

cursor.execute(command)

command2 = ("CREATE TABLE IF NOT EXISTS Progress("
            "Id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "UserID INTEGER NOT NULL,"
            "Game TEXT NOT NULL,"
            "Level INTEGER DEFAULT 1,"
            "MaxPoints INTEGER DEFAULT 0,"
            "LastSession TEXT DEFAULT CURRENT_TIMESTAMP,"
            "FOREIGN KEY (UserID) REFERENCES Users(UserID),"
            "UNIQUE (UserID, Game))")

cursor.execute(command2)

def create_password_hash(password_text):
    password_bytes = password_text.encode('utf-8')
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password_bytes, salt)
    return password_hash

def verify_password(written_password, saved_hash):
    password_bytes = written_password.encode('utf-8')

    if bcrypt.checkpw(password_bytes, saved_hash):
        return True
    else:
        return False

def register_user(username, password):
    connection = sqlite3.connect("cogniplay.db")
    cursor = connection.cursor()
    password_hash = create_password_hash(password)
    try:
        cursor.execute("INSERT INTO Users (Username, Password) VALUES (?, ?)",
                       (username, password_hash))
        connection.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    connection.close()
    return success

def login_user(username, password):
    connection = sqlite3.connect("cogniplay.db")
    cursor = connection.cursor()
    cursor.execute("SELECT UserID, Password FROM Users WHERE Username = ?", (username, ))
    row = cursor.fetchone()
    connection.close()

    if row is None:
        return None
    user_id, saved_hash = row
    if verify_password(password, saved_hash):
        return user_id 
    return None

def save_progress(user_id, game, level):
    connection = sqlite3.connect("cogniplay.db")
    cursor = connection.cursor()

    cursor.execute("SELECT Level FROM Progress WHERE UserID = ? AND Game = ?", (user_id, game))
    row = cursor.fetchone()

    if row is None:
        cursor.execute("INSERT INTO Progress (UserID, Game, Level) VALUES (?, ?, ?)",
                       (user_id, game, level))
    elif level > row[0]:
        cursor.execute("UPDATE Progress SET Level = ?, LastSession = CURRENT_TIMESTAMP "
                       "WHERE UserID = ? AND Game = ?",
                       (level, user_id, game))

    connection.commit()
    connection.close()

def load_progress(user_id, game):
    connection = sqlite3.connect("cogniplay.db")
    cursor = connection.cursor()
    cursor.execute("SELECT Level FROM Progress WHERE UserID = ? AND Game = ?", (user_id, game))
    row = cursor.fetchone()
    connection.close()

    # for new users
    if row is None:
        return 1
    return row[0]

connection.close() #close db