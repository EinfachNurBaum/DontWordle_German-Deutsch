import json
from models.word import db, Word, create_tables
from sqlalchemy.exc import IntegrityError
from flask import Flask

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/words.db"


def word_generator(file_path):
    # Überprüfen, ob die Datei eine JSON-Datei ist
    if file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as file:
            words_list = json.load(file)
    # Angenommen, es ist eine Textdatei
    else:
        with open(file_path, 'r', encoding='utf-8') as file:
            words_list = file.readlines()

    # Wörter filtern, die genau 5 Buchstaben lang sind
    for word in words_list:
        # Entfernen Sie eventuelle Leerzeichen am Anfang und am Ende der Zeile
        word = word.strip()
        if len(word) == 5:
            yield word


def word_2_db(file_path):
    # Wörter in die Datenbank einfügen
    for word in word_generator(file_path):
        try:

            new_word = Word(word=word)
            db.session.add(new_word)

            # Änderungen in der Datenbank speichern
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            print(f"Das Wort '{word}' existiert bereits in der Datenbank.")


if __name__ == '__main__':
    # Pfad zur JSON-Datei
    # file_path = 'woerter/German-words-1600000-words-multilines.json'
    # file_path = 'woerter/Adjektive/Adjektive.txt'
    # file_path = 'woerter/Substantive/substantiv_singular_das.txt'
    # file_path = 'woerter/Substantive/substantiv_singular_der.txt'
    # file_path = 'woerter/Substantive/substantiv_singular_die.txt'
    # file_path = 'woerter/Verben/Verben_regelmaesig.txt'
    file_path = 'woerter/Verben/Verben_unregelmaeßig_Infinitiv.txt'
    with app.app_context():
        create_tables()
        db.init_app(app)
        word_2_db(file_path)
