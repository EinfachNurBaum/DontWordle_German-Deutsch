# DON'T WORDLE GERMAN - DEUTSCH(Erste Version 🔴)

## Projektbeschreibung

DON'T WORDLE ist eine Variante des beliebten Worträtselspiels Wordle, bei dem Sie versuchen müssen, das geheime Wort zu erraten. Wir haben über 6000 Wörter die Sie erraten können.

Dieses Projekt befindet sich derzeit in der Entwicklung und wird unregelmäßig weiterentwickelt.

Für Linux und Windows gibt es direkt ausführbare Dateien unter: [Releases](https://github.com/EinfachNurBaum/DontWordle_German-Deutsch/releases)

## Anleitung (Aktuell)

### Anleitung zum Starten der Flask-App unter Linux

Um die Flask-App unter Linux zu starten, folgen Sie bitte den unten stehenden Schritten wenn die **linux_build.sh** nicht korrekt ausgeführt wird:

1. **Installieren Sie Virtualenv:**
   Führen Sie den folgenden Befehl aus, um Virtualenv zu installieren:
   ```bash
   pip install virtualenv
   ```

2. **Erstellen Sie eine Virtual Environment:**
   Erstellen Sie eine neue Virtual Environment mit dem Namen "DontWordle", in den Verzeichnis wo auch die `app.py` befindet mit dem Befehl:
   ```bash
   virtualenv DontWordle
   ```

3. **Aktivieren Sie die Virtual Environment:**
   Aktivieren Sie die Virtual Environment mit den Skripten in `./DontWordle/bin`. Unter Gnome können Sie dies mit folgendem Befehl tun:
   ```bash
   source ./DontWordle/bin/activate
   ```

4. **Installieren Sie Flask:**
   Nach der Aktivierung der Virtual Environment installieren Sie Flask mit dem Befehl:
   ```bash
   pip install flask
   ```

5. **Starten Sie die Flask-App:**
   Führen Sie die Flask-App mit dem folgenden Befehl aus:
   ```bash
   python app.py
   ```

   Die App sollte jetzt auf `http://localhost:5000` oder `http://localhost:5001` verfügbar sein.

7. **(Ab jetzt Optional) Für eine Binary**
    Installieren Sie Pyinstaller mit dem folgenem Befehl:
    ```bash
    pip install pyinstaller
    ```

8. **(Ab jetzt Optional) Builden der Binary**
    Führen Sie folgenen Befehl aus, in dem Verzeichnis wo die `app.py` und DontWordle ist:
    ```bash
    pyinstaller --hidden-import Flask --add-data "./words.txt:." --add-data "./static/js/*:static/js" --add-data "./static/css/*:static/css" --add-data "./static/*:static" --add-data "./templates/*:templates" --paths DontWordle/lib/python3.11/site-packages/ --onefile --console ./app.py
    ```

9. **(Ab jetzt Optional) Starten der Binary**
    Öffnen sie ein Terminal in den lokalen `dist` Verzeichnis und führen sie folgenen Befehl aus:
    ```bash
    ./app
    ```


### Anleitung zum Starten der Flask-App unter Windows, wenn die Exe Datei nicht funktioniert!

Um die Flask-App unter Windows zu starten, befolgen Sie bitte die unten stehenden Schritte:

1. **Installieren Sie Python und PIP:**
   Stellen Sie sicher, dass Python und PIP auf Ihrem System installiert sind. Sie können Python von der offiziellen Website herunterladen und installieren: [python.org](https://www.python.org/downloads/)

2. **Klonen Sie das Repository und wechseln Sie in das Verzeichnis:**
   Öffnen Sie ein Terminal (Powersshell) und lade sie Sie das Repository herunter unter "Code" -> "Download ZIP"
   oder Klonen Sie das Repository mit:
   ```bash
   git clone https://github.com/EinfachNurBaum/DontWordle_German-Deutsch.git
   cd DontWordle_German-Deutsch
   ```

3. **Führen Sie das Windows-Build-Skript aus:**
   In den Ordner, mit der `app.py`, führen Sie das Windows-Build-Skript aus, indem Sie die Datei `Windows-build.ps1` ausführen. Sie können dies mit PowerShell tun:
   ```bash
   .\Windows-build.ps1
   ```

4. **Starten Sie die Flask-App:**
   Nachdem das Skript ausgeführt wurde, navigieren Sie in das `dist`-Verzeichnis:
   ```bash
   cd dist
   ```

5. **(Wenn die EXE nicht funktioniert) Führen Sie die `app.py`**
    In dem Verzeichnis mit der `app.py` führen Sie folgenes aus:
    ```bash
    python app.py
    ```
    oder 
    ```bash
    python3 app.py
    ```
    Die App sollte nun auf `http://localhost:5000` oder `http://localhost:5001` verfügbar sein.

#### Fehlerbehebung:
Von wenn Fehler:
   ```bash
   Windows-build.ps1" kann nicht
   geladen werden, da die Ausführung von Skripts auf diesem System deaktiviert ist. Weitere Informationen finden Sie
   unter "about_Execution_Policies" (https:/go.microsoft.com/fwlink/?LinkID=135170).
   ```

Das kann man lösen durch:
   ```bash
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
   ```
Weiter mit:
   ```bash
   .\Windows-build.ps1
   ```

### Anleitung zum Starten der Flask-App für Python-Kenner

Wenn Sie mit Python vertraut sind, können Sie die Flask-App manuell einrichten und starten:

1. **Klonen Sie das Repository und wechseln Sie in das Verzeichnis:**
   ```bash
   git clone https://github.com/EinfachNurBaum/DontWordle_German-Deutsch.git
   cd DontWordle_German-Deutsch
   ```

2. **Erstellen und aktivieren Sie eine Virtual Environment:**
   Erstellen Sie eine Virtual Environment und aktivieren Sie sie:
   ```bash
   python -m venv venv
   source .\venv\Scripts\activate 
   ```

3. **Installieren Sie die erforderlichen Pakete:**
   Installieren Sie Flask und andere erforderliche Pakete:
   ```bash
   pip install -r requirements.txt
   ```

4. **Starten Sie die Flask-App:**
   Führen Sie die Flask-App aus:
   ```bash
   python app.py
   ```

   Die App sollte nun auf `http://localhost:5000` oder `http://localhost:5001` verfügbar sein.



### Technische Beschreibung

Für Entwickler und technisch Interessierte bieten wir eine kurze Übersicht über die technische Seite des Projekts:

- **Frontend**: Das Frontend ist mit HTML, CSS und JavaScript entwickelt. Die Benutzeroberfläche verwendet Grid Layouts und Flexbox für ein ansprechendes Design. Das Design habe ich zu großteils mit ChatGPT gemacht, weil ich keinen Bock habe das Frontend selber zumacheb.
  - Das Frontend bietet das Feature von Darkmode und Lightmode an.
  - Für die Animation wird Anime.js genutzt

- **Backend**: Das Backend verwendet Flask, ein Python-Framework, um die Kommunikation von Frontend und Backend zu verwalten. Die Kommunikation zwischen Frontend und Backend erfolgt über nur über POST-Anfragen, zudem verwaltet es auch denn Rate-Prozess, also welches Wort Sie raten müssen, was Sie richtig haben und co.

- **Datenbank**: Die Datenbank ist aktuell in der TXT Version, weil eine TXT sich am leichtesten lesen und öffnen lässt.
  
- **Spiellogik**: Der User muss das System zu einem Wort zwingen. Je nach Eingabe und anfangs Zielwort ergiben sich "gefangene Buchstaben". Die jeweils im nächsten Zielwort vorhanden sein müssen.
