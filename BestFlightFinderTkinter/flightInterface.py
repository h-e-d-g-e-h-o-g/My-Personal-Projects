from tkinter import *
from PIL import Image, ImageTk
import io
from tkinter import filedialog
import requests
BACKGROUND_COLOR = "#B8E7E1"
FONT_COLOR = "black"
class flightWindow:
    def __init__(self, city_name_list, city_iata_code_list, image_url, image_tourism, flightDataObject):
        self.flight_window = Tk()
        self.flight_window.title("Flight details")
        self.flight_window.config(bg=BACKGROUND_COLOR)
        self.image_urls = image_tourism
        image_response = requests.get(image_url)
        image_data = image_response.content
        image = Image.open(io.BytesIO(image_data))
        photo = ImageTk.PhotoImage(image)
        self.canvas = Canvas(width=520, height=320, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.create_image(260, 160, image=photo)
        self.canvas.grid(row=0, column=0, columnspan=3)
        self.details_canvas = Canvas(width=520, height=300, bg=BACKGROUND_COLOR, highlightthickness=0)
        details_img = ImageTk.PhotoImage(file="images/flight_details.png")
        self.details_canvas.create_image(260, 150, image=details_img)
        y_position = 100
        line_spacing = 30
        self.details_canvas.create_text(260, y_position, text=f"Origin City:  {city_name_list[0]}", font=("Arial", 16, "italic"),fill=FONT_COLOR)
        y_position += line_spacing
        self.details_canvas.create_text(260, y_position, text=f"Destination City:  {city_name_list[1]}", font=("Arial", 16, "italic"),fill=FONT_COLOR)
        y_position += line_spacing
        self.details_canvas.create_text(260, y_position, text=f"Flight Price: ₹{flightDataObject.price}", font=("Arial", 16, "italic"),fill=FONT_COLOR)
        y_position += line_spacing
        self.details_canvas.create_text(260, y_position, text=f"Flight type: Round with no stopovers", font=("Arial", 16, "italic"),fill=FONT_COLOR)
        y_position += line_spacing
        self.details_canvas.create_text(260, y_position, text=f"Flight Date: {flightDataObject.out_date}-->{flightDataObject.return_date}", font=("Arial", 16, "italic"),fill=FONT_COLOR)
        y_position += line_spacing
        self.details_canvas.create_text(260, y_position, text=f"{city_name_list[0]}'s IATA Code:  {city_iata_code_list[0]}", font=("Arial", 16, "italic"),fill=FONT_COLOR)
        y_position += line_spacing
        self.details_canvas.create_text(260, y_position, text=f"{city_name_list[1]}'s IATA Code:  {city_iata_code_list[1]}", font=("Arial", 16, "italic"),fill=FONT_COLOR)
        self.details_canvas.grid(row=1, column=0, pady=5, columnspan=3)
        self.download_button = Button(text="Download", font=("Ariel", 20, "bold"), bg="#655465", fg="#F2F1EC", command=lambda: self.download_details(city_name_list, city_iata_code_list, flightDataObject))
        self.download_button.grid(row=2, column=0, pady=5)
        self.tourism_places = Button(text="Tourist sites", font=("Ariel", 20, "bold"), bg="#655465", fg="#F2F1EC",
                                      command=self.create_tourist_window)
        self.tourism_places.grid(row=2, column=1, pady=5)
        self.exit_button = Button(text="Exit", font=("Ariel", 20, "bold"), bg="#655465", fg="#F2F1EC",
                                      command=self.ui_build)
        self.exit_button.grid(row=2, column=2, pady=5)
        self.flight_window.mainloop()

    def download_details(self, city_name_list, city_iata_code_list, flightDataObject):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file_name:
                    # Here, my open() has not the way to encode "₹" symbol due to its default encoding.
                    # For that, we are choosing utf-8 encoding format. As it supports all unicode characters.
                    file_name.write(f"Origin City:  {city_name_list[0]}\n")
                    file_name.write(f"Destination City:  {city_name_list[1]}\n")
                    file_name.write(f"Flight Price: ₹{flightDataObject.price}\n")
                    file_name.write("Flight type: Round with no stopovers\n")
                    file_name.write(f"Flight Date: {flightDataObject.out_date}-->{flightDataObject.return_date}\n")
                    file_name.write(f"{city_name_list[0]}'s IATA Code:  {city_iata_code_list[0]}\n")
                    file_name.write(f"{city_name_list[1]}'s IATA Code:  {city_iata_code_list[1]}\n")
                print("Downloaded Successfully")
            
            except Exception as e:
                print(f"Something error occurred while downloading: {e}")
        
        else:
            print("No file path selected!")

    def ui_build(self):
        self.flight_window.destroy()
        
    def create_tourist_window(self):
        tourist_window = Toplevel()
        tourist_window.title("Tourist Attraction")
        photo_objects = []
        unique_image_urls = set(self.image_urls) 
        for image_url in unique_image_urls:
            image_response = requests.get(image_url)
            image_data = image_response.content
            image = Image.open(io.BytesIO(image_data))
            photo = ImageTk.PhotoImage(image)
            photo_objects.append(photo)
    
        i = 0
        j = 0
        for photo_object in photo_objects:
            label = Label(tourist_window, image=photo_object)
            label.image = photo_object  # Keep a reference to avoid garbage collection
            label.grid(row=i, column=j)
            j += 1
            if j > 0 and j % 2 == 0:
                i += 1
                j = 0
        tourist_window.mainloop()
