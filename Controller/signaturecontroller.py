from Model.model import Model
from View.view import View

import customtkinter as ctk
from tkinter import filedialog

class SignatureController:
    def __init__(self, model: Model, view: View) -> None:
        ''' Initializes model and view and sets the frame to "signature" '''
        self.model = model
        self.view = view
        self.frame = self.view.frames["signature"]
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
        ''' Show the signature of the system '''
        for widget in self.frame.frm_calculate.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.destroy()

        for widget in self.frame.frm_solution.winfo_children():
            widget.destroy()

        if len(self.model.radix.signature) > 10:
            lbl_error = ctk.CTkLabel(self.frame.frm_solution, text="This signature takes up too much space, try saving it to a file", text_color="red")
            lbl_error.pack()
            return

        # Convert arrays to string representations
        result_string = '(' + ', '.join(str(element) for element in self.model.radix.signature) + ')'

        lbl = ctk.CTkLabel(self.frame.frm_solution, text=result_string)
        lbl.pack()


    def save_to_file(self):
        ''' Save signature to file '''
        for widget in self.frame.frm_calculate.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.destroy()

        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt")])

        if file_path:
            with open(file_path, 'w') as file:
                file.write('(' + ', '.join(str(element) for element in self.model.radix.signature) + ')')