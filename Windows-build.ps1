pyinstaller --hidden-import Flask --add-data ".\words.txt;." --add-data ".\static\js\*;static\js" --add-data ".\static\css\*;static\css" --add-data ".\static\*;static" --add-data ".\templates\*;templates" --icon=DontWordle_German-Deutsch\static\favicon.ico --paths ..\venv\Lib\site-packages --onefile --console .\app.py

# Wechsle in das dist-Verzeichnis
cd .\dist\

# Kopiere die words.txt-Datei in das dist-Verzeichnis
Copy-Item ..\words.txt .

# Wechsle zurück in das übergeordnete Verzeichnis
cd ..

# Erstelle eine neue Textdatei mit einer Nachricht im dist-Verzeichnis
New-Item -ItemType File -Path ".\" -Name "IN DEM DIST ORDNER IST DIE AUSFÜHRBARE DATEI.txt"
