import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chinese TEXT NOT NULL,
        pinyin TEXT NOT NULL,
        french TEXT NOT NULL,
        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_reviewed TIMESTAMP,
        hsk_level INTEGER DEFAULT 1,
        difficulty INTEGER DEFAULT 0,
    )
''')

conn.commit()
conn.close()
