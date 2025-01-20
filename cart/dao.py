import os
import sqlite3
import json


def connect(path):
    exists = os.path.exists(path)
    conn = sqlite3.connect(path)
    if not exists:
        create_tables(conn)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS carts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            contents TEXT,
            cost REAL
        )
    ''')
    conn.commit()


def get_cart(username: str) -> dict:
    conn = connect('carts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM carts WHERE username = ?', (username,))
    cart = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if cart:
        return dict(cart)
    return None


def create_cart(username: str, contents: list[int]):
    conn = connect('carts.db')
    cursor = conn.cursor()
    contents_json = json.dumps(contents)
    cursor.execute('INSERT INTO carts (username, contents, cost) VALUES (?, ?, ?)',
                   (username, contents_json, 0))  # Set initial cost to 0
    conn.commit()
    cursor.close()
    conn.close()


def update_cart(username: str, contents: list[int]):
    conn = connect('carts.db')
    cursor = conn.cursor()
    contents_json = json.dumps(contents)
    cursor.execute('UPDATE carts SET contents = ? WHERE username = ?', (contents_json, username))
    conn.commit()
    cursor.close()
    conn.close()


def delete_cart(username: str):
    conn = connect('carts.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM carts WHERE username = ?', (username,))
    conn.commit()
    cursor.close()
    conn.close()

