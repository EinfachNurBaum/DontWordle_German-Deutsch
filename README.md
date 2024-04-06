# DON'T WORDLE (Erste Version 🔴)

## Projektbeschreibung

DON'T WORDLE ist eine Variante des beliebten Worträtselspiels Wordle, bei dem du versuchen musst, das geheime Wort zu erraten. Dieses Projekt befindet sich derzeit in der Entwicklung und wird unregelmäßig weiterentwickelt.

## Anleitung (Aktuell)



### Technische Beschreibung

Für Entwickler und technisch Interessierte bieten wir eine kurze Übersicht über die technische Seite des Projekts:

- **Frontend**: Das Frontend ist mit HTML, CSS und JavaScript entwickelt. Die Benutzeroberfläche verwendet Grid Layouts und Flexbox für ein ansprechendes Design. Das Design habe ich zu großteils mit chatGPT gemacht, weil ich kein bock habe frontend machen, ohne bezahlt zu werden.
  - Das Frontend bietet das Feature von Darkmode und Lightmode an.
  - Für die Animation wird Anime.js genutzt

- **Backend**: Das Backend verwendet Flask, ein Python-Framework, um die Kommunikation von Frontend und Backend zu verwalten. Die Kommunikation zwischen Frontend und Backend erfolgt über nur über POST-Anfragen.

- **Datenbank**: Die Datenbank ist aktuell in der TXT Version, weil eine TXT sich am leichtesten lesen und öffnen lässt.
  
- **Spiellogik**: Der User muss das System zu einem Wort zwingen. Je nach Eingabe und anfangs Zielwort ergiben sich "gefangene Buchstaben". Die jeweils im nächsten Zielwort vorhanden sein müssen.
