import sqlite3
from datetime import datetime

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''
    UPDATE cards 
    SET next_review_date = datetime('now')
    WHERE next_review_date IS NULL
''')

rows_updated = c.rowcount
conn.commit()
conn.close()

print(f"✅ {rows_updated} cartes initialisées avec next_review_date")
print("Toutes tes cartes existantes sont maintenant disponibles pour révision !")