import sqlite3 as sql
import bcrypt
from tkinter import messagebox as mb


def hash_password(pas: str):  # Improved security with hashed password
    password = pas.encode('utf-8')  # to bytes

    salt = bcrypt.gensalt()  # Generates random salt

    hashed_password = bcrypt.hashpw(password, salt)

    return hashed_password


def create_table():
    connection = sql.connect('./database/users.db')

    confirmed = False

    query = '''CREATE TABLE users (
            id INTEGER NOT NULL,
            name TEXT NOT NULL DEFAULT Unknown,
            user TEXT NOT NULL UNIQUE,
            password BLOB NOT NULL,
            PRIMARY KEY (id AUTOINCREMENT)
            )'''
    try:
        with connection:
            connection.execute(query)

        confirmed = True

    except sql.Error:
        confirmed = False

    connection.close()
    return confirmed


def new_user(name: str, user: str, pas: str):
    create_table()  # Creates database if it doesn't exists

    password = hash_password(pas)

    connection = sql.connect('./database/users.db')

    # Main query
    query = 'INSERT INTO users (name, user, password) VALUES (?, ?, ?)'

    confirmed = True

    try:
        with connection:  # Execute insertion
            connection.execute(query, (name, user, password))

    except sql.IntegrityError:  # Raise error if 'user' already exists (UNIQUE)
        mb.showerror(
            title='Error',
            message='User already exists'
        )

        confirmed = False

    connection.close()

    return confirmed


def fetch_user(user: str, pas: str):
    create_table()  # Creates database if it doesn't exists

    connection = sql.connect('./database/users.db')

    query = 'SELECT * FROM users WHERE user = ?'  # Select entire row

    res = connection.execute(query, (user,)).fetchone()

    connection.close()

    if not res:  # If user is not in the database, return NONE
        return None

    db_password = res[3]  # id - name - user - [password]

    if not bcrypt.checkpw(pas.encode('utf-8'), db_password):
        return None  # If password is incorrect, return NONE

    res = [x for x in res]

    return res


def fetch_user_id(id: int):
    if create_table():  # Creates database if it doesn't exists
        mb.showwarning(  # Return if it is empty
            title='No data',
            message='This database has no data'
        )

        return None

    connection = sql.connect('./database/users.db')

    query = 'SELECT * FROM users WHERE id = ?'

    res = connection.execute(query, (id,)).fetchone()

    connection.close()

    if not res:
        return None

    res = [x for x in res]

    return res


def last_user_id():
    create_table()

    connection = sql.connect('./database/users.db')

    query = 'SELECT id FROM users ORDER BY id DESC'

    res = connection.execute(query).fetchone()

    connection.close()

    if not res:  # If no users in db, return the first ID that will be created
        return '1'

    # Autoincrement new id
    res = str(int(res[0] + 1))

    return res
