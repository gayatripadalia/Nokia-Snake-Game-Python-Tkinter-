## 🐍 Nokia Snake Game

## Classic Snake Game using Python & Tkinter

## About the Project
This project is a Nokia-style Snake Game developed using Python and the Tkinter GUI library.
It recreates the classic snake gameplay with dynamic speed control, score tracking,
and a visual speed indicator panel.

## Features
- Classic snake gameplay
- Grid-based movement
- Random food generation
- Score tracking
- Dynamic speed control
- Speed indicator (Slow / Medium / Fast)
- Status panel showing score and speed
- Wall and self collision detection
- Game Over screen with Retry button

## Speed Indicator Logic
- 🟢 Slow : speed > 150 ms
- 🟡 Medium : 90 < speed ≤ 150 ms
- 🔴 Fast : speed ≤ 90 ms

Speed increases immediately after eating food and gradually relaxes using a cooldown system.

## Controls
- Arrow Keys to move the snake

## Technologies Used
- Python 3
- Tkinter
- Random module

## How to Run
python snake_game.py

## Author
Gayatri Padalia  
BCA (Hons.) AI & Data Science  
Graphic Era Hill University
