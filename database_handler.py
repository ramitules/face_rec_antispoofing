import sqlite3 as sql
from tkinter import messagebox as mb


def create_table():
    connection = sql.connect('./database/users.db')

    query = '''CREATE TABLE users (
            id INTEGER NOT NULL,
            name TEXT NOT NULL DEFAULT Unknown,
            user TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            PRIMARY KEY (id AUTOINCREMENT)
            )'''
    try:
        with connection:
            connection.execute(query)

        mb.showinfo(
            title='No database',
            message='There was no database. New one created successfully'
        )

    except sql.Error:
        return


def new_user(name: str, user: str, pas: str):
    create_table()

    connection = sql.connect('./database/users.db')

    # Main query
    query = 'INSERT INTO users (name, user, password) VALUES (?, ?, ?)'

    confirmed = True

    try:
        with connection:  # Execute insertion
            connection.execute(query, (name, user, pas))

    except sql.IntegrityError:  # Raise error if 'user' already exists (UNIQUE)
        mb.showerror(
            title='Error',
            message='User already exists'
        )

        confirmed = False

    connection.close()

    return confirmed


def fetch_user(user: str, pas: str):
    create_table()

    connection = sql.connect('./database/users.db')

    query = 'SELECT * FROM users WHERE user = ? AND password = ?'

    res = connection.execute(query, (user, pas)).fetchone()

    confirmed = True

    if not res:
        mb.showerror(
            title='Not found',
            message='User not found'
        )

        confirmed = False

    connection.close()

    return confirmed
