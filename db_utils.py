import sqlite3

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# ==================== GENERIC METHODS ====================

def get_field(card_id, field_name):
    """Récupère un champ spécifique d'une carte"""
    conn = get_db()
    query = f'SELECT {field_name} FROM cards WHERE id = ?'
    result = conn.execute(query, (card_id,)).fetchone()[0]
    conn.close()
    return result

def set_field(card_id, field_name, value):
    """Met à jour un champ spécifique d'une carte"""
    conn = get_db()
    query = f'UPDATE cards SET {field_name} = ? WHERE id = ?'
    conn.execute(query, (value, card_id))
    conn.commit()
    conn.close()

# ==================== SPECIFIC METHODS ====================

def add_card(chinese, pinyin, french, hsk_level=1):
    conn = get_db()
    conn.execute('INSERT INTO cards (chinese, pinyin, french, hsk_level) VALUES (?, ?, ?, ?)',
                 (chinese, pinyin, french, hsk_level))
    conn.commit()
    conn.close()

def get_all_cards():
    conn = get_db()
    cards = conn.execute('SELECT * FROM cards ORDER BY date_added DESC').fetchall()
    conn.close()
    return cards

def get_cards_count():
    conn = get_db()
    count = conn.execute('SELECT COUNT(*) FROM cards').fetchone()[0]
    conn.close()
    return count

def delete_card(card_id):
    conn = get_db()
    conn.execute('DELETE FROM cards WHERE id = ?', (card_id,))
    conn.commit()
    conn.close()

# ==================== ALIASES (pour compatibilité) ====================

# === GET === #
def get_card_difficulty(card_id):
    return get_field(card_id, 'difficulty')

def get_card_name(card_id):
    return get_field(card_id, 'chinese')

def get_card_last_reviewed(card_id):
    return get_field(card_id, 'last_reviewed')

# === SET === #
def set_card_chinese(card_id, value):
    set_field(card_id, 'chinese', value)
    
def set_card_pinyin(card_id, value):
    set_field(card_id, 'pinyin', value)

def set_card_french(card_id, value):
    set_field(card_id, 'french', value)

def set_card_hsk_level(card_id, value):
    set_field(card_id, 'hsk_level', value)
    
def set_card_difficulty(card_id, value):
    set_field(card_id, 'difficulty', value)

def set_card_last_reviewed(card_id, value):
    set_field(card_id, 'last_reviewed', value)