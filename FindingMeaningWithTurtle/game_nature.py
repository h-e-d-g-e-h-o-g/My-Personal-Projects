from turtle import Turtle, Screen
import color_pixel
import time
screen = Screen()


class Game(Turtle):
    def __init__(self):
        super().__init__()
        screen.bgcolor("pink")
        self.hideturtle()
        self.penup()
        self.setpos(-212, -212)
        self.speed("fastest")
        self.draw_dot()

    def draw_dot(self):
        screen.colormode(255)
        for i in range(4):
            self.forward(20)
        for j in range(8):
            for k in range(7):
                self.dot(15, color_pixel.generate_color())
                self.penup()
                self.forward(40)
                self.pendown()
            self.dot(15, color_pixel.generate_color())
            self.setheading(90)
            self.penup()
            self.forward(40)
            self.pendown()
            if j % 2 == 0:
                self.setheading(180)
            else:
                self.setheading(0)
        self.game_name()

    def game_name(self):
        x = self.xcor() + 125
        y = self.ycor()
        self.penup()
        self.goto(x, y)
        self.color("blue")
        self.write("Answer the  ", align="center", font=('Courier', 45, 'bold'))
        self.draw_turtle()
        time.sleep(1)
        self.goto((5, -310))
        self.color("orange red")
        self.write("Starting...", align="center", font=('Courier', 45, 'bold'))

    def draw_turtle(self):
        x_position = self.xcor() + 200
        buzzo = Turtle()
        buzzo.penup()
        buzzo.setpos(x_position, self.ycor() + 20)
        buzzo.shape("turtle")
        buzzo.shapesize(stretch_wid=3, stretch_len=3)
        buzzo.color("blue")
        time.sleep(0.4)
        buzzo.setheading(90)
