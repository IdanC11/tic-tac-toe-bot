# Tic-Tac-Toe Game
This repository contains a Python implementation of the classic game Tic-Tac-Toe. 
The game can be played either against another player or against a computer opponent. 
The code provides a command-line interface (CLI) for interacting with the game.

## Features
* Play against another player: Two human players can take turns playing the game on the command line.
* Play against a computer opponent: A computer bot can be chosen as the opponent to play against.
* Game statistics tracking: The code records game results, including player names, dates, and winners, in an SQLite database.
* Database interaction: The code establishes a connection to an SQLite database file and creates a table to store game records.
  
## Dependencies
The following dependencies are required to run the Tic-Tac-Toe game:

* Python 3.x
* numpy
* tabulate
* sqlite3
  
## Usage
### Clone the repository in shell:

git clone https://github.com/your-username/tic-tac-toe.git

cd tic-tac-toe

### Install the dependencies using pip in shell:

pip install numpy tabulate sqlite3

### Run the game in shell:

python tic_tac_toe.py

Follow the on-screen instructions to play the game. Use the menu options to select the game mode (player vs. player, player vs. computer, view statistics, clear statistics).

## Database
### The game results are stored in an SQLite database file named ttt_db.db. The database contains a single table named GameTable, which has the following columns:

* player1: Name of the first player.
* player2: Name of the second player or computer opponent.
* date: Date of the game.
* score: The winner of the game or "Tie" in case of a draw.
