import tkinter as tk
import random
# constants
cell_size = 25
game_cols = 22
game_rows = 22
game_width = game_cols * cell_size
height = game_rows * cell_size
panel_width = 240
width = game_width + panel_width
initial_speed = 200
min_speed = 60
score_increment = 5
speed_cooldown = 200  # ms
# colors
bg_color = "#000814"
grid_color = "#003566"
panel_color = "#001d3d"
snake_color = "#00ff99"
snake_head = "#80ffdb"
food_color = "#ff006e"
text_glow = "#00f5d4"
dim_text = "#6c757d"
# fonts
title_font = ("Segoe UI", 18, "bold")
label_font = ("Segoe UI", 12, "bold")
game_over_font = ("Segoe UI", 32, "bold")
# window
root = tk.Tk()
root.title("GP Snake Game")
root.configure(bg=bg_color)
root.geometry(f"{width}x{height}")
root.minsize(width, height)
root.resizable(True, True)
# background canvas
bg_canvas = tk.Canvas(root, bg="#020617", highlightthickness=0)
bg_canvas.place(relwidth=1, relheight=1)
# game canvas
canvas = tk.Canvas(
    root,
    width=width,
    height=height,
    bg=bg_color,
    highlightthickness=0
)
canvas.place(relx=0.5, rely=0.5, anchor="center")
# game state
snake = []
direction = "Right"
food = None
score = 0
speed = initial_speed
game_over = False
retry_button = None
# wallpaper
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
        bg_canvas.create_oval(x, y, x + 2, y + 2, fill="#00f5d4", outline="")
def on_resize(event):
    draw_wallpaper()
    canvas.place(relx=0.5, rely=0.5, anchor="center")
root.bind("<Configure>", on_resize)
# draw helpers
def draw_block(x, y, color, tag):
    px = x * cell_size
    py = y * cell_size
    canvas.create_rectangle(
        px + 2, py + 2,
        px + cell_size - 2, py + cell_size - 2,
        fill=color, outline="", tag=tag
    )
def draw_grid():
    for x in range(0, game_width, cell_size):
        canvas.create_line(x, 0, x, height, fill=grid_color, tag="grid")
    for y in range(0, height, cell_size):
        canvas.create_line(0, y, game_width, y, fill=grid_color, tag="grid")
def draw_panel():
    canvas.delete("panel")
    canvas.create_rectangle(
        game_width, 0, width, height,
        fill=panel_color, tag="panel"
    )
    canvas.create_text(
        game_width + panel_width // 2, 40,
        text="STATUS", fill=text_glow,
        font=title_font, tag="panel"
    )
    canvas.create_text(
        game_width + panel_width // 2, 90,
        text="SCORE", fill=dim_text,
        font=label_font, tag="panel"
    )
    canvas.create_text(
        game_width + panel_width // 2, 125,
        text=str(score), fill="white",
        font=("Segoe UI", 28, "bold"), tag="panel"
    )
def draw_speed_dots():
    canvas.delete("speeddots")
    active = 0 if speed > 150 else 1 if speed > 90 else 2
    colors = ["#00ff99", "#ffd60a", "#ff006e"]
    labels = ["SLOW", "MEDIUM", "FAST"]
    for i in range(3):
        y = 190 + i * 50
        canvas.create_oval(
            game_width + panel_width // 2 - 12, y - 12,
            game_width + panel_width // 2 + 12, y + 12,
            fill=colors[i] if i == active else "#1b263b",
            outline="", tag="speeddots"
        )
    canvas.create_text(
        game_width + panel_width // 2, 360,
        text=labels[active],
        fill=colors[active],
        font=("Segoe UI", 14, "bold"),
        tag="speeddots"
    )
# game logic
def create_food():
    global food
    while True:
        fx = random.randint(0, game_cols - 1)
        fy = random.randint(0, game_rows - 1)
        if [fx, fy] not in snake:
            food = [fx, fy]
            break
def reset_game():
    global snake, direction, score, speed, game_over, retry_button
    canvas.delete("all")
    draw_grid()
    draw_panel()
    snake = [[game_cols // 2, game_rows // 2]]
    direction = "Right"
    score = 0
    speed = initial_speed
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
    if direction == "Left":
        head_x -= 1
    elif direction == "Right":
        head_x += 1
    elif direction == "Up":
        head_y -= 1
    elif direction == "Down":
        head_y += 1
    new_head = [head_x, head_y]
    if (
        head_x < 0 or head_y < 0 or
        head_x >= game_cols or
        head_y >= game_rows or
        new_head in snake
    ):
        game_over = True
        canvas.create_text(
            game_width // 2, height // 2 - 40,
            text="GAME OVER",
            fill=food_color,
            font=game_over_font
        )
        retry_button = tk.Button(
            root, text="RETRY",
            font=("Segoe UI", 14, "bold"),
            bg=food_color, fg="white",
            relief="flat",
            command=reset_game
        )
        canvas.create_window(
            game_width // 2, height // 2 + 30,
            window=retry_button
        )
        return
    snake.insert(0, new_head)
    if new_head == food:
        score += score_increment
        create_food()
        if speed > min_speed:
            speed -= 15
    else:
        snake.pop()
    draw_game()
    root.after(speed, move_snake)
def speed_cooldown_fn():
    global speed
    if not game_over and speed < initial_speed:
        speed += 5
    root.after(speed_cooldown, speed_cooldown_fn)
def draw_game():
    canvas.delete("snake")
    canvas.delete("food")
    for i, (x, y) in enumerate(snake):
        draw_block(
            x, y,
            snake_head if i == 0 else snake_color,
            "snake"
        )
    if food:
        draw_block(food[0], food[1], food_color, "food")
    draw_panel()
    draw_speed_dots()
def change_direction(event):
    global direction
    opposite = {
        "Left": "Right",
        "Right": "Left",
        "Up": "Down",
        "Down": "Up"
    }
    if event.keysym in opposite and direction != opposite[event.keysym]:
        direction = event.keysym
# start
root.bind("<Key>", change_direction)
draw_wallpaper()
reset_game()
speed_cooldown_fn()
root.mainloop()
