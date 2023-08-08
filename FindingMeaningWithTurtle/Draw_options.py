from turtle import Turtle, Screen
import time
screen = Screen()


class Option(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.goto(-7, 168)
        self.options = ["'m' for Movie quiz", "'g' for GK quiz", "'c' for Computer quiz", "'v' for Video Games quiz"]
        self.y_position = 140
        self.options_for_game()

    def options_for_game(self):
        screen.bgcolor("cornflower blue")
        self.write("Choose the category!", align="center", font=('Courier', 40, 'bold'))
        # self.goto((-145, 140))
        for option in self.options:
            self.goto((-145, self.y_position))
            self.write(f"Type {option}", align="left", font=('Courier', 15, 'bold'))
            self.y_position -= 30
        time.sleep(1.2)



        # choose = random.choice(film.movie_easy)
        # screen.clear()
        # question = choose['question']
        # answer = screen.textinput("Answer in True/False", f"Q.1 {question}")
        # screen.clear()
        # quest.setpos(-5, -10)
        # if answer == choose['correct_answer']:
        #     quest.color("Blue")
        #     quest.write("Right!", align="center", font=('Courier', 25, 'bold'))
        # else:
        #     quest.color("Red")
        #     quest.write("Wrong!", align="center", font=('Courier', 25, 'bold'))
