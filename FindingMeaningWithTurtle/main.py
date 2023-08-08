from turtle import Turtle, Screen
import time
from game_nature import Game
from Draw_options import Option
from what_is_game import Question
screen = Screen()
screen.setup(width=800, height=800)
time.sleep(1)
game = Game()
time.sleep(0.5)
screen.clear()
option = Option()
response = screen.textinput("Quiz(True/False)", "Enter the category!")
screen.clear()
question = Question(response)


screen.exitonclick()
