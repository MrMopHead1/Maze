import turtle
import random
from collections import deque
import math

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("A Maze Game")
wn.setup(700, 700)

class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)

class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.gold = 0

    def go_up(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() + 24
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_down(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() - 24
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_left(self):
        move_to_x = self.xcor() - 24
        move_to_y = self.ycor()
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_right(self):
        move_to_x = self.xcor() + 24
        move_to_y = self.ycor()
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 5:
            return True
        else:
            return False


class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.original_position = (x, y)
        self.goto(x, y)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

    def move_to_random_location(self):
        new_x, new_y = get_random_empty_spot()
        self.goto(new_x, new_y)
        self.showturtle()

    def reset_position(self):
        self.goto(self.original_position)
        self.showturtle()

class Enemy(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("red")
        self.penup()
        self.speed(-10000)

    def move_towards_player(self):
        if self.distance(player) < 24:
            print("Player caught!")
            restart_game()
            return

        start = (self.xcor(), self.ycor())
        goal = (player.xcor(), player.ycor())

        path = self.bfs(start, goal)
        if path:
            self.goto(path[1])

    def bfs(self, start, goal):
        queue = deque([[start]])
        visited = set()
        visited.add(start)

        while queue:
            path = queue.popleft()
            x, y = path[-1]

            if (x, y) == goal:
                return path

            for move_x, move_y in [(24, 0), (-24, 0), (0, 24), (0, -24)]:
                next_pos = (x + move_x, y + move_y)
                if next_pos not in walls and next_pos not in visited:
                    new_path = list(path)
                    new_path.append(next_pos)
                    queue.append(new_path)
                    visited.add(next_pos)
        return None

def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.stamp()
                walls.append((screen_x, screen_y))
            if character == "P":
                player.goto(screen_x, screen_y)
            if character == "E":
                enemy.goto(screen_x, screen_y)
            if character == "T":
                treasures.append(Treasure(screen_x, screen_y))

def get_random_empty_spot():
    while True:
        x = random.randint(0, 24)
        y = random.randint(0, 24)
        screen_x = -288 + (x * 24)
        screen_y = 288 - (y * 24)
        if (screen_x, screen_y) not in walls:
            return (screen_x, screen_y)

def restart_game():
    global score, high_score
    player.goto(-288 + 24, 288 - 24)  # Reset player to initial position
    enemy.goto(216, -216)  # Reset enemy to initial position
    for treasure in treasures:
        treasure.reset_position()  # Reset treasures to their original positions
    if score > high_score:
        high_score = score
    score = 0
    update_score_display()

def update_score_display():
    score_display.clear()
    score_display.goto(-290, 310)
    score_display.write(f"Score: {score}", align="left", font=("Arial", 16, "normal"))
    score_display.goto(150, 310)
    score_display.write(f"High Score: {high_score}", align="left", font=("Arial", 16, "normal"))

pen = Pen()
player = Player()
enemy = Enemy()

walls = []
treasures = []

score = 0
high_score = 0

level_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XP XXXXXXX           XXXXX",
    "X  XXXXXXX   XXXXX  XXXXXX",
    "X       XX XXXXXXX  XXXXXX",
    "X       XX XXX          XX",
    "XXXXXX  XX XXX      T    X",
    "XXXXXX  XX XXXXXXX  XXXXXX",
    "X  XXX       XXXXX  XXXXXX",
    "X  XXX  XXXXXXXXXXXXXXXXXX",
    "X         XXXXXXXXXXXXXXXX",
    "X                  XXXXXXX",
    "XXXXXXXXXXXX     XXXXXXXXX",
    "XXXXXXXXXXXXX  XXXXXXXXXXX",
    "X                 XXXXXXXX",
    "X XX  XXXXXXXXX        XXX",
    "X  X      XXXXXXXXXXXX   X",
    "XX XXXXX           XXXX  X",
    "X  X                XXXX X",
    "X         XXXXXXXXXXXXXX X",
    "XXXX    XXXXXXX    XXXX  X",
    "XXXX                    XX",
    "XXXX  XXXXXXXXX  E      XX",
    "XX    XXXXXXXXX XXXXXXXXXX",
    "XXXX  XXXXXXXXX    XXXXXXX",
    "XXXX      XXXXX    XXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXX"
]

setup_maze(level_1)
score_display = turtle.Turtle()
score_display.hideturtle()
score_display.color("white")
score_display.penup()
update_score_display()

# KeyBoardBinding
turtle.listen()
turtle.onkey(player.go_left, "Left")
turtle.onkey(player.go_right, "Right")
turtle.onkey(player.go_up, "Up")
turtle.onkey(player.go_down, "Down")

# Main game loop
def game_loop():
    enemy.move_towards_player()
    wn.ontimer(game_loop, 250)

wn.tracer(0)

game_loop()

while True:
    for treasure in treasures:
        if player.is_collision(treasure):
            player.gold += treasure.gold
            score += treasure.gold
            if score > high_score:
                high_score = score
            print("Player Gold: {}".format(player.gold))
            treasure.move_to_random_location()
            update_score_display()

    wn.update()
