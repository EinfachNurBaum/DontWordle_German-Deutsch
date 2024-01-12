let cell_row = 5;

document.addEventListener('DOMContentLoaded', function() {
    const inputBox = document.getElementById('textbox');
    inputBox.addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            let inputText = inputBox.value;
            if (inputText.length === 5) {
                for (let i = 0; i < 5; i++) {
                    let cell = document.getElementById('cell-'+ cell_row +'-' + i);
                    if (cell) {
                        cell.textContent = inputText[i].toUpperCase();
                    }
                }
                inputBox.value = ''; // Textbox leeren

                // Hier senden wir die Eingabe an das Backend
                checkWord(inputText, cell_row);
                cell_row--;
            }
        }
    });
});

function checkWord(inputWord, row) {
    fetch('/check_word', {
        method: 'POST',
        body: JSON.stringify({
            word: inputWord,
            cell_row: row
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Aktualisieren der Anzahl der verbleibenden Wörter im Frontend
        let wordsLeftCount = document.getElementById('words-left-count');
        if (data.possible_words || data.possible_words === 0) {
            console.log('Mögliche Wörter Anzahl:', data.possible_words)
            console.log('Typ von data.possible_words:', typeof data.possible_words)
            if (typeof data.possible_words === 'number') {
                console.log('data.possible_words ist ein int!')
                wordsLeftCount.textContent = data.possible_words.toString();
            } else {
                console.error('Fehler: data.possible_words ist kein int!');
                wordsLeftCount.textContent = '0';
            }

            if (data.game_status === 'win' || data.game_status === 'lose') {
                // Setzen dem letzten Wort
                console.log('Game Status:', data.game_status);
                afterGameResult(data.final_word, data.game_status); // Ersetzen Sie TARGET_WORD durch die tatsächliche Variable, die das letzte Wort enthält
            }
        }
        else {
            console.error('data.possible_words existiert nicht!')
            wordsLeftCount.textContent = '0';
        }

        data.info.forEach(info => {
            let cell = document.getElementById('cell-'+row+'-' + info.position);
            if (cell) {
                cell.textContent = info.letter;
                if (info.status === 'correct') {
                    cell.style.backgroundColor = 'green';
                } else if (info.status === 'maybe') {
                    cell.style.backgroundColor = 'yellow';
                } else if (info.status === 'incorrect') {
                    cell.style.backgroundColor = '#ccc'; // Grauer Hintergrund für "incorrect"
                }
            }
        });

        console.log('Mögliche Wörter:', data.possible_words);
    })
    .catch(error => console.error('Fehler:', error));
}

function triggerConfetti() {
    confetti({
        particleCount: 150,
        spread: 180,
        origin: { y: 0.5, x: 0.75}
    });
    confetti({
        particleCount: 150,
        spread: 200,
        origin: { y: 0.5, x: 0.25}
    });
}


function afterGameResult(word, gameStatus) {
    document.getElementById('final-word').textContent = word;
    const shareButton = document.querySelector('.share-button');
    const finalWordContainer = document.querySelector('.final-word-container');

    // Container und Teilen-Button sichtbar machen
    finalWordContainer.style.display = 'block';
    shareButton.style.display = 'block';

    // Konfetti nur bei einem Gewinn auslösen
    if (gameStatus === 'win') {
        triggerConfetti();
    }
}

function shareResults() {
    // Logik zum Teilen der Ergebnisse
    // Beispiel: Kopieren des letzten Worts in die Zwischenablage oder Teilen über soziale Medien
}