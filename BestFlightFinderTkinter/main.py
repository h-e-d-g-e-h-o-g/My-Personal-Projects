from ui import UserInterface
from tkinter import messagebox
input = True
while input:
    ui = UserInterface()
    input = messagebox.askyesno(title="Your Best Flight Deal Finder", message="Want to continue?")
    