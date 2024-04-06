# Überprüfe, ob "python" oder "python3" nicht vorhanden sind
if ! command -v python &>/dev/null && ! command -v python3 &>/dev/null; then
    # Wenn weder "python" noch "python3" gefunden werden, versuche Python 3.11 zu installieren
    sudo apt install python3.11
fi

pip install virtualenv

virtualenv DontWordle

echo "Bitte aktivieren Sie die Virtual Enviroment, die per Skripte von ./DontWodle/bin aktiviert werden kann."
echo "Dann bitte nach der aktivierung Flask installieren mit 'pip install flask'"
echo "Wenn es geklappt hat, bitte ein Input machen, egal welcher."

read userInput

pip install pyinstaller

pyinstaller --hidden-import Flask --add-data "./words.txt:." --add-data "./static/js/*:static/js" --add-data "./static/css/*:static/css" --add-data "./static/*:static" --add-data "./templates/*:templates" --paths DontWordle/lib/python3.10/site-packages/ --onefile --console ./app.py

cd ./dist/

cp ../words.txt .

cd ..

touch "IN DEM DIST ORDNER IST DIE AUSFÜHRBARE DATEI".txt
