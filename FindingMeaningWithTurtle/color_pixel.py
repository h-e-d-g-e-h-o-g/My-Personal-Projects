from turtle import Turtle, Screen
import random
screen = Screen()
screen.colormode(255)


def generate_color():
    red = random.randint(0, 255)
    blue = random.randint(0, 255)
    green = random.randint(0, 255)
    color = (red, blue, green)
    return color

