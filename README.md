# CogniPlay

CogniPlay is a cognitive training app featuring three mini-games, built with Python and Pygame.

## Description

CogniPlay features three mini-games, each training a different cognitive function:

- **Memória Botânica** - a card pairing game that trains memory
- **Encontre o Pato** - an attention game where the user has to find and click on a duck hidden in a growing crowd of animals
- **Colheita Atenta** - a go/no-go task that trains inhibitory control: press SPACE when a good apple appears, and do nothing when a rotten one does

The interface is in European Portuguese.

## Features

- Sign up and log in, with passwords hashed using bcrypt
- Progress saved per user and per game in a SQLite database
- Difficulty that scales with the player's level
- Instructions screen for every game, available at any time
- Three mini-games

## Requirements

- Python 3
- pygame-ce
- bcrypt

## Installation

```bash
pip install pygame-ce bcrypt
```

## Running the program

```bash
python main.py
```

The database file `cogniplay.db` is created automatically on first run.

## Controls

- **Mouse** - navigate the menus and play Memória Botânica and Encontre o Pato
- **SPACE** - respond to good apples in Colheita Atenta
- **I** - open and close the instructions of the current game
- **F11** - toggle fullscreen (the app starts in fullscreen)

## Project structure

```
main.py               central game loop and screen navigation
configs.py            window, font and image settings
database.py           SQLite access, user registration and login
timer.py              elapsed time counter, with pause and resume
instructions.py       shared instructions screen and text wrapping
start_screen.py       welcome screen
signup_screen.py      registration screen
login_screen.py       login screen
selection_screen.py   game selection menu
memoria_botanica.py   memory mini-game
encontre_pato.py      attention mini-game
colheita_atenta.py    inhibitory control mini-game
imgs/                 images
fonts/                fonts
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Author

Inês Mendes
8470558@formacao.iefp.pt
26103 - Linguagens de Programação - Programação em Python
