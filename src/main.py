from turtle import Turtle, Screen
from random import randint
from threading import get_ident

def create_tail_part(position, heading = 0):
    tail_part = Turtle(shape="square", visible=False)
    tail_part.speed(speed="fastest")
    tail_part.penup()
    tail_part.shapesize(0.8, 0.8)
    tail_part.setheading(heading)
    tail_part.setpos(position[0], position[1])

    return tail_part

def move_snake_tail_part(position, heading = 0, tail_part_size = 20):
    if heading == 0:
        return (position[0] + tail_part_size, position[1])
    elif heading == 180:
        return (position[0] - tail_part_size, position[1])
    elif heading == 90:
        return (position[0], position[1] + tail_part_size)
    else:
        return (position[0], position[1] - tail_part_size)

def create_gift(width, height, tail_part_size = 20):
    half_width = round((width - width * 0.1) / 2)
    half_height = round((height - height * 0.1) / 2)
    
    x = randint(half_width * -1, half_width)
    y = randint(half_height * -1, half_height)

    gift = create_tail_part([x - x % tail_part_size, y - y % tail_part_size])
    gift.showturtle()
    return gift

def has_collected_gift(snake, gift):
    if gift is None:
        return False
    
    head_pos = snake[0].pos()
    gift_pos = gift.pos()
    return head_pos[0] == gift_pos[0] and head_pos[1] == gift_pos[1]

def add_new_tail_part(snake, tail_part_size = 20):
    last_tail_part_pos = snake[len(snake) - 1].pos()
    new_tail_part_spots = [
        (last_tail_part_pos[0] + tail_part_size, last_tail_part_pos[1]),
        (last_tail_part_pos[0] - tail_part_size, last_tail_part_pos[1]),
        (last_tail_part_pos[0], last_tail_part_pos[1] + tail_part_size),
        (last_tail_part_pos[0], last_tail_part_pos[1] - tail_part_size)
    ]
    
    for new_tail_pos in new_tail_part_spots:
        is_free = True
        for tail_part in snake:
            tail_part_pos = tail_part.pos()
            if new_tail_pos[0] == tail_part_pos[0] and new_tail_pos[1] == tail_part_pos[1]:
                is_free = False
                break
            
        if is_free:
            new_tail_part = create_tail_part(new_tail_pos)
            snake.append(new_tail_part)
            return
  

def render_loop(screen, snake):
    
    for tail_part in snake:
        tail_part.showturtle()
    
    def handle_move_up():
        print('UP ' + str(get_ident()))
        head = snake[0]
        if head.heading() == 270:
            return
        head.setheading(90)
        
    def handle_move_down():
        print('DOWN ' + str(get_ident()))
        head = snake[0]
        if head.heading() == 90:
            return
        head.setheading(270)
        
    def handle_move_left():
        print('LEFT ' + str(get_ident()))
        head = snake[0]
        if head.heading() == 0:
            return
        head.setheading(180)
        
    def handle_move_right():
        print('RIGHT ' + str(get_ident()))
        head = snake[0]
        if head.heading() == 180:
            return
        head.setheading(0)
        
    screen.onkeypress(handle_move_up, "w")
    screen.onkeypress(handle_move_down, "s")
    screen.onkeypress(handle_move_left, "a")
    screen.onkeypress(handle_move_right, "d")
    
    def next_frame(gift = None):
        print("Frame " + str(get_ident()))
        if gift is None:
            gift = create_gift(screen.window_width(), screen.window_height())
            
        head = snake[0]
        new_tail_part = create_tail_part(move_snake_tail_part(head.pos(), head.heading()), head.heading())
        snake.insert(0, new_tail_part)
        
        last_tail_part = snake.pop()
        last_tail_part.hideturtle()
        last_tail_part.clear()
        new_tail_part.showturtle()
        
        if has_collected_gift(snake, gift):
            add_new_tail_part(snake)
            gift.hideturtle()
            gift.clear()
            gift = create_gift(screen.window_width(), screen.window_height())
        
        screen.ontimer(lambda: next_frame(gift), 100)
            
    next_frame()

snake = []
screen = Screen()

for i in range(3):
    tail_part = create_tail_part(move_snake_tail_part([i * -1, 0]))
    snake.append(tail_part)

render_loop(screen, snake)

screen.listen()
screen.exitonclick()
