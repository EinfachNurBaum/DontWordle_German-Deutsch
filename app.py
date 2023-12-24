from flask import Flask, render_template, jsonify, request
from random import choice
import os
import re

app = Flask(__name__)

words = ["Stern", "Stand", "Stamm", "Stein", "Staub", "Sturm", "Stadt", "Stufe", "Stiel", "Blatt",
         "Blüte", "Block", "Blase", "Blick", "Blech", "Blend", "Blitz", "Bleib", "Rasch", "Hasse"]
TARGET_WORD = "Stern"
possible_words = words.copy()


@app.route('/')
def home():
    word_count = len(words)
    game_content = """
    <div class='grid-container'>
        <!-- Übrige Wörter: Zeigt die Anzahl der verbleibenden Wörter an -->
        <div class='words-left'>Übrige Wörter: <span class='score-count' id='words-left-count'>""" + f'{word_count}' + """</span></div>
        
        <!-- Verbliebene Zurücknahme: Zeigt die Anzahl der verbleibenden Zurücknahmen an -->
        <div class='words-right'>Verbliebene Zurücknahme: <span class='score-count' id='undo-count'>5</span></div>
        
        <!-- Spielraster: Hier werden die Buchstabenboxen generiert -->
        <div class='game-grid'>
            """ + ''.join([
        '<div class="game-row">' + ''.join(
            [f'<div class="game-cell" id="cell-{row}-{col}"></div>' for col in range(5)]
        ) + '</div>' for row in range(6)
    ]) + """
        </div>
        
        <!-- Eingabefeld: Textfeld, in das der Benutzer tippt -->
        <div class='input-box'><input type='text' class='input-rounded' id='textbox' autofocus></div>
    </div>
    """
    print(os.getcwd())
    return render_template('./template.html', title='Nicht wördeln!', game_content=game_content)


@app.route('/check_word', methods=['POST'])
def check_word():
    global TARGET_WORD  # import Target word
    global possible_words  # import possible words
    user_input = request.json['word'].upper()  # import user input
    feedback = []  # the list that will send to user

    # RegEx-Pattern
    pattern = ""

    for i, char in enumerate(user_input):
        if char == TARGET_WORD[i].upper():
            pattern += char  # Buchstabe ist korrekt und an der richtigen Stelle
            feedback.append({'letter': char, 'position': i, 'status': 'correct'})
        else:
            pattern += '.'  # Buchstabe ist unbestimmt

    # Filtern der möglichen Wörter
    possible_words = [word for word in possible_words if re.fullmatch(pattern, word)]

    """ Mockdaten
    info = {
        "info": [
        {"letter": "S", "position": 0, "status": "correct"},
        {"letter": "T", "position": 1, "status": "incorrect"},
        {"letter": "E", "position": 2, "status": "maybe"},
        {"letter": "R", "position": 3, "status": "maybe"},
        {"letter": "N", "position": 4, "status": "correct"}
    ]
    }
    return jsonify(info)"""
    print(f"{feedback} und {len(possible_words)}")
    return jsonify({'info': feedback, 'possible_words': len(possible_words)})


def new_word():
    global TARGET_WORD
    TARGET_WORD = choice(words)


if __name__ == '__main__':
    new_word()
    app.run(debug=True)
