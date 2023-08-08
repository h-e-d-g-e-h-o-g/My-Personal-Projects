from tkinter import *
from PIL import Image, ImageTk
from flightInterface import flightWindow
from flight_search import FlightSearch
from tkinter import messagebox
from findingImage import CityImage
from flight_data import FlightData
BACKGROUND_COLOR = "#F0BB32"
FONT_COLOR = "#F2F1EC"
class UserInterface:
    def __init__(self):
        self.window = Tk()
        self.window.config(background=BACKGROUND_COLOR)
        self.window.title("Best Flight Deal Finder")
        self.canvas = Canvas(width=480, height=270, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=2)
        self.animate_gif("images/airplane_gif.gif")
        self.create_form()
        self.submit_button = Button(text="Submit", font=("Ariel", 25, "bold"), bg="#655465", fg=FONT_COLOR, command=self.get_data )
        self.submit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.window.mainloop()
    
    def create_form(self):
        self.origin_label = Label(text="Origin City:", font=("Ariel", 15, "bold"), fg=FONT_COLOR, bg=BACKGROUND_COLOR)
        self.origin_label.grid(row=1, column=0, padx=10, pady=5)

        self.origin_entry = Entry()
        self.origin_entry.focus()
        self.origin_entry.grid(row=1, column=1, padx=10, pady=5)

        self.destination_label = Label(text="Destination City:", font=("Ariel", 15, "bold"), fg=FONT_COLOR, bg=BACKGROUND_COLOR)
        self.destination_label.grid(row=2, column=0, padx=10, pady=10)

        self.destination_entry = Entry()
        self.destination_entry.grid(row=2, column=1, padx=10, pady=10)

    def animate_gif(self, filepath):
        gif = Image.open(filepath)
        frames = []
        try:
            while True:
                frames.append(ImageTk.PhotoImage(gif))
                gif.seek(len(frames))  # Move to the next frame
        except EOFError:  # Reached the end of the GIF
            pass

        self.current_frame = 0
        # Now, understanding animate_gif()
        # Here, first I open the gif file by having its filepath. and store it into gif.
        # Then, I create the frames list in order to store the gif frames.
        # I use the try and except block in order to handle EOFError.
        # In try block, i am running while true loop because, I don't know the number of frames in the gif.
        # It will run until It encounters the end of file.
        # In while loop, i am turning the first frame of gif file into PhotoImage object and added into the frames list.
        # Then, i need to move on to the next frame. In order to go, I use seek(), that changes the file handle to the index that i passed as the parameter.
        # As parameter, I passed the length of the frame list. Now, its 1, then it will move to the 1 index of the gif file.
        # Next, i have created self.current_frame = 0, in order to track the current frame that's going to be displayed into the canvas.
        def update_frame():
            if self.canvas.winfo_exists():
                self.canvas.delete("all")
                self.canvas.create_image(240, 135, image=frames[self.current_frame])
                self.current_frame = (self.current_frame + 1) % len(frames)
                self.window.after(100, update_frame)
        # Then, inside the animate_gif, i have created update_frame(), it is responsible to update the canvas with the next frame.
        # First, i will delete all the current contents of the canvas in order to avoid overlapping.
        # Then, I am drawing the current frame onto the canvas.
        # Then, i am updating the current frame by 1. Here, i have used modulo operator.
        # Because, For example, i have exceeded the length of the frame list.
        # For example:- If the frame list's length is 5. I have reached to index 4. Then, i need to go back to 0.
        # In order to make the gif animated and frame continous. In this way, the index will be within the frame list's length.
        # Then, there is window.after, it will call the update_frame() after 100ms. In this way, the current frame will be there for 1 sec. 
        update_frame()

    def loading(self, filePath, city_names, IATA_list, image_label, image_tourism, flightData):
        # Clearig out all the widgets in the window
        for widget in self.window.winfo_children():
            widget.destroy()

        airplane_gif = Image.open(filePath)
        airplane_frames = []

        try:
            while True: 
                airplane_frames.append(ImageTk.PhotoImage(airplane_gif))
                airplane_gif.seek(len(airplane_frames))
        except EOFError:
            pass
        
        self.new_canvas = Canvas(width=480, height=447, bg="#3198DA")
        self.new_canvas.grid(row=0, column=0, columnspan=2)
        self.current_loading_frame = 0

        def loading_frames():
            if self.current_loading_frame == 60:
                self.window.destroy()
                flightData.get_price(IATA_list, city_names)
                flight_interface = flightWindow(city_names, IATA_list, image_label, image_tourism, flightData)
            else:
                if self.window.winfo_exists():
                    self.new_canvas.delete("all")
                    self.new_canvas.create_image(240, 224, image=airplane_frames[self.current_loading_frame])
                    self.current_loading_frame += 1
                    self.window.after(50, loading_frames)
        
        loading_frames()

    def get_data(self):
        origin_city = self.origin_entry.get()
        destination_city = self.destination_entry.get()
        cities = [origin_city, destination_city]
        flightSearch = FlightSearch()
        IATA_list = []
        for city in cities:
            IATA_list.append(flightSearch.updating_flight_data(city))
        image = CityImage(cities[1])
        image_label = image.make_request()
        image_tourism = image.get_tourist_images()
        flightData = FlightData()
        # Check if both origin and destination city are entered
        if origin_city and destination_city:
            self.loading("images/airplane_load.gif", cities, IATA_list, image_label, image_tourism, flightData)
        else:
            # Display an error message if either origin or destination city is missing
            messagebox.showerror("Error", "Please enter both origin and destination cities.")
