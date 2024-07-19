import turtle
import time
import random

delay = 0.1
score = 0
high_score = 0
black_turtle = None
black_turtle_timer = 0
black_turtle_interval = random.randint(5, 15)

# Set up the screen
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)

# Register new shape for the snake's head and black turtle
wn.register_shape("snake_head", ((-10, -10), (-10, 10), (10, 10), (10, -10)))
wn.register_shape("black_turtle", ((-10, -10), (-10, 10), (10, 10), (10, -10)))

# Snake head
head = turtle.Turtle()
head.shape("snake_head")
head.color("green")
head.penup()
head.goto(0, 0)
head.direction = "right"

# Initial body segment
initial_segment = turtle.Turtle()
initial_segment.speed(0)
initial_segment.shape("square")
initial_segment.color("grey")
initial_segment.penup()
initial_segment.goto(-20, 0)
segments = [initial_segment]

# Snake food
food = turtle.Turtle()
food.speed(0)
foods = ["circle", "square", "triangle", "classic"]
colors = ["orange", "yellow", "green"]
food.penup()

# Black turtle
def create_black_turtle():
    global black_turtle
    black_turtle = turtle.Turtle()
    black_turtle.speed(0)
    black_turtle.shape("black_turtle")
    black_turtle.penup()
    black_turtle.hideturtle()

def change_food():
    """Change the shape and color of the regular food."""
    food.shape(random.choice(foods))
    color = random.choice(colors)
    food.color(color)
    x = random.randint(-270, 270)
    y = random.randint(-270, 270)
    food.goto(x, y)
    return color

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

# Functions
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

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

def reset_game():
    """Reset the game after collision."""
    global score, delay, black_turtle_interval
    time.sleep(1)
    head.goto(0, 0)
    head.direction = "stop"

    # Hide the segments of the body
    for segment in segments:
        segment.goto(1000, 1000)

    # Clear the segments list
    segments.clear()

    # Re-add the initial segment
    segments.append(initial_segment)
    initial_segment.goto(-20, 0)

    # Reset the score
    score = 0

    # Reset the delay
    delay = 0.1

    # Reset the black turtle interval
    black_turtle_interval = random.randint(5, 15)

    pen.clear()
    pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    # Change the food shape and color
    change_food()

# Initialize the game
create_black_turtle()
change_food()

# Keyboard bindings
wn.listen()
wn.onkey(go_up, "Up")
wn.onkey(go_down, "Down")
wn.onkey(go_left, "Left")
wn.onkey(go_right, "Right")

# Main game loop
last_black_turtle_appearance = time.time()

while True:
    wn.update()

    current_time = time.time()

    # Check for a collision with the border
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        reset_game()

    # Check for a collision with the food
    if head.distance(food) < 20:
        # Move the food to a random spot and change its shape and color
        change_food()

        # Add more segments
        for _ in range(3):
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("grey")
            new_segment.penup()
            if segments:
                last_segment = segments[-1]
                new_segment.goto(last_segment.xcor(), last_segment.ycor())
            segments.append(new_segment)

        # Shorten the delay
        delay -= 0.001

        # Increase the score
        score += 10

        if score > high_score:
            high_score = score

        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    # Move the end segments first in reverse order
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    # Check for head collision with body segments
    for segment in segments[1:]:
        if segment.distance(head) < 20:
            reset_game()

    time.sleep(delay)

wn.mainloop()
