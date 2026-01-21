import tkinter as tk
import random
#CONSTANTS
CELL_SIZE = 25            
GAME_COLS = 22         
GAME_ROWS = 22           
GAME_WIDTH = GAME_COLS * CELL_SIZE
HEIGHT = GAME_ROWS * CELL_SIZE
PANEL_WIDTH = 240
WIDTH = GAME_WIDTH + PANEL_WIDTH
INITIAL_SPEED = 200
MIN_SPEED = 60
SCORE_INCREMENT = 5
SPEED_COOLDOWN = 2000  # ms
#COLORS 
BG_COLOR = "#000814"
GRID_COLOR = "#003566"
PANEL_COLOR = "#001d3d"
SNAKE_COLOR = "#00ff99"
SNAKE_HEAD = "#80ffdb"
FOOD_COLOR = "#ff006e"
TEXT_GLOW = "#00f5d4"
DIM_TEXT = "#6c757d"
#FONTS
TITLE_FONT = ("Segoe UI", 18, "bold")
LABEL_FONT = ("Segoe UI", 12, "bold")
GAME_OVER_FONT = ("Segoe UI", 32, "bold")
#WINDOW 
root = tk.Tk()
root.title("GP Snake Game")
root.configure(bg=BG_COLOR)
root.geometry(f"{WIDTH}x{HEIGHT}")
root.minsize(WIDTH, HEIGHT)
root.resizable(True, True)
#BACKGROUND
bg_canvas = tk.Canvas(root, bg="#020617", highlightthickness=0)
bg_canvas.place(relwidth=1, relheight=1)
#GAME CANVAS
canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg=BG_COLOR,
    highlightthickness=0
)
canvas.place(relx=0.5, rely=0.5, anchor="center")
#GAME STATE
snake = []
direction = "Right"
food = None
score = 0
speed = INITIAL_SPEED
game_over = False
retry_button = None
#WALLPAPER
def draw_wallpaper():
    bg_canvas.delete("all")
    w = bg_canvas.winfo_width()
    h = bg_canvas.winfo_height()
    bg_canvas.create_rectangle(0, 0, w, h, fill="#020617", outline="")
    for i in range(-h, w, 90):
        bg_canvas.create_line(i, 0, i + h, h, fill="#06283d", width=2)
    for _ in range(160):
        x = random.randint(0, w)
        y = random.randint(0, h)
        bg_canvas.create_oval(x, y, x+2, y+2, fill="#00f5d4", outline="")
def on_resize(event):
    draw_wallpaper()
    canvas.place(relx=0.5, rely=0.5, anchor="center")
root.bind("<Configure>", on_resize)
#DRAW HELPERS
def draw_block(x, y, color, tag):
    px = x * CELL_SIZE
    py = y * CELL_SIZE
    canvas.create_rectangle(
        px + 2, py + 2,
        px + CELL_SIZE - 2, py + CELL_SIZE - 2,
        fill=color, outline="", tag=tag
    )
def draw_grid():
    for x in range(0, GAME_WIDTH, CELL_SIZE):
        canvas.create_line(x, 0, x, HEIGHT, fill=GRID_COLOR, tag="grid")
    for y in range(0, HEIGHT, CELL_SIZE):
        canvas.create_line(0, y, GAME_WIDTH, y, fill=GRID_COLOR, tag="grid")
def draw_panel():
    canvas.delete("panel")
    canvas.create_rectangle(GAME_WIDTH, 0, WIDTH, HEIGHT,
                            fill=PANEL_COLOR, tag="panel")
    canvas.create_text(GAME_WIDTH + PANEL_WIDTH//2, 40,
                       text="STATUS", fill=TEXT_GLOW,
                       font=TITLE_FONT, tag="panel")
    canvas.create_text(GAME_WIDTH + PANEL_WIDTH//2, 90,
                       text="SCORE", fill=DIM_TEXT,
                       font=LABEL_FONT, tag="panel")
    canvas.create_text(GAME_WIDTH + PANEL_WIDTH//2, 125,
                       text=str(score), fill="white",
                       font=("Segoe UI", 28, "bold"), tag="panel")
