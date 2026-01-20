🐍 Nokia Snake Game (Python – Tkinter)

A classic Nokia-style Snake Game built using Python and Tkinter. The game features smooth movement, dynamic speed control, score tracking, and a visual status panel that indicates the current speed level (Slow, Medium, Fast).

Features

Classic snake gameplay

Grid-based game board

Random food generation

Score increases on eating food

Dynamic speed system with cooldown

Speed indicator using green, yellow, and red dots

Collision detection (wall & self)

Game Over screen with Retry button

Side status panel showing score and speed

Speed Indicator Logic

🟢 Slow → speed > 150 ms

🟡 Medium → 90 < speed ≤ 150 ms

🔴 Fast → speed ≤ 90 ms
Eating food increases speed instantly, while a cooldown system gradually slows the snake back to normal.

Controls

Arrow Keys: Move the snake (Up, Down, Left, Right)

Technologies Used

Python 3

Tkinter

Random module

How to Run
python snake_game.py

Project Structure
nokia-snake-game/
├── snake_game.py
└── README.md

Author

Gayatri Padalia
BCA (Hons.) AI & Data Science
Graphic Era Hill University
