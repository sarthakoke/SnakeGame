import turtle
import time
import random
import os

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCORE_AREA_Y = 260  # Score display Y-position
SCORE_AREA_HEIGHT = 40  # Height buffer for score display area

# Ask for player name
player_name = turtle.textinput("Player Name", "Enter your name:")

# Score tracking
score = 0
high_score = 0
high_score_name = "None"

# Load high score from file
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        line = f.readline().strip().split(",")
        if len(line) == 2:
            high_score_name = line[0]
            high_score = int(line[1])
else:
    with open("highscore.txt", "w") as f:
        f.write("None,0")

# Create screen
win = turtle.Screen()
win.title("Snake Game")
win.bgcolor("white")
win.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
win.tracer(0)

# Snake head
head = turtle.Turtle()
head.shape("square")
head.color("black")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Food
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

# Score display
pen = turtle.Turtle()
pen.color("blue")
pen.penup()
pen.hideturtle()
pen.goto(0, SCORE_AREA_Y)

# Game Over display
game_over_pen = turtle.Turtle()
game_over_pen.color("red")
game_over_pen.penup()
game_over_pen.hideturtle()
game_over_pen.goto(0, 0)

segments = []

def update_score():
    pen.clear()
    pen.write(f"Score: {score}  High Score: {high_score} ({high_score_name})", align="center", font=("Courier", 18, "normal"))

def is_in_score_area(x, y):
    return y > (SCORE_AREA_Y - SCORE_AREA_HEIGHT)

update_score()

# Movement functions
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def quit_game():    #This function is bound to the Escape key for exiting the game.
    turtle.bye()

# Snake movement
def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    elif head.direction == "down":
        head.sety(head.ycor() - 20)
    elif head.direction == "left":
        head.setx(head.xcor() - 20)
    elif head.direction == "right":
        head.setx(head.xcor() + 20)

# Keyboard bindings
win.listen()
win.onkeypress(go_up, "w")
win.onkeypress(go_down, "s")
win.onkeypress(go_left, "a")
win.onkeypress(go_right, "d")
win.onkeypress(quit_game, "Escape")

# Main game loop
while True:
    win.update()

    # Move segments
    for i in range(len(segments) - 1, 0, -1):
        segments[i].goto(segments[i - 1].pos())
    if segments:
        segments[0].goto(head.pos())

    move()

    # Collision with food
    if head.distance(food) < 20:
        while True:
            x = random.randint(-280, 280)
            y = random.randint(-280, 260 - SCORE_AREA_HEIGHT)  # prevent food in score area
            if not is_in_score_area(x, y):
                break
        food.goto(x, y)

        new_segment = turtle.Turtle()
        new_segment.shape("square")
        new_segment.color("black")
        new_segment.penup()
        new_segment.goto(1000, 1000)  # Avoid flashing black dot in the center
        segments.append(new_segment)

        score += 10
        if score > high_score:
            high_score = score
            high_score_name = player_name
            with open("highscore.txt", "w") as f:
                f.write(f"{high_score_name},{high_score}")

        update_score()

    # Collision with wall
    if abs(head.xcor()) > 290 or abs(head.ycor()) > 290:
        head.goto(0, 0)
        head.direction = "stop"
        head.hideturtle()

        game_over_pen.clear()
        game_over_pen.write("GAME OVER", align="center", font=("Courier", 36, "bold"))
        win.update()
        time.sleep(2)
        game_over_pen.clear()
        head.showturtle()

        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()

        score = 0
        update_score()

    # Collision with self
    for segment in segments:
        if segment.distance(head) < 20:
            head.goto(0, 0)
            head.direction = "stop"
            head.hideturtle()

            game_over_pen.clear()
            game_over_pen.write("GAME OVER", align="center", font=("Courier", 36, "bold"))
            win.update()
            time.sleep(2)
            game_over_pen.clear()
            head.showturtle()

            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()

            score = 0
            update_score()
            break

    time.sleep(0.1)
