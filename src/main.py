from turtle import Turtle, Screen
from random import randint
from math import ceil


class SnakeGame:

    def __init__(self) -> None:
        self.score = 0
        self.snake = []
        self.screen = Screen()
        self.screen.setup(600, 600)
        self.screen.bgcolor("black")
        self.tail_part_size = 20
        self.gift = None
        self.heading = 0
        self.create_score()
        for i in range(3):
            tail_part = self.create_part(
                self.move_snake_tail_part([i * -1, 0]))
            self.snake.append(tail_part)

    def create_score(self):
        score_pen = Turtle(visible=False)
        score_pen.penup()
        screen_height = self.screen.window_height() / 2
        score_pen.setpos(0, screen_height - screen_height * 0.1)
        score_pen.color("white")
        score_pen.write("Score: 0", move=False, align="center",
                        font=("Arial", 18, "normal"))
        self.score_pen = score_pen

    def update_score(self):
        self.score += 1
        self.score_pen.clear()
        self.score_pen.write(f"Score: {self.score}", move=False, align="center",
                             font=("Arial", 18, "normal"))

    def game_over(self):
        game_over_pen = Turtle(visible=False)
        game_over_pen.penup()
        game_over_pen.color("red")
        game_over_pen.write("Game over!", move=False, align="center",
                            font=("Arial", 24, "normal"))

    def move_snake_tail_part(self, position, heading=0):
        if heading == 0:
            return (position[0] + self.tail_part_size, position[1])
        elif heading == 180:
            return (position[0] - self.tail_part_size, position[1])
        elif heading == 90:
            return (position[0], position[1] + self.tail_part_size)
        else:
            return (position[0], position[1] - self.tail_part_size)

    def create_part(self, position, heading=0, color="white"):
        tail_part = Turtle(shape="square", visible=False)
        tail_part.color(color)
        tail_part.speed(speed="fastest")
        tail_part.penup()
        tail_part.shapesize(0.8, 0.8)
        tail_part.setheading(heading)
        tail_part.setpos(position[0], position[1])

        return tail_part

    def create_gift(self, width, height):
        half_width = round((width - width * 0.1) / 2)
        half_height = round((height - height * 0.1) / 2)

        x = randint(half_width * -1, half_width)
        y = randint(half_height * -1, half_height)

        self.gift = self.create_part(
            position=[x - x % self.tail_part_size, y - y %
                      self.tail_part_size],
            color="blue"
        )
        self.gift.showturtle()

    def has_collected_gift(self):
        if self.gift is None:
            return False

        head_pos = self.snake[0].pos()
        gift_pos = self.gift.pos()
        return self.compare_positions(head_pos, gift_pos)

    def compare_positions(self, pos1, pos2):
        return pos1[0] == pos2[0] and pos1[1] == pos2[1]

    def add_new_tail_part(self):
        last_tail_part_pos = self.snake[len(self.snake) - 1].pos()
        new_tail_part_spots = [
            (last_tail_part_pos[0] +
             self.tail_part_size, last_tail_part_pos[1]),
            (last_tail_part_pos[0] -
             self.tail_part_size, last_tail_part_pos[1]),
            (last_tail_part_pos[0],
             last_tail_part_pos[1] + self.tail_part_size),
            (last_tail_part_pos[0],
             last_tail_part_pos[1] - self.tail_part_size)
        ]

        for new_tail_pos in new_tail_part_spots:
            is_free = True
            for tail_part in self.snake:
                tail_part_pos = tail_part.pos()
                if self.compare_positions(new_tail_pos, tail_part_pos):
                    is_free = False
                    break

            if is_free:
                new_tail_part = self.create_part(new_tail_pos)
                self.snake.append(new_tail_part)
                return

    def collision_happened(self):
        head_pos = self.snake[0].pos()
        tail = slice(1, len(self.snake))

        half_width = ceil(self.screen.window_width() / 2)
        half_height = ceil(self.screen.window_height() / 2)

        if head_pos[0] >= half_width or head_pos[0] <= half_width * -1:
            return True

        if head_pos[1] >= half_height or head_pos[1] <= half_height * -1:
            return True

        for tail_part in self.snake[tail]:
            if self.compare_positions(head_pos, tail_part.pos()):
                return True

        return False

    def handle_move_up(self):
        if self.heading == 270:
            return
        self.heading = 90

    def handle_move_down(self):
        if self.heading == 90:
            return
        self.heading = 270

    def handle_move_left(self):
        if self.heading == 0:
            return
        self.heading = 180

    def handle_move_right(self):
        if self.heading == 180:
            return
        self.heading = 0

    def start(self):
        for tail_part in self.snake:
            tail_part.showturtle()

        self.screen.onkeypress(self.handle_move_up, "w")
        self.screen.onkeypress(self.handle_move_down, "s")
        self.screen.onkeypress(self.handle_move_left, "a")
        self.screen.onkeypress(self.handle_move_right, "d")

        self.create_gift(self.screen.window_width(),
                         self.screen.window_height())

        self.next_frame()

        self.screen.listen()
        self.screen.exitonclick()

    def next_frame(self):
        head = self.snake[0]
        new_tail_part = self.create_part(
            self.move_snake_tail_part(head.pos(), self.heading), self.heading
        )
        self.snake.insert(0, new_tail_part)

        last_tail_part = self.snake.pop()
        last_tail_part.hideturtle()
        last_tail_part.clear()
        new_tail_part.showturtle()

        if self.collision_happened():
            self.game_over()
            return

        if self.has_collected_gift():
            self.update_score()
            self.add_new_tail_part()
            self.gift.hideturtle()
            self.gift.clear()
            self.create_gift(
                self.screen.window_width(), self.screen.window_height())

        self.screen.ontimer(lambda: self.next_frame(), 100)


game = SnakeGame()
game.start()
