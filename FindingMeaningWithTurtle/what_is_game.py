from turtle import Turtle, Screen
import random
import time
from film import movie_list
from gk import gk_list
from computer import computer_list
from video_game import vg_list
screen = Screen()


class Question(Turtle):
    def __init__(self, response):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.response = response
        self.score = Turtle()
        self.score_value = 0
        self.chance_value = 8
        self.difficulty = 'Easy'
        self.options = {'m': movie_list, 'g': gk_list, 'c': computer_list, 'v': vg_list}
        self.check_category()

    def check_category(self):
        for option in self.options:
            if self.response == option:
                self.loop_question(self.options[option])
                break
        else:
            self.invalid_input()

    def start_game(self, level, count):
        self.show_score()
        choose = random.choice(level)
        quiz = choose['question']
        level.remove(choose)
        answer = screen.textinput("Answer in True/False and 'To quit':- type 'q'", f"Q.{count} {quiz}")
        self.setpos(-5, 50)
        if answer is None:
            return 'Q'
        answer = answer.title()
        if answer == choose['correct_answer']:
            self.color('Blue')
            self.write("Right!", align="center", font=('Courier', 50, 'bold'))
            self.update_score()
        elif answer == 'Q':
            return 'Q'
        else:
            self.color("Red")
            self.write("Wrong!", align="center", font=('Courier', 50, 'bold'))
            self.diminish_chance()

    def loop_question(self, quiz_list):
        count = 1
        for question_ask in range(25):
            if question_ask == 0:
                level = quiz_list[0]
            elif question_ask == 8:
                self.difficulty = 'Medium'
                level = quiz_list[1]
            elif question_ask == 17:
                self.difficulty = 'Hard'
                level = quiz_list[2]
            screen.bgcolor("spring green")
            stop = self.start_game(level, count)
            if stop == 'Q':
                break
            count += 1
            time.sleep(1.2)
            screen.clear()
            if self.chance_value < 0:
                break
        self.goto(0, 0)
        screen.bgcolor("dark orange")
        if self.score_value == 25:
            self.write(f"Congratulations!", align="center", font=('Courier', 40, 'bold'))
            self.goto(0, -70)
            self.write(f"You get {self.score_value}/25", align="center", font=('Courier', 50, 'bold'))
        else:
            self.color("Red")
            self.write(f"Game Over!", align="center", font=('Courier', 50, 'bold'))
            self.goto(0, -70)
            self.color("Blue")
            self.write(f"You get {self.score_value}/25", align="center", font=('Courier', 50, 'bold'))


    def invalid_input(self):
        screen.clear()
        self.setpos(-5, 50)
        self.write("Invalid Input!", align="center", font=('Courier', 50, 'bold'))

    def show_score(self):
        self.score.speed("fastest")
        self.score.hideturtle()
        self.score.penup()
        self.score.goto(-300, 200)
        self.score.write(f"Score: {self.score_value}", align="center", font=("Courier", 25, 'normal'))
        self.score.goto(-20, 200)
        self.score.write(f"Chances: {self.chance_value}", align="center", font=("Courier", 25, 'normal'))
        self.score.goto(260, 200)
        self.score.write(f"Level: {self.difficulty}", align="center", font=("Courier", 25, 'normal'))

    def update_score(self):
        self.score.clear()
        self.score_value += 1
        self.show_score()

    def diminish_chance(self):
        self.chance_value -= 1

