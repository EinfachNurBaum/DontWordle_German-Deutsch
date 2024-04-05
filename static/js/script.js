let cell_row = 5;
let feedbackArray = []; // Zweidimensionales Array für das Feedback
let UserHaveWon = null;
let wordList = [];

document.addEventListener('DOMContentLoaded', function() {
    loadWordList();
    const inputBox = document.getElementById('textbox');

    inputBox.addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            let inputText = inputBox.value;
            if (wordList.includes(inputText.toUpperCase()))
            {
                if (inputText.length === 5) {
                    for (let i = 0; i < 5; i++) {
                        let cell = document.getElementById('cell-'+ cell_row +'-' + i);
                        if (cell) {
                            cell.textContent = inputText[i].toUpperCase();
                        }
                        else {
                            console.error('Zelle nicht gefunden:', 'cell-'+ cell_row +'-' + i);
                        }
                    }
                    inputBox.value = ''; // Textbox leeren

                    // Hier senden wir die Eingabe an das Backend
                    checkWord(inputText, cell_row);
                    cell_row--;
                }
            }
            else {
                inputBox.value = ''; // Textbox leeren

                // Animation für falsche Eingabe
                anime({
                    targets: inputBox,
                    translateX: [
                        { value: 10, duration: 100 },
                        { value: -10, duration: 100 },
                        { value: 0, duration: 100 }
                    ],
                });

            }
        }
    });
});

// Funktion zum Laden der Wörterliste aus der Datenbankdatei
function loadWordList() {
    fetch('/get_word_list') // Dies ist der Endpunkt, den Sie in Flask erstellen müssen, um die Wörterliste zu erhalten
        .then(response => response.json())
        .then(data => {
            // Daten aufteilen und der wordList zuweisen
            wordList = data.word_list;
            console.log(wordList);
        })
        .catch(error => console.error('Fehler beim Laden der Wortliste:', error));
}

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

            wordsLeftCount.textContent = data.possible_words.toString();

            if (data.game_status === 'win' || data.game_status === 'lose') {
                // Setzen dem letzten Wort
                console.log('Game Status:', data.game_status);
                afterGameResult(data.final_word, data.game_status); // Anzeigen des letzten Wortes und Auslösen von Konfetti
            }

            feedbackArray.push(data);
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
                    cell.style.backgroundColor = '#35393B'; // Grauer Hintergrund für "incorrect"
                }
            }
        });

        console.log('Mögliche Wörter:', data.possible_words);
    })
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
        UserHaveWon = 'win';
        triggerConfetti();
    }
    else {
        UserHaveWon = 'lose';
    }
}

// Wordle like Ergebnisse teilen
function shareResults() {
    let final_word = '';

    // Logik zum Teilen der Ergebnisse
    console.log(feedbackArray);


    let display = feedbackArray.map(row => row.info.map(feedback => {
        if (row.final_word !== null) {
            final_word = row.final_word;
        }
        if (feedback.status === 'correct') return '🟩';
        if (feedback.status === 'maybe') return '🟨';
        return '⬛';
    }).join('')).join('\n');

    if (UserHaveWon === 'win') {
        display += '\n\nDas letzte Wort: ' + final_word + ' wurde in ' + String(feedbackArray.length) + ' Versuchen erraten.';
    }
    else if (UserHaveWon === 'lose') {
        display += '\nIch bin scheiße!';
    }

    // In die Zwischenablage kopieren
    navigator.clipboard.writeText(display).then(() => {
        alert('Ergebnisse in die Zwischenablage kopiert!');
    }).catch(err => {
        console.error('Fehler beim Kopieren in die Zwischenablage:', err);
    });

}
