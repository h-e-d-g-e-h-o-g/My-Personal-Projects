from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
FONT_STYLE = ('Lucida Sans Typewriter', 12, 'normal')
BACKGROUND_COLOR = "#FAF2E1"
BUTTON_STATE = None
BUTTON_TEXT = "Added to Watchlist"

class Interface:
    def __init__(self, shows, shows_library) -> None:
        self.window = Tk()
        self.window.title("Top 100 shows")
        self.window.config(background=BACKGROUND_COLOR)
        self.window.wm_minsize(914, 576)
        self.shows = tuple(shows)
        self.show_poster = None
        self.chosen_show = None
        self.background_image = None
        self.watchlist_button = None
        self.watchlist_shows = []
        self.shows_library = shows_library
        title_label = ttk.Label(text="Top 100 TV Shows of all time", font=('Lucida Sans Typewriter', 35, 'bold'), background=BACKGROUND_COLOR)
        title_label.grid(row=0, column=0, padx=20, pady=10)
        canvas = Canvas(width=864, height=576, background=BACKGROUND_COLOR, highlightthickness=0)
        canvas.grid(row=1, column=0)
        photo_image = PhotoImage(file="images/tv-shows.png")
        canvas.create_image(457, 288, image=photo_image)
        tracker = StringVar()
        # What you'vs chosen
        self.show_chosen = ttk.Combobox(width=50, textvariable=tracker, font=('Lucida Sans Typewriter', 12, 'normal'))
        self.show_chosen['values'] = self.shows
        self.show_chosen.current(0)
        self.show_chosen.bind("<<ComboboxSelected>>", self.show_details)
        # Here, we bind the show_chosen(combobox) with the event(when one of the option in the combobox got selected),
        # When this event occurs, we will call the show_details().
        combostyle = ttk.Style()
        combostyle.theme_create('combostyle', parent='alt',
                        settings={'TCombobox':
                                  {'configure':
                                   {'selectbackground': '#4CAF50',
                                    'fieldbackground': '#f2f2f2',
                                    'foreground': '#333',
                                    'arrowcolor': '#333',
                                    'arrowpadding': (5, 5, 5, 5),
                                    'bordercolor': '#ccc',
                                    'lightcolor': '#fff',
                                    'darkcolor': '#ccc',
                                    }}}
                        )
        combostyle.theme_use('combostyle')
        canvas.create_window(457, 288, window=self.show_chosen)
        #shows_chosen.current()
        self.window.mainloop()

    def show_details(self, event):
        selected_show_name = self.show_chosen.get()
        selected_show_detail = next(show for show in self.shows_library if show["name"] == selected_show_name)
        show_image = self.loading_image(selected_show_detail['src_poster'])
        self.show_detail_window(selected_show_detail, show_image)

    def show_detail_window(self, show_selected, show_image):
        global BUTTON_STATE, BUTTON_TEXT
        page_backgdround = "#668B4F"
        show_window = Toplevel(background=page_backgdround)
        self.chosen_show = show_selected["name"].split(".")[1]
        show_window.title(self.chosen_show)
        # Keep a reference to the PhotoImage due to garbage collection
        self.show_poster = ImageTk.PhotoImage(image=show_image)
        show_poster_label = Label(show_window, image=self.show_poster)
        show_poster_label.grid(row=0, column=0, padx=5, pady=5)
        message = f"Title:{self.chosen_show}\n\nRating: {show_selected['ratings']}\n\nSynopsis: {show_selected['synopsis']}"
        show_canvas = Canvas(show_window, width=500, height=414, background=page_backgdround, highlightthickness=0)
        show_canvas.grid(row=1, column=0, padx=5, pady=5)
        self.background_image = PhotoImage(file="images/background.png")
        show_canvas.create_image(250,207, image=self.background_image)
        show_canvas.create_text(250, 207, text=message, width=220, font=(FONT_STYLE), fill="white")
        if self.chosen_show in self.watchlist_shows:
            BUTTON_STATE = DISABLED
            BUTTON_TEXT = "Added"
        else:
            BUTTON_TEXT = "Add to Watchlist"
        self.watchlist_button = Button(show_window, text=BUTTON_TEXT, font=("Ariel", 20, "bold"), bg="#655465", fg="#F2F1EC",
                                      command=self.add_to_watchlist, state=BUTTON_STATE)
        self.watchlist_button.grid(row=2, column=0, padx=5, pady=5)

    def loading_image(self, image_url):
        response = requests.get(image_url)
        response_data = response.content
        image = Image.open(BytesIO(response_data))
        return image

    def add_to_watchlist(self):
        self.watchlist_shows.append(self.chosen_show)
        self.watchlist_button.config(text="Added", state=DISABLED)
        with open("watchlist.txt", "+a") as f:
            f.write(f"{self.chosen_show}\n")