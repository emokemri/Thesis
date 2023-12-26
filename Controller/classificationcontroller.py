from Model.model import Model
from View.view import View

import customtkinter as ctk
from tkinter import filedialog

class ClassificationController:
    def __init__(self, model: Model, view: View) -> None:
        ''' Initializes model and view and sets the frame to "classification" '''
        self.model = model
        self.view = view
        self.frame = self.view.frames["classification"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.btn_back.configure(command=self.back_to_calculations)
        self.frame.btn_calculate.configure(command=self.calculate)
        self.frame.btn_file.configure(command=self.save_to_file)


    def back_to_calculations(self) -> None:
        ''' Switch back to Calculations window '''
        for widget in self.frame.frm_solution.winfo_children():
                widget.destroy()

        self.view.switch("calculations")


    def calculate(self) -> None:
        ''' Shows the classification '''
        for widget in self.frame.frm_calculate.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.destroy()

        for widget in self.frame.frm_solution.winfo_children():
            widget.destroy()

        if len(self.model.radix.classification) > 5:
            lbl_error = ctk.CTkLabel(self.frame.frm_solution, text="This classification takes up too much space, try saving it to a file", text_color="red")
            lbl_error.pack()
            return

        # Convert arrays to string representations
        result = [[array.tolist() for array in inner_list] for inner_list in self.model.radix.classification]
        result_string = ', '.join(str(element) for element in result)

        # Join the string representations with ' -> ' separator
        lbl = ctk.CTkLabel(self.frame.frm_solution, text=result_string)
        lbl.pack()


    def save_to_file(self):
        ''' Saves classification to file '''
        for widget in self.frame.frm_calculate.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.destroy()

        result = [[array.tolist() for array in inner_list] for inner_list in self.model.radix.classification]
        
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt")])

        if file_path:
            with open(file_path, 'w') as file:
                file.write(', '.join(str(element) for element in result))