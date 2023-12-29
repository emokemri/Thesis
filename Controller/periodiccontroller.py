from Model.model import Model
from View.view import View

import customtkinter as ctk
from tkinter import filedialog

class PeriodicController:
    def __init__(self, model: Model, view: View) -> None:
        ''' Initializes model and view and sets the frame to "periodic" '''
        self.model = model
        self.view = view
        self.frame = self.view.frames["periodic"]
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
        ''' Show the periodic points of the system '''
        for widget in self.frame.frm_calculate.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.destroy()

        for widget in self.frame.frm_solution.winfo_children():
            widget.destroy()

        if len(self.model.radix.periodic_points) > 10:
            lbl_error = ctk.CTkLabel(self.frame.frm_solution, text="There are too many periodic points, try saving them to a file", text_color="red")
            lbl_error.pack()
            return
        
        # Convert arrays to string representations
        dimension = self.model.radix.dimension
        if dimension == 1:
            sorted_list = sorted(self.model.radix.periodic_points)
            result_string = ', '.join(f"({element[0]})" for element in sorted_list)

            lbl = ctk.CTkLabel(self.frame.frm_solution, text=result_string)
            lbl.pack()

        else:
            sorted_list = sorted(self.model.radix.periodic_points)
            result_string = ', '.join(str(element) for element in sorted_list)

            lbl = ctk.CTkLabel(self.frame.frm_solution, text=result_string)
            lbl.pack()


    def save_to_file(self):
        ''' Save periodic points to a file '''
        for widget in self.frame.frm_calculate.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.destroy()

        sorted_list = sorted(self.model.radix.periodic_points)
        
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt")])

        if file_path:
            with open(file_path, 'w') as file:
                file.write(', '.join(f"({element[0]})" if len(element) == 1 else str(element) for element in sorted_list))