from Model.model import Model
from View.view import View

import numpy as np
import customtkinter as ctk
import sys

class PhiController:
    def __init__(self, model: Model, view: View) -> None:
        ''' Initializes model and view and sets the frame to "phi" '''
        self.model = model
        self.view = view
        self.frame = self.view.frames["phi"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.btn_back.configure(command=self.back_to_calculations)
        self.frame.btn_calculate.configure(command=lambda: self.calculate(self.frame.frm_entries))


    def back_to_calculations(self) -> None:
        ''' Switch back to Calculations window '''
        for widget in self.frame.frm_solution.winfo_children():
                widget.destroy()

        self.view.switch("calculations")

    def update_view(self) -> None:
        ''' Update Phi window '''
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
        ''' Show Phi function's solution for given lattice point '''
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
        error = False
        for child in master_name.winfo_children():
            if isinstance(child, ctk.CTkEntry):
                if int(child.get()) > sys.maxsize:
                    error = True
                    break
                try:
                    array[col] = int(child.get())
                    col += 1
                except ValueError:
                    error = True
        
        if error:
            lbl_error = ctk.CTkLabel(self.frame.frm_calculate, text="Enter another lattice point", text_color="red")
            lbl_error.pack()
            return

        phi_solution = self.model.radix.phi_n_z(array)
        for i in range(dimension):
            ent = ctk.CTkEntry(self.frame.frm_solution, width=30, fg_color="#98e3d9")
            ent.insert(0, phi_solution[i])
            ent.grid(row=0, column=i+1, padx=2, pady=2)