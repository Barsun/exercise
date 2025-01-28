import sqlite3

def init_db():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_item(name, description):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO items (name, description) VALUES (?, ?)
    ''', (name, description))
    conn.commit()
    conn.close()