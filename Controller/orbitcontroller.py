from Model.model import Model
from View.view import View

import numpy as np

import customtkinter as ctk
from tkinter import filedialog
import sys

class OrbitController:
    def __init__(self, model: Model, view: View) -> None:
        ''' Initializes model and view and sets the frame to "orbit" '''
        self.model = model
        self.view = view
        self.frame = self.view.frames["orbit"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.btn_back.configure(command=self.back_to_calculations)
        self.frame.btn_calculate.configure(command=lambda: self.calculate(self.frame.frm_entries))
        self.frame.btn_file.configure(command=self.save_to_file)


    def back_to_calculations(self) -> None:
        ''' Switch back to Calculations window '''
        for widget in self.frame.frm_solution.winfo_children():
                widget.destroy()

        self.view.switch("calculations")


    def update_view(self) -> None:
        ''' Update Orbit window '''
        self.frame.dimension = self.model.radix.dimension

        for widget in self.frame.frm_entries.winfo_children():
            widget.destroy()

        if self.model.radix.dimension == 0:
            lbl_error = ctk.CTkLabel(self.frame.frm_entries, text="Enter the appropriate data on the main window", text_color="red")
            lbl_error.grid(row=0, column=0, padx=2, pady=2)
        else:
            for j in range(self.frame.dimension):
                ent = ctk.CTkEntry(self.frame.frm_entries, width=30, fg_color="#E0FFFF")
                ent.grid(row=0, column=j+1, padx=2, pady=2)


    def calculate(self, master_name) -> None:
        ''' Show the orbit for a given lattice point '''
        for widget in self.frame.frm_calculate.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.destroy()

        dimension = self.model.radix.dimension

        # Initialize a NumPy array with zeros
        array = np.zeros(dimension, dtype=int)

        # Fill the NumPy array with the elements from the entry widgets
        col = 0
        for child in master_name.winfo_children():
            if isinstance(child, ctk.CTkEntry):
                entry_value = child.get()

                if not entry_value:
                    lbl_error = ctk.CTkLabel(self.frame.frm_calculate, text="Enter another lattice point", text_color="red")
                    lbl_error.pack()
                    return

                try:
                    if int(entry_value) > sys.maxsize:
                        lbl_error = ctk.CTkLabel(self.frame.frm_calculate, text="Enter another lattice point", text_color="red")
                        lbl_error.pack()
                        return
                    array[col] = int(child.get())
                    col += 1
                except ValueError:
                    lbl_error = ctk.CTkLabel(self.frame.frm_calculate, text="Enter another lattice point", text_color="red")
                    lbl_error.pack()
                    return
        
                
        if hasattr(self.model.radix, 'orbit'):
            self.model.radix.orbit = []

        self.model.radix.phi_n_recursion(array)

        for widget in self.frame.frm_solution.winfo_children():
            widget.destroy()

        if len(self.model.radix.orbit) > 10:
            lbl_error = ctk.CTkLabel(self.frame.frm_solution, text="Orbit is too long, try saving it to a file", text_color="red")
            lbl_error.pack()
            return

        # Convert arrays to string representations
        result = [[array.tolist() for array in inner_list] for inner_list in self.model.radix.orbit]
        result_string = ' -> '.join(str(element) for element in result)
        lbl = ctk.CTkLabel(self.frame.frm_solution, text=result_string)
        lbl.pack()

        self.model.radix.orbit.clear()


    def save_to_file(self):
        ''' Save orbit to a file '''
        for widget in self.frame.frm_calculate.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.destroy()

        dimension = self.model.radix.dimension

        if dimension == 0:
            return

        # Initialize a NumPy array with zeros
        array = np.zeros(dimension, dtype=int)

        # Fill the NumPy array with the elements from the entry widgets
        col = 0
        for child in self.frame.frm_entries.winfo_children():
            if isinstance(child, ctk.CTkEntry):
                try:
                    array[col] = int(child.get())
                    col += 1
                except ValueError:
                    lbl_error = ctk.CTkLabel(self.frame.frm_calculate, text="Enter another lattice point", text_color="red")
                    lbl_error.pack()
                    return

        self.model.radix.phi_n_recursion(array)

        for widget in self.frame.frm_solution.winfo_children():
            widget.destroy()

        # Convert arrays to string representations
        result = [[array.tolist() for array in inner_list] for inner_list in self.model.radix.orbit]
        result_string = ' -> '.join(str(element) for element in result)

        self.model.radix.orbit.clear()


        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt")])

        if file_path:
            with open(file_path, 'w') as file:
                file.write(result_string)