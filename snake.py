import random
from tkinter import *

WIDTH = 700
HEIGHT = 700
SPEED = 100
SIZE = 50
BODY = 3 
COL = "#08ff00"
BG_COLOR = "#000000"
FOOD_COL = "#ff0000"
direction_move_start = 'right'
pending_direction = direction_move_start
SCORE = 0

class Snake:
    def __init__(self):
        self.body_size = BODY
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SIZE, y + SIZE, fill=COL, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        self.coordinates = self.place_food()

        x, y = self.coordinates
        canvas.create_oval(x, y, x + SIZE, y + SIZE, fill=FOOD_COL, tag="food")

    def place_food(self):
        while True:
            x = random.randint(0, int(WIDTH / SIZE - 1)) * SIZE 
            y = random.randint(0, int(HEIGHT / SIZE - 1)) * SIZE 
            if [x, y] not in snake.coordinates:
                return [x, y]

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction_move_start == "up":
        y -= SIZE
    elif direction_move_start == "down":
        y += SIZE
    elif direction_move_start == "left":
        x -= SIZE
    elif direction_move_start == "right":
        x += SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SIZE, y + SIZE, fill=COL)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global SCORE
        SCORE += 1

        if SCORE >= 10 and SCORE <= 15:
                global SPEED
                print("Game is speeding up!!!")
                SPEED = 90
        elif SCORE >= 16 and SCORE <= 20: 
                print("It's getting even faster!!!")
                SPEED = 70
        elif SCORE > 20: 
                print("You have reached the max speed!!!")
                SPEED = 50

        label.config(text="Score: {}".format(SCORE))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collision(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food) 

def change_direction(new_direction):
    global direction_move_start

    if new_direction == 'left' and direction_move_start != 'right':
        direction_move_start = new_direction
    elif new_direction == 'right' and direction_move_start != 'left':
        direction_move_start = new_direction
    elif new_direction == 'up' and direction_move_start != 'down':
        direction_move_start = new_direction
    elif new_direction == 'down' and direction_move_start != 'up':
        direction_move_start = new_direction    

def check_collision(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return True
    
    for body in snake.coordinates[1:]:
        if x == body[0] and y == body[1]:
            return True
        
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2,
                       canvas.winfo_height()/2,
                       font=('Arial', 70), text="Game Over", fill="red", tag="GameOver")

window = Tk()
window.title("SNAKE")
window.resizable(False, False)

canvas = Canvas(window, bg=BG_COLOR, height=HEIGHT, width=WIDTH)
canvas.pack()

label = Label(window, text="Score: {}".format(SCORE), font=('Arial', 55))
label.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

position1 = int((screen_width / 2) - (window_width / 2))
pos2 = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{position1}+{pos2}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)  

window.mainloop()