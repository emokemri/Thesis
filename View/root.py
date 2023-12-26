import customtkinter as ctk

class Root(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Set the background color for the window
        self.configure(fg_color="#ADD8E6")
        self.resizable(False, False)
        self.title("Szakdolgozat")