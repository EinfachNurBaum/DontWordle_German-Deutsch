# DON'T WORDLE (Erste Version 🔴)

## Projektbeschreibung

DON'T WORDLE ist eine Variante des beliebten Worträtselspiels Wordle, bei dem du versuchen musst, das geheime Wort zu erraten. Dieses Projekt befindet sich derzeit in der Entwicklung und wird unregelmäßig weiterentwickelt.

## Anleitung (Aktuell)

### Anleitung zum Starten der Flask-App unter Linux

Um die Flask-App unter Linux zu starten, folgen Sie bitte den unten stehenden Schritten, wenn die **linux_build.sh** nicht korrekt ausgeführt werden könnte:

1. **Überprüfen Sie die Python-Installation:**
   Öffnen Sie ein Terminal und überprüfen Sie, ob Python installiert ist, indem Sie `python --version` oder `python3 --version` eingeben.
   ```
   sudo apt install python3.11
   ```
2. **Installieren Sie Virtualenv:**
   Führen Sie den folgenden Befehl aus, um Virtualenv zu installieren:
   ```
   pip install virtualenv
   ```
3. **Erstellen Sie eine Virtual Environment:**
   Erstellen Sie eine neue Virtual Environment mit dem Namen "DontWordle", in den Verzeichnis wo auch die **app.py** befindet mit dem Befehl:
   ```
   virtualenv DontWordle
   ```

4. **Aktivieren Sie die Virtual Environment:**
   Aktivieren Sie die Virtual Environment mit den Skripten in `./DontWordle/bin`. Unter Gnome können Sie dies mit folgendem Befehl tun:
   ```
   source ./DontWordle/bin/activate
   ```

5. **Installieren Sie Flask:**
   Nach der Aktivierung der Virtual Environment installieren Sie Flask mit dem Befehl:
   ```
   pip install flask
   ```

6. **Starten Sie die Flask-App:**
   Führen Sie die Flask-App mit dem folgenden Befehl aus:
   ```
   python app.py
   ```

   Die App sollte jetzt auf `http://localhost:5000` oder `http://localhost:5001` verfügbar sein.

7. **(Ab jetzt Optional) Für eine Binary**
    Installieren Sie Pyinstaller mit dem folgenem Befehl:
    ```
    pip install pyinstaller
    ```
8. **(Ab jetzt Optional) Builden der Binary**
    Führen Sie folgenen Befehl aus, in dem Verzeichnis wo die app.py und DontWordle ist:
    ```
    pyinstaller --hidden-import Flask --add-data "./words.txt:." --add-data "./static/js/*:static/js" --add-data "./static/css/*:static/css" --add-data "./static/*:static" --add-data "./templates/*:templates" --paths DontWordle/lib/python3.11/site-packages/ --onefile --console ./app.py
    ```
9. **(Ab jetzt Optional) Starten der Binary**
    Öffnen sie ein Terminal in den lokalen "dist" Verzeichnis und führen sie folgenen Befehl aus:
    ```
    ./app
    ```


### Anleitung zum Starten der Flask-App unter Windows

Um die Flask-App unter Windows zu starten, befolgen Sie bitte die unten stehenden Schritte:

1. **Installieren Sie Python und PIP:**
   Stellen Sie sicher, dass Python und PIP auf Ihrem System installiert sind. Sie können Python von der offiziellen Website herunterladen und installieren: [python.org](https://www.python.org/downloads/)

2. **Klonen Sie das Repository und wechseln Sie in das Verzeichnis:**
   Öffnen Sie ein terminal (Powersshell) und lade sie Sie das Repository herunter unter "Code" -> "Download ZIP"
   oder Klonen Sie das Repository mit:
   ```
   git clone https://github.com/EinfachNurBaum/DontWordle_German-Deutsch.git
   cd DontWordle_German-Deutsch
   ```

3. **Führen Sie das Windows-Build-Skript aus:**
   In den Ordner, mit der app.py, führen Sie das Windows-Build-Skript aus, indem Sie die Datei `Windows-build.ps1` ausführen. Sie können dies mit PowerShell tun:
   ```
   .\Windows-build.ps1
   ```

4. **Starten Sie die Flask-App:**
   Nachdem das Skript ausgeführt wurde, navigieren Sie in das `dist`-Verzeichnis:
   ```
   cd dist
   ```

   Führen Sie die ausführbare Datei aus, um die Flask-App zu starten. Die App sollte nun auf `http://localhost:5000` oder `http://localhost:5001` verfügbar sein.

5. **(Wenn die EXE nicht funktioniert) Führen Sie die app.py**
    In dem Verzeichnis mit der app.py führen Sie folgenes aus:
    ```
    python app.py
    ```
    oder 
    ```
    python3 app.py
    ```
    Die App sollte nun auf `http://localhost:5000` oder `http://localhost:5001` verfügbar sein.

### Anleitung zum Starten der Flask-App für Python-Kenner

Wenn Sie mit Python vertraut sind, können Sie die Flask-App manuell einrichten und starten:

1. **Klonen Sie das Repository und wechseln Sie in das Verzeichnis:**
   ```
   git clone https://github.com/EinfachNurBaum/DontWordle_German-Deutsch.git
   cd DontWordle_German-Deutsch
   ```

2. **Erstellen und aktivieren Sie eine Virtual Environment:**
   Erstellen Sie eine Virtual Environment und aktivieren Sie sie:
   ```
   python -m venv venv
   source .\venv\Scripts\activate 
   ```

3. **Installieren Sie die erforderlichen Pakete:**
   Installieren Sie Flask und andere erforderliche Pakete:
   ```
   pip install -r requirements.txt
   ```

4. **Starten Sie die Flask-App:**
   Führen Sie die Flask-App aus:
   ```
   python app.py
   ```

   Die App sollte nun auf `http://localhost:5000` oder `http://localhost:5001` verfügbar sein.



### Technische Beschreibung

Für Entwickler und technisch Interessierte bieten wir eine kurze Übersicht über die technische Seite des Projekts:

- **Frontend**: Das Frontend ist mit HTML, CSS und JavaScript entwickelt. Die Benutzeroberfläche verwendet Grid Layouts und Flexbox für ein ansprechendes Design. Das Design habe ich zu großteils mit chatGPT gemacht, weil ich kein bock habe frontend machen, ohne bezahlt zu werden.
  - Das Frontend bietet das Feature von Darkmode und Lightmode an.
  - Für die Animation wird Anime.js genutzt

- **Backend**: Das Backend verwendet Flask, ein Python-Framework, um die Kommunikation von Frontend und Backend zu verwalten. Die Kommunikation zwischen Frontend und Backend erfolgt über nur über POST-Anfragen.

- **Datenbank**: Die Datenbank ist aktuell in der TXT Version, weil eine TXT sich am leichtesten lesen und öffnen lässt.
  
- **Spiellogik**: Der User muss das System zu einem Wort zwingen. Je nach Eingabe und anfangs Zielwort ergiben sich "gefangene Buchstaben". Die jeweils im nächsten Zielwort vorhanden sein müssen.
