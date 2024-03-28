from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/words.db"

db = SQLAlchemy(app)


class Word(db.Model):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True)
    word = Column(String(5), unique=True, nullable=False)

    def __init__(self, word: str) -> None:
        self.word: str = word


def create_tables():
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
