import os
import webbrowser

def interactive_hangman():
    # 'r' prefix use kiya hai taake strings as-is render hon aur JS break na ho
    html_content = r"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Interactive Hangman</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body { font-family: 'Inter', sans-serif; background-color: #121212; color: #e5e7eb; }
            .floating-card { transition: all 0.3s ease; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
            
            /* Dynamic Letter Boxes */
            .letter-box { 
                width: 40px; height: 50px; 
                border-bottom: 2px solid #2dd4bf; /* Teal accent */
                display: flex; align-items: flex-end; justify-content: center; 
                font-size: 1.5rem; font-weight: bold; text-transform: uppercase; color: white; 
                transition: all 0.2s ease;
            }
            .letter-empty { border-bottom-color: #374151; color: transparent; }
            
            input:focus { outline: none; border-color: #2dd4bf; box-shadow: 0 0 10px rgba(45, 212, 191, 0.2); }
        </style>
    </head>
    <body class="min-h-screen flex flex-col items-center justify-center p-4">
        
        <div class="floating-card bg-[#1E1E1E] rounded-2xl p-8 border border-gray-800 w-full max-w-lg text-center relative">
            <h2 class="text-3xl font-extrabold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-indigo-500">Interactive Hangman</h2>
            <p class="text-sm text-gray-400 mb-6" id="status-text">Type a letter below to guess!</p>
            
            <div class="flex flex-col items-center justify-center bg-[#121212] rounded-xl p-6 mb-6">
                <pre id="hangman-art" class="text-indigo-400 font-mono text-sm leading-tight mb-8 text-left inline-block">
- - - - - - -
|           |
|            
|            
|            
-
                </pre>
                
                <div id="word-container" class="flex flex-wrap justify-center gap-2 px-2">
                </div>
            </div>
            
            <div class="mb-8 flex justify-center items-center flex-col">
                <input type="text" id="letter-input" maxlength="1" autocomplete="off" 
                       class="w-16 h-16 text-center text-2xl font-bold bg-[#121212] border-2 border-gray-700 text-teal-400 rounded-xl transition"
                       placeholder="?">
                <p class="text-xs text-gray-500 mt-2">Click box and type</p>
            </div>

            <div>
                <button onclick="window.close()" class="bg-teal-500 text-gray-900 px-10 py-2.5 rounded-full font-bold hover:bg-teal-400 transition transform hover:scale-105 shadow-lg">Done</button>
            </div>
        </div>

        <script>
            // Random words including some tech/agency themes
            const wordList = ["PYTHON", "ECHO", "PHANTOM", "DEVELOPER", "MINIMAL", "AGENCY", "DESIGN"];
            let currentWord = wordList[Math.floor(Math.random() * wordList.length)];
            let guessedLetters = new Set();
            let mistakes = 0;
            const maxMistakes = 6;

            // Perfectly aligned ASCII Art matching the first image.
            const stages = [
                `- - - - - - -\n|           |\n|            \n|            \n|            \n-`,
                `- - - - - - -\n|           |\n|           O\n|            \n|            \n-`,
                `- - - - - - -\n|           |\n|           O\n|           |\n|            \n-`,
                `- - - - - - -\n|           |\n|           O\n|          /|\n|            \n-`,
                `- - - - - - -\n|           |\n|           O\n|          /|\\\n|            \n-`,
                `- - - - - - -\n|           |\n|           O\n|          /|\\\n|          / \n-`,
                `- - - - - - -\n|           |\n|           O\n|          /|\\\n|          / \\\n-`
            ];

            const wordContainer = document.getElementById('word-container');
            const hangmanArt = document.getElementById('hangman-art');
            const inputField = document.getElementById('letter-input');
            const statusText = document.getElementById('status-text');

            // Words ki blanks render karne ka function
            function renderWord() {
                wordContainer.innerHTML = '';
                let win = true;
                
                for (let char of currentWord) {
                    const div = document.createElement('div');
                    if (guessedLetters.has(char)) {
                        div.className = 'letter-box';
                        div.innerText = char;
                    } else {
                        div.className = 'letter-box letter-empty';
                        div.innerText = char;
                        win = false; // Agar koi letter missing hai toh win false
                    }
                    wordContainer.appendChild(div);
                }
                
                // Win state check
                if (win) {
                    statusText.innerText = "You Won! 🎉 Excellent Job.";
                    statusText.className = "text-md text-teal-400 font-bold mb-6 animate-pulse";
                    inputField.disabled = true;
                    inputField.classList.add('opacity-50', 'cursor-not-allowed');
                }
            }

            // Input handle karne ka function
            function handleGuess(e) {
                let letter = e.target.value.toUpperCase();
                e.target.value = ''; // Input box foran clear kar do
                
                // Sirf A-Z letters allow karein
                if (!letter.match(/[A-Z]/) || letter.length !== 1) return;

                if (guessedLetters.has(letter)) {
                    statusText.innerText = "Already guessed '" + letter + "'!";
                    statusText.className = "text-sm text-yellow-400 mb-6";
                    return;
                }

                guessedLetters.add(letter);

                // Agar guess galat hai
                if (!currentWord.includes(letter)) {
                    mistakes++;
                    hangmanArt.innerText = stages[mistakes];
                    
                    if (mistakes >= maxMistakes) {
                        statusText.innerText = "Game Over! The word was " + currentWord;
                        statusText.className = "text-md text-red-400 font-bold mb-6";
                        inputField.disabled = true;
                        inputField.classList.add('opacity-50', 'cursor-not-allowed');
                    } else {
                        statusText.innerText = "Wrong guess! Try again.";
                        statusText.className = "text-sm text-red-400 mb-6";
                    }
                } else {
                    // Agar guess sahi hai
                    statusText.innerText = "Good guess!";
                    statusText.className = "text-sm text-teal-400 mb-6";
                }
                
                renderWord();
            }

            // Event Listener for the input field
            inputField.addEventListener('input', handleGuess);
            
            // Initialize game
            hangmanArt.innerText = stages[0];
            renderWord();
            inputField.focus();
        </script>
    </body>
    </html>
    """
    
    file_path = os.path.abspath("task1_interactive_hangman.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print("Interactive Hangman task running... Opening Web UI.")
    webbrowser.open(f"file://{file_path}")

if __name__ == "__main__":
    interactive_hangman()