def draw_speed_dots():
    canvas.delete("speeddots")
    active = 0 if speed > 150 else 1 if speed > 90 else 2
    colors = ["#00ff99", "#ffd60a", "#ff006e"]
    labels = ["SLOW", "MEDIUM", "FAST"]
    for i in range(3):
        y = 190 + i * 50
        canvas.create_oval(
            GAME_WIDTH + PANEL_WIDTH//2 - 12, y - 12,
            GAME_WIDTH + PANEL_WIDTH//2 + 12, y + 12,
            fill=colors[i] if i == active else "#1b263b",
            outline="", tag="speeddots"
        )
    canvas.create_text(GAME_WIDTH + PANEL_WIDTH//2, 360,
                       text=labels[active],
                       fill=colors[active],
                       font=("Segoe UI", 14, "bold"),
                       tag="speeddots")
#GAME LOGIC
def create_food():
    global food
    while True:
        fx = random.randint(0, GAME_COLS - 1)
        fy = random.randint(0, GAME_ROWS - 1)
        if [fx, fy] not in snake:
            food = [fx, fy]
            break
def reset_game():
    global snake, direction, score, speed, game_over, retry_button
    canvas.delete("all")
    draw_grid()
    draw_panel()
    snake = [[GAME_COLS//2, GAME_ROWS//2]]
    direction = "Right"
    score = 0
    speed = INITIAL_SPEED
    game_over = False
    create_food()
    draw_game()
    move_snake()
    if retry_button:
        retry_button.destroy()
        retry_button = None
def move_snake():
    global score, speed, game_over, retry_button
    if game_over:
        return
    head_x, head_y = snake[0]
    if direction == "Left": head_x -= 1
    elif direction == "Right": head_x += 1
    elif direction == "Up": head_y -= 1
    elif direction == "Down": head_y += 1
    new_head = [head_x, head_y]
    if (head_x < 0 or head_y < 0 or
        head_x >= GAME_COLS or
        head_y >= GAME_ROWS or
        new_head in snake):
        game_over = True
        canvas.create_text(GAME_WIDTH//2, HEIGHT//2 - 40,
                           text="GAME OVER",
                           fill="#ff006e",
                           font=GAME_OVER_FONT)
        retry_button = tk.Button(
            root, text="RETRY",
            font=("Segoe UI", 14, "bold"),
            bg="#ff006e", fg="white",
            relief="flat",
            command=reset_game
        )
        canvas.create_window(GAME_WIDTH//2, HEIGHT//2 + 30,
                             window=retry_button)
        return
    snake.insert(0, new_head)
    if new_head == food:
        score += SCORE_INCREMENT
        create_food()
        if speed > MIN_SPEED:
            speed -= 15
    else:
        snake.pop()
    draw_game()
    root.after(speed, move_snake)
def speed_cooldown():
    global speed
    if not game_over and speed < INITIAL_SPEED:
        speed += 5
    root.after(SPEED_COOLDOWN, speed_cooldown)
def draw_game():
    canvas.delete("snake")
    canvas.delete("food")
    for i, (x, y) in enumerate(snake):
        draw_block(x, y,
                   SNAKE_HEAD if i == 0 else SNAKE_COLOR,
                   "snake")
    if food:
        draw_block(food[0], food[1], FOOD_COLOR, "food")
    draw_panel()
    draw_speed_dots()
def change_direction(event):
    global direction
    opposite = {"Left":"Right", "Right":"Left",
                "Up":"Down", "Down":"Up"}
    if event.keysym in opposite and direction != opposite[event.keysym]:
        direction = event.keysym
#Start
root.bind("<Key>", change_direction)
draw_wallpaper()
reset_game()
speed_cooldown()
root.mainloop()