from flask import Flask
from models.word import db, Word, create_tables
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/words.db"

words_list = ["Stern", "Stand", "Stamm", "Stein", "Staub", "Sturm", "Stadt",
              "Stufe", "Stiel", "Blatt", "Blüte", "Block", "Blase", "Blick",
              "Blech", "Blend", "Blitz", "Bleib", "Rasch", "Hasse"]


def words_2_db(words: list) -> None:
    for word in words:
        try:
            new_word = Word(word)
            db.session.add(new_word)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            print(f"Das Wort '{word}' existiert bereits in der Datenbank.")


if __name__ == '__main__':
    with app.app_context():
        create_tables()
        db.init_app(app)
        words_2_db(words_list)
