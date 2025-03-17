from tkinter import *
import random

GAME_WIDTH = 1100
GAME_HEIGHT = 600
SPEED = 150
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "white"
FOOD_COLOR = "orange"
BACKGROUND_COLOR = "#000000"

game_running = True

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = [[0, 0] for _ in range(BODY_PARTS)]
        self.squares = [canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake") 
                         for x, y in self.coordinates]

class Food:
    def __init__(self):
        self.coordinates = [random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE,
                    random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE]

        canvas.create_oval(self.coordinates[0], self.coordinates[1], 
                           self.coordinates[0] + SPACE_SIZE, self.coordinates[1] + SPACE_SIZE, 
                           fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    global direction, game_running, high_score, score
    if not game_running:
        return
    
    x, y = snake.coordinates[0]
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    
    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)
    
    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text=f"Score: {score}  High Score: {high_score}")
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    
    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    if (x, y) in snake.coordinates[1:]:
        return True
    return False

def game_over():
    global game_running, high_score, score
    game_running = False
    if score > high_score:
        high_score = score
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 + 50,
                       font=('consolas', 30), text="Press 'Enter' to Restart", fill="white", tag="restart")

def restart_game():
    global game_running, score, direction, snake, food
    canvas.delete(ALL)
    game_running = True
    score = 0
    label.config(text=f"Score: {score}  High Score: {high_score}")
    direction = 'down'
    snake = Snake()
    food = Food()
    next_turn(snake, food)

# Initialize Game
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
high_score = 0
direction = 'down'

label = Label(window, text=f"Score: {score}  High Score: {high_score}", font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f"{window_width}x{window_height}+{(screen_width - window_width) // 2}+{(screen_height - window_height) // 2}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<Return>', lambda event: restart_game())

snake = Snake()
food = Food()
next_turn(snake, food)

window.mainloop()
