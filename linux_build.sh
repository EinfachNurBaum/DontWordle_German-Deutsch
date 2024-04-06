# Überprüfe, ob "python" oder "python3" nicht vorhanden sind
if ! command -v python &>/dev/null && ! command -v python3 &>/dev/null; then
    # Wenn weder "python" noch "python3" gefunden werden, versuche Python 3.11 zu installieren
    sudo apt install python3.11
fi

pip install virtualenv

virtualenv DontWordle

source ./DontWordle/bin/activate

pip install flask

pip install pyinstaller

pyinstaller --hidden-import Flask --add-data "./words.txt:." --add-data "./static/js/*:static/js" --add-data "./static/css/*:static/css" --add-data "./static/*:static" --add-data "./templates/*:templates" --paths DontWordle/lib/python3.10/site-packages/ --onefile --console ./app.py

cd ./dist/

cp ../words.txt .

cd ..

touch "IN DEM DIST ORDNER IST DIE AUSFÜHRBARE DATEI".txt
