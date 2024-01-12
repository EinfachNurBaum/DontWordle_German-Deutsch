from flask import Flask, render_template, jsonify, request
from random import choice
import os
import re

app = Flask(__name__)

words = []
possible_words = []
TARGET_WORD = ""


def prepare_game_start():
    global words
    global possible_words
    global TARGET_WORD
    words = ["Stern", "Stand", "Stamm", "Stein", "Staub", "Sturm", "Stadt", "Stufe", "Stiel", "Blatt",
             "Blüte", "Block", "Blase", "Blick", "Blech", "Blend", "Blitz", "Bleib", "Rasch", "Hasse"]
    possible_words = words.copy()
    # SPÄTER BEARBEITEN / TODO: Die daten schon in uppercase speichern und zeile löschen
    possible_words = [word.upper() for word in possible_words]

    TARGET_WORD = choice(possible_words)

    first_round = True


@app.route('/')
def home():
    prepare_game_start()

    word_count = len(possible_words)
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
        
        <!-- Neue Box für das letzte Wort und den Teilen-Button -->
        <div class='final-word-container'>
            <div class='final-word'>Letztes Wort: <span id='final-word'></span></div>
                <button class='share-button' onclick='shareResults()'>Teilen</button>
        </div>
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
    cell_row = request.json['cell_row']  # Empfangen der cell_row Information vom Frontend
    feedback = []  # the list that will send to user

    # Zählen, wie oft jeder Buchstabe im Zielwort vorkommt
    letter_counts = {char: TARGET_WORD.count(char) for char in TARGET_WORD}

    # RegEx-Pattern
    # Initialisieren der Regex-Patterns
    pattern_green = "^"  # Für korrekte Buchstaben an der richtigen Stelle
    pattern_yellow_array = []  # Für korrekte Buchstaben an der falschen Stelle

    print("Target word: " + TARGET_WORD)

    for i, char in enumerate(user_input):

        if char == TARGET_WORD[i]:
            # Richtiger Buchstabe an der richtigen Stelle
            feedback.append({"letter": char, "position": i, "status": "correct"})
            letter_counts[char] -= 1
            pattern_green += char

        elif (char in TARGET_WORD) and letter_counts[char] >= 1:
            # Zur ner unbekannte wahrscheinlichkeit macht (char in TARGET_WORD) fehler, darum doppel checken wir
            print(char, TARGET_WORD, char in TARGET_WORD)
            # Buchstabe ist im Wort, aber an falscher Stelle
            feedback.append({"letter": char, "position": i, "status": "maybe"})
            pattern_yellow_array.append(char)  # Stellt sicher, dass das Wort den Buchstaben irgendwo hat
            letter_counts[char] -= 1
            pattern_green += "."  # Ersetzt den Platzhalter für die falsche Position

        else:
            # Buchstabe nicht im Wort
            feedback.append({"letter": char, "position": i, "status": "incorrect"})
            pattern_green += "."  # Ersetzt den Platzhalter für die falsche Position

    pattern_green += "$"  # Ende des Regex-Musters

    # Filtern der möglichen Wörter, die im Wort pattern_green Buchstaben haben, an der richtigen Stelle
    possible_words_green_filtered = [word for word in possible_words if re.fullmatch(pattern_green, word)]

    # Filtern der möglichen Wörter, die im Wort pattern_yellow Buchstaben haben, an der zufälligen Stelle
    possible_words_yellow_filtered = []
    for char in pattern_yellow_array:  # set() entfernt Duplikate, aber das wollen wir hier nicht, z.B. bei "Stamm"
        possible_words_yellow_filtered = [word for word in possible_words_green_filtered if char in word]

    # Überprüfung auf Gewinn oder Verlust und Rückgabe des finalen Worts
    if len(possible_words_green_filtered) == 1 and user_input == TARGET_WORD:
        game_status = 'win'
    elif cell_row == 0 and user_input != TARGET_WORD:
        game_status = 'lose'
    else:
        game_status = 'continue'

    # Wählen eines neuen Zielworts für die nächste Runde
    if not first_round and game_status == 'continue':
        new_word(False)
    elif game_status == 'continue':
        first_round = False
        new_word(first_round)

    # Ermitteln des finalen Worts
    final_word = TARGET_WORD if len(possible_words_yellow_filtered) <= 1 else None

    print(f'''
    Target word: {TARGET_WORD}
    User input: {user_input}
    Feedback: {feedback}
    Possible words: {possible_words}
    Possible words green filtered: {possible_words_green_filtered}
    Possible words yellow filtered: {possible_words_yellow_filtered}
    Game status: {game_status}
    final word: {final_word}
    green pattern: {pattern_green}
    yellow pattern: {pattern_yellow_array}
    first round: {first_round}
    game status: {game_status}
    len possible words yellow filtered: {len(possible_words_yellow_filtered)}
    ''')

    return jsonify({
        'info': feedback,
        'possible_words': len(possible_words_yellow_filtered),
        'game_status': game_status,
        'final_word': final_word
    })


# Neues Zielwort auswählen
def new_word(first_round_param):
    global TARGET_WORD
    global possible_words

    if not first_round_param:
        if TARGET_WORD in possible_words:
            possible_words.remove(TARGET_WORD)  # Entfernen des aktuellen Zielworts aus der Liste, falls vorhanden

    if possible_words:  # Überprüfen, ob die Liste noch Elemente enthält
        TARGET_WORD = choice(possible_words)  # Wählen eines neuen Zielworts



if __name__ == '__main__':
    app.run(debug=True)
