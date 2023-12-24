from flask import Flask, render_template, jsonify, request
from random import choice
import os
import re

app = Flask(__name__)

words = ["Stern", "Stand", "Stamm", "Stein", "Staub", "Sturm", "Stadt", "Stufe", "Stiel", "Blatt",
         "Blüte", "Block", "Blase", "Blick", "Blech", "Blend", "Blitz", "Bleib", "Rasch", "Hasse"]
possible_words = words.copy()
# SPÄTER BEARBEITEN / TODO: Die daten schon in uppercase speichern und zeile löschen
possible_words = [word.upper() for word in possible_words]

TARGET_WORD = choice(possible_words)

first_round = True

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
    return render_template('template.html', title='Nicht wördeln!', game_content=game_content)


@app.route('/check_word', methods=['POST'])
def check_word():
    global first_round
    global TARGET_WORD  # import Target word
    global possible_words  # import possible words
    user_input = request.json['word'].upper()  # import user input
    feedback = []  # the list that will send to user

    # Zählen, wie oft jeder Buchstabe im Zielwort vorkommt
    letter_counts = {char: TARGET_WORD.count(char) for char in set(TARGET_WORD)}

    # RegEx-Pattern
    pattern = "^"
    for i, char in enumerate(user_input):

        if char == TARGET_WORD[i]:
            # Richtiger Buchstabe an der richtigen Stelle
            feedback.append({"letter": char, "position": i, "status": "correct"})
            letter_counts[char] -= 1
            pattern += char

        elif char in TARGET_WORD and letter_counts[char] >= 1:
            # Buchstabe ist im Wort, aber an falscher Stelle
            feedback.append({"letter": char, "position": i, "status": "maybe"})
            letter_counts[char] -= 1
            pattern += "(?!{})".format(char)  # RegEx sagt wort enthält char, aber nicht an der Stelle i

        else:
            # Buchstabe nicht im Wort
            feedback.append({"letter": char, "position": i, "status": "incorrect"})
            pattern += "." # RegEx sagt wort enthält beliebigen Buchstaben

    pattern += "$"  # Ende des Regex-Musters

    # Filtern der möglichen Wörter
    possible_words = [word for word in possible_words if re.fullmatch(pattern, word)]

    # Wählen eines neuen Zielworts für die nächste Runde
    if not first_round:
        new_word(False)
    else:
        first_round = False
        new_word(first_round)

    """ Daten für die Rückgabe Beispiel:
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
    # print(f"{feedback} und {len(possible_words)}, wurde mit {pattern} gefiltert")
    return jsonify({'info': feedback, 'possible_words': len(possible_words)})


# Neues Zielwort auswählen
def new_word(first_round):
    global TARGET_WORD
    global possible_words

    if not first_round:
        if TARGET_WORD in possible_words:
            possible_words.remove(TARGET_WORD)  # Entfernen des aktuellen Zielworts aus der Liste, falls vorhanden

    if possible_words:  # Überprüfen, ob die Liste noch Elemente enthält
        TARGET_WORD = choice(possible_words)  # Wählen eines neuen Zielworts
        possible_words.append(TARGET_WORD)  # Hinzufügen des neuen Zielworts zur Liste


if __name__ == '__main__':
    new_word()
    app.run(debug=True)
