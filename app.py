import logging
import re
from os import access, R_OK, stat
from random import choice
from sys import exit
from flask import Flask, render_template, jsonify, request

app = None

try:
    logging.basicConfig(filename='app.log', level=logging.DEBUG)  # Konfigurieren des Loggings
    logger = logging.getLogger('werkzeug')
    logger.setLevel(logging.WARNING)
except Exception as e:
    logging.error("Logging Datei access: " + str(access('app.log', R_OK)))
    logging.error("Logging Datei stat: " + str(stat('app.log')))
    logging.error("Die Logging Datei konnte nicht erstellt werden.\n" + str(e))
    exit(1)

try:
    app = Flask(__name__)
except Exception as e:
    logging.error("Die App konnte nicht initialisiert werden.\n" + str(e))
    exit(1)

possible_words = []
TARGET_WORD = ""
final_word = None


def getWordListFromFile():
    try:
        with open('words.txt', 'r') as f:
            return f.read().splitlines()
    except Exception as e:
        logging.error("Logging Datei access: " + str(access('words.txt', R_OK)))
        if access('words.txt', R_OK):
            logging.error("Logging Datei stat: " + str(stat('words.txt')))
        logging.error("Wenn könnte die Words.txt nicht gelesen, oder die Datei wurde gelöscht.\n" + str(e))
        print("Bitte die app.log Datei überprüfen.")
        exit(1)


@app.route('/get_word_list')
def get_word_list():
    liste = getWordListFromFile()
    return jsonify({'word_list': liste})


def prepare_game_start():
    global possible_words
    global TARGET_WORD

    possible_words = getWordListFromFile()

    if len(possible_words) == 0:
        logging.error("No words found in words.txt")
        print("Bitte die app.log Datei überprüfen.")
        exit(1)

    TARGET_WORD = choice(possible_words)
    TARGET_WORD = "KÜCHE"


