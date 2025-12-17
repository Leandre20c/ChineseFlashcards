from flask import Flask, render_template, request, redirect
from db_utils import *
import random
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def library(msg:str=None):
    if msg:
        return render_template('library.html', message=msg, cards=get_all_cards())
    else:
        return render_template('library.html', cards=get_all_cards())

@app.route('/review')
def review():
    cards = get_all_cards()
    if cards == []:
        return render_template('review.html', error='Pas de cartes disponibles.')
    
    curr_card = get_next_review_card()
    return render_template('review.html', card=curr_card, now=datetime.now().isoformat())


@app.route('/append', methods=['POST'])
def append():
    if request.method == 'POST':
        # Take all fields
        chinese = request.form['chinese']
        pinyin = request.form['pinyin']
        french = request.form['french']
        hsk_level = request.form.get('hsk_level', 1)

        # Append the card to the db
        add_card(chinese, pinyin, french, hsk_level)
        
        #card_added_message = f'Ajouté {chinese}.\n Total: {get_cards_count()}.'
        
        return redirect('/')
    
@app.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        card_id = request.form['card_id']
        
        #card_removed_message = f'Carte {get_card_name(card_id)} supprimée.'
        
        delete_card(card_id)
        
        return redirect('/')
        
@app.route('/mark-reviewed', methods=['POST'])
def mark_reviewed():
    card_id = request.form['card_id']
    difficulty_response = int(request.form['difficulty'])
    
    # Met à jour la difficulté
    current_difficulty = get_field(card_id, 'difficulty')
    
    if difficulty_response == 0:  # Oublié
        new_difficulty = max(0, current_difficulty - 5)
        next_review = datetime.now() + timedelta(hours=10)  # Revoir vite
    elif difficulty_response == 1:  # Dur
        new_difficulty = max(0, current_difficulty - 2)
        next_review = datetime.now() + timedelta(days=1)
    elif difficulty_response == 2:  # Moyen
        new_difficulty = current_difficulty
        next_review = datetime.now() + timedelta(days=3)
    elif difficulty_response == 3:  # Facile
        new_difficulty = min(20, current_difficulty + 2)
        next_review = datetime.now() + timedelta(days=7)
    else:  # Parfait
        new_difficulty = min(20, current_difficulty + 5)
        next_review = datetime.now() + timedelta(days=14)
    
    set_field(card_id, 'difficulty', new_difficulty)
    set_field(card_id, 'last_reviewed', datetime.now().isoformat())
    set_field(card_id, 'next_review_date', next_review.isoformat())
    
    return redirect('/review')

@app.route('/update', methods=['POST'])
def edit():
    if request.method == 'POST':
        card_id = request.form['card_id']
        new_chinese = request.form['chinese']
        new_pinyin = request.form['pinyin']
        new_french = request.form['french']
        new_hsk_level = request.form['hsk_level']
        
        set_card_chinese(card_id, new_chinese)
        set_card_pinyin(card_id, new_pinyin)
        set_card_french(card_id, new_french)
        set_card_hsk_level(card_id, new_hsk_level)
        
        return redirect('/')


def get_next_review_card():
    """
    Retourne la carte la plus prioritaire à réviser
    Priorité :
    1. Cartes jamais révisées (next_review_date IS NULL)
    2. Cartes dont la date de révision est dépassée
    3. Si aucune carte due, retourne la carte la plus proche de sa date de révision
    """
    conn = get_db()
    
    card = conn.execute('''
        SELECT * FROM cards
        ORDER BY 
            CASE 
                WHEN next_review_date IS NULL THEN 0                    -- Jamais révisé = priorité 0 (max)
                WHEN next_review_date <= datetime('now') THEN 1         -- À réviser maintenant = priorité 1
                ELSE 2                                                   -- Pas encore due = priorité 2
            END,
            next_review_date ASC                                         -- Dans chaque groupe, tri par date
        LIMIT 1
    ''').fetchone()
    
    conn.close()
    return card

        
if __name__ == '__main__':
    app.run(debug=True)