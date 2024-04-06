Write-Host "Wenn Sie schon PIP haben, bitte einfach nur ein Input machen"
Write-Host "Bitte Python mit PIP und mit PATH installieren."
Write-Host "Danach eine Taste klicken um ein Input zu machen."

$userInput = Read-Host

pip install virtualenv

virtualenv DontWordle

cd .\DontWordle\Scripts\

.\activate.ps1

cd ..\..

pip install Flask

pip install Pyinstaller

pyinstaller --hidden-import Flask --add-data ".\words.txt;." --add-data ".\static\js\*;static\js" --add-data ".\static\css\*;static\css" --add-data ".\static\*;static" --add-data ".\templates\*;templates" --icon=.\static\favicon.ico --paths .\DontWordle\Lib\site-packages --console --debug all --onefile .\app.py

# Wechsle in das dist-Verzeichnis
cd .\dist\

# Kopiere die words.txt-Datei in das dist-Verzeichnis
Copy-Item ..\words.txt .

# Wechsle zurück in das Übergeordnete Verzeichnis
cd ..

# Erstelle eine neue Textdatei mit einer Nachricht im dist-Verzeichnis
New-Item -ItemType File -Path ".\" -Name "IN DEM DIST ORDNER IST DIE AUSFUEHRBARE DATEI.txt"