@app.route('/')
def home():
    prepare_game_start()

    word_count = len(possible_words)
    game_content = """
    <div class='grid-container'>
        <!-- Übrige Wörter: Zeigt die Anzahl der verbleibenden Wörter an -->
        <div class='words-left' >Übrige Wörter: <span class='score-count' id='words-left-count'>""" + f'{word_count}' + """</span></div>
        
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
    return render_template('template.html', title='Nicht wördeln!', game_content=game_content)


@app.route('/check_word', methods=['POST'])
def check_word():
    global TARGET_WORD  # import Target word
    global possible_words  # import possible words
    global final_word  # import final word

    user_input = request.json['word'].upper()  # import user input
    cell_row = request.json['cell_row']  # Empfangen der cell_row Information vom Frontend
    feedback = []  # Feedback-Liste, die die USer inputs enthält

    # Zählen, wie oft jeder Buchstabe im Zielwort vorkommt
    user_counts = {char: user_input.count(char) for char in user_input}

    MultipleLetters = {}

    # RegEx-Pattern
    # Initialisieren der Regex-Patterns
    pattern_green = "^"  # Für korrekte Buchstaben an der richtigen Stelle
    pattern_yellow_array = []  # Für korrekte Buchstaben an der falschen Stelle

    logging.debug(f"Target word: {TARGET_WORD}")

    for i, char in enumerate(user_input):

        if char == TARGET_WORD[i]:
            # Richtiger Buchstabe an der richtigen Stelle
            feedback.append({"letter": char, "position": i, "status": "correct"})
            pattern_green += char
            if user_counts[char] > 1 and MultipleLetters.get(char) is None:
                MultipleLetters[char] = user_counts[char]


        elif char in TARGET_WORD:
            # Buchstabe ist im Wort, aber an falscher Stelle
            feedback.append({"letter": char, "position": i, "status": "maybe"})
            pattern_yellow_array.append(char)  # Stellt sicher, dass das Wort den Buchstaben irgendwo hat
            pattern_green += "."  # Ersetzt den Platzhalter für die falsche Position
            if user_counts[char] > 1 and MultipleLetters.get(char) is None:
                MultipleLetters[char] = user_counts[char]

        else:
            # Buchstabe nicht im Wort
            feedback.append({"letter": char, "position": i, "status": "incorrect"})
            pattern_green += "."  # Ersetzt den Platzhalter für die falsche Position

    pattern_green += "$"  # Ende des Regex-Musters

    # Filtern der möglichen Wörter, die im Wort pattern_green Buchstaben haben, an der richtigen Stelle
    possible_words_green_filtered = [word for word in possible_words if re.fullmatch(pattern_green, word)]

    # Filtern den möglichen Wörtern. User input hatte richtige Buchstaben an der falschen Stelle
    possible_words_yellow_filtered = []
    if len(pattern_yellow_array) > 0:
        for yp_char in pattern_yellow_array:
            for word in possible_words_green_filtered:
                if word.count(yp_char) == 1:
                    possible_words_yellow_filtered.append(word)

    logging.debug("Diese Liste sollte richtige Buchstabe an der falschen Stelle haben:")
    logging.debug(f"Erste 20 Wörter sind: {possible_words_yellow_filtered[:20]}")
    logging.debug(f"Letzte 20 Wörter sind: {possible_words_yellow_filtered[-20:]}")

    # Erstellen einer Liste die Wörter besitzt, die von den User gefundene doppele Buchstaben enthält
    if len(MultipleLetters) > 0:
        possible_words_prepared = []
        for char in MultipleLetters.keys():
            for word in possible_words_yellow_filtered:
                if word.count(char) == MultipleLetters[char]:
                    if word not in possible_words_prepared:
                        possible_words_prepared.append(word)
    else:
        possible_words_prepared = possible_words_yellow_filtered

    possible_words = possible_words_prepared.copy()

    logging.debug(f"Target word: {TARGET_WORD}")
    logging.debug(f"User input: {user_input}")
    logging.debug(f"Feedback: {feedback}")
    logging.debug(f"erste Possible words green filtered: {possible_words_green_filtered[:10]}")
    logging.debug(f"letzte Possible words green filtered: {possible_words_green_filtered[-10:]}")
    logging.debug(f"erste Possible words yellow filtered: {possible_words_yellow_filtered[:10]}")
    logging.debug(f"letzte Possible words yellow filtered: {possible_words_yellow_filtered[-10:]}")
    logging.debug(f"green pattern: {pattern_green}")
    logging.debug(f"yellow pattern: {pattern_yellow_array}")
    logging.debug(f"Liste der mehrmals vorkommenden Buchstaben: {MultipleLetters}")
    logging.debug(f"len possible words yellow filtered: {len(possible_words_yellow_filtered)}")

    if user_input in possible_words and len(possible_words) > 1 and final_word is None:
        possible_words.remove(
            user_input)  # Entfernen des aktuellen Benutzerworts aus der Liste der möglichen Wörter

    # Überprüfung auf Gewinn oder Verlust und Rückgabe des finalen Worts
    if len(possible_words) == 1 and user_input == TARGET_WORD:
        game_status = 'win'
        logging.debug(f"User win with: {TARGET_WORD}")
    elif cell_row == 0 and user_input != TARGET_WORD:
        game_status = 'lose'
        logging.debug(f"User lose with: {TARGET_WORD}")
    else:
        game_status = 'continue'
        logging.debug(f"User continue")

    TARGET_WORD = choice(possible_words)  # Wählen eines neuen Zielworts

    # Ermitteln des finalen Worts
    final_word = TARGET_WORD if len(possible_words_yellow_filtered) <= 1 else None

    logging.debug("NACH REMOVE!")
    logging.debug(f"New Target word: {TARGET_WORD}")
    logging.debug(f"Final word: {final_word}")
    logging.debug(f"game status: {game_status}")
    logging.debug(f"len possible words yellow filtered: {len(possible_words)}")
    logging.debug(f"len possible words: {len(possible_words)}")
    logging.debug(f"erste 10 possible words: {possible_words[:10]}")
    logging.debug(f"letzte 10 possible words: {possible_words[-10:]}")

    return jsonify({
        'info': feedback,
        'possible_words': len(possible_words) if final_word is None and user_input is not final_word else 0,
        'game_status': game_status,
        'final_word': final_word
    })


if __name__ == '__main__':
    logging.info("App started")
    logging.info("App sollte Berechtigung haben Dateien in aktuellen Verzeichnis zu lesen und zu schreiben.")

    try:
        print("App gestartet unter http://127.0.0.1:5000/")
        print("Beachte http:// und nicht https:// in der URL.")
        app.run()
    except Exception as e:
        logging.error(
            "Die App konnte nicht gestartet werden. Wahrscheinlich ist der 5000er Port nicht frei \n" + str(e))
        try:
            app.run(port=5001)
            print("App gestartet unter http://127.0.0.1:5000/")
            print("Beachte http:// und nicht https:// in der URL.")
        except Exception as e:
            logging.error(
                "Die App konnte nicht mit anderen Port gestartet werden. Bitte Port angeben, wenn dass das Problem war. \n" + str(
                    e))
            print("Bitte die app.log Datei überprüfen.")
            exit(1)

    logging.info("App ended")
