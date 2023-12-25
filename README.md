# DON'T WORDLE (Work in Progress) 🔴

## Projektbeschreibung

DON'T WORDLE ist eine Variante des beliebten Worträtselspiels Wordle, bei dem du versuchen musst, das geheime Wort zu erraten. Dieses Projekt befindet sich derzeit in der Entwicklung und wird unregelmäßig weiterentwickelt.

## Anleitung (Aktuell)

### Schritt-für-Schritt-Anleitung für das Ausführen der Flask-App

Wenn du die Flask-App ausführen möchtest, um DON'T WORDLE lokal zu spielen, folge dieser Anleitung:

1. **Python und PyCharm**: Stelle sicher, dass du [Python](https://www.python.org/)  auf deinem Computer installiert hast. Wir empfehlen die Verwendung von [PyCharm](https://www.jetbrains.com/pycharm/download/), einer beliebten integrierten Entwicklungsumgebung (IDE) für Python.

2. **Projekt klonen**: Clone das GitHub-Projekt in ein Verzeichnis deiner Wahl. Du kannst dies über die GitHub-Website tun oder die folgende Befehlszeile verwenden:
```
git clone <GitHub-Repository-URL>
```

3. **PyCharm öffnen**: Öffne PyCharm und wähle "Open" aus dem Hauptmenü. Navigiere zu dem Verzeichnis, in dem du das Projekt geklont hast, und wähle es aus.

4. **Virtuelle Umgebung erstellen**: In PyCharm wird empfohlen, eine virtuelle Python-Umgebung zu erstellen. Gehe dazu zu "File" > "Settings" > "Python Interpreter" und klicke auf das Zahnradsymbol. Wähle "Add..." und erstelle eine neue virtuelle Umgebung.

5. **Flask installieren**: Öffne das Terminal in PyCharm und führe den folgenden Befehl aus, um Flask in deiner virtuellen Umgebung zu installieren:
```
pip install Flask
```

6. **App starten**: Du kannst die Flask-App starten, indem du die Datei `app.py` ausführst. Klicke mit der rechten Maustaste auf die Datei in PyCharm und wähle "Run 'app'". Alternativ kannst du auch das Terminal verwenden und den folgenden Befehl ausführen:
```
python app.py
```

### Technische Beschreibung

Für Entwickler und technisch Interessierte bieten wir eine kurze Übersicht über die technische Seite des Projekts:

- **Frontend**: Das Frontend ist mit HTML, CSS und JavaScript entwickelt. Die Benutzeroberfläche verwendet Grid Layouts und Flexbox für ein ansprechendes Design. Das Desin habe ich mit chatGPT gemacht, weil kein bock auf frontend machen, ohne bezahlt zu werden.

- **Backend**: Das Backend verwendet Flask, ein Python-Framework, um die Spiellogik zu verwalten. Die Kommunikation zwischen Frontend und Backend erfolgt über AJAX-Anfragen.

- **Spiellogik**: Das Spiel verwendet Reguläre Ausdrücke, um Benutzereingaben mit dem geheimen Wort zu vergleichen und Feedback zu generieren. Die verfügbaren Wörter werden dynamisch gefiltert.

- **In Entwicklung**: Das Projekt ist noch nicht abgeschlossen und wird kontinuierlich verbessert. Neue Funktionen und Fehlerkorrekturen sind geplant.
