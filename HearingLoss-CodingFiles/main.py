from tkinter import *
import pandas, random

BACKGROUND_COLOR = "#B1DDC6"
FONT_TEXT = ('Ariel', 20, 'bold')
CHOOSE = "Start"
TIME = 5
CURRENT_DICT = {}
SIGN_IMG = NONE
ALPHABET_IMG = NONE
DATA_TO_WORK_LIST = []


def card_known(new_window, new_canvas, card_content, card_img, card_back, card_front):
    global DATA_TO_WORK_LIST
    DATA_TO_WORK_LIST.remove(CURRENT_DICT)
    new_data = pandas.DataFrame(DATA_TO_WORK_LIST)
    if CHOOSE == 'Alphabet':
        new_data.to_csv("data/alphabets_to_learn.csv", index=False)
    elif CHOOSE == 'Word':
        new_data.to_csv("data/words_to_learn.csv", index=False)
    random_create(new_window, new_canvas, card_content, card_img, card_back, card_front)


def random_create(new_window, new_canvas, card_content, card_img, card_back, card_front):
    global TIME, DATA_TO_WORK_LIST
    new_window.after_cancel(TIME)
    if CHOOSE == 'Alphabet':
        try:
            with open("data/alphabets_to_learn.csv") as f:
                data_to_work = pandas.read_csv("data/alphabets_to_learn.csv")

        except FileNotFoundError:
            with open("data/Alphabet_data.csv") as f:
                data_to_work = pandas.read_csv("data/Alphabet_data.csv")
        finally:
            DATA_TO_WORK_LIST = data_to_work.to_dict(orient="records")

    elif CHOOSE == 'Word':
        try:
            with open("data/words_to_learn.csv") as f:
                data_to_work = pandas.read_csv("data/words_to_learn.csv")

        except FileNotFoundError:
            with open("data/Words_data.csv") as f:
                data_to_work = pandas.read_csv("data/Words_data.csv")
        finally:
            DATA_TO_WORK_LIST = data_to_work.to_dict(orient="records")

    global CURRENT_DICT, ALPHABET_IMG
    CURRENT_DICT = random.choice(DATA_TO_WORK_LIST)
    ALPHABET_IMG = PhotoImage(file=CURRENT_DICT[CHOOSE])
    new_canvas.itemconfig(card_img, image=card_front)
    new_canvas.itemconfig(card_content, image=ALPHABET_IMG)
    TIME = new_window.after(2000, random_sign, new_canvas, card_img, card_content, card_back)


def random_sign(new_canvas, card_img, card_content, card_back):
    new_canvas.itemconfig(card_img, image=card_back)
    global SIGN_IMG
    SIGN_IMG = PhotoImage(file=CURRENT_DICT['Sign'])
    new_canvas.itemconfig(card_content, image=SIGN_IMG)


def choose_alphabet():
    window.destroy()
    global CHOOSE
    CHOOSE = 'Alphabet'
    create_new_window()


def choose_word():
    window.destroy()
    global CHOOSE
    CHOOSE = 'Word'
    create_new_window()


def create_new_window():
    new_window = Tk()
    new_window.title("HEARING THE LOST ONE")
    new_window.config(padx=50, pady=50, background="#B1DDC6")
    new_canvas = Canvas(width=800, height=526, background="#B1DDC6", highlightthickness=0)
    card_back = PhotoImage(file="images/card_back.png")
    card_front = PhotoImage(file="images/card_front.png")
    card_img = new_canvas.create_image(400, 263, image=card_front)
    alphabet_char = PhotoImage(file="images/start.png")
    card_content = new_canvas.create_image(400, 263, image=alphabet_char)
    new_canvas.grid(row=0, column=0, columnspan=2)
    wrong_img = PhotoImage(file="images/wrong.png")
    wrong_button = Button(image=wrong_img, highlightthickness=0, command=lambda: random_create(new_window, new_canvas,
                                                                                               card_content, card_img,
                                                                                               card_back, card_front))
    wrong_button.grid(row=1, column=0)
    right_img = PhotoImage(file="images/right.png")
    right_button = Button(image=right_img, highlightthickness=0, command=lambda: card_known(new_window, new_canvas,
                                                                                            card_content, card_img,
                                                                                            card_back, card_front))
    right_button.grid(row=1, column=1)
    new_window.after(1000, random_create, new_window, new_canvas, card_content, card_img, card_back, card_front)
    new_window.mainloop()


window = Tk()
window.title("HEARING THE LOST ONE")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
canvas = Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0)
circle_img = PhotoImage(file="images/circle.png")
canvas.create_image(400, 263, image=circle_img)
hearing_logo = PhotoImage(file="images/hearing_symbol.png")
canvas.create_image(400, 280, image=hearing_logo)
canvas.grid(row=0, column=0, columnspan=2)
alphabet_button = Button(text="Alphabets", font=FONT_TEXT, bg="#25327B", fg='white', command=choose_alphabet)
alphabet_button.grid(row=1, column=0)
words_button = Button(text="Words", width=8, font=FONT_TEXT, bg="#25327B", fg='white', command=choose_word)
words_button.grid(row=1, column=1)
window.mainloop()
