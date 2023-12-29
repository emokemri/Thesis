from Model.model import Model
from View.view import View

import customtkinter as ctk
import tkinter as tk

import numpy as np
import json
import re
import sys


class MainController:
    def __init__(self, model: Model, view: View) -> None:
        ''' Initializes model and view and sets the frame to "mainwindow" '''
        self.model = model
        self.view = view
        self.frame = self.view.frames["mainwindow"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.btn_generate.configure(command=lambda: self.generate_matrix(self.frame.frm_matrix))
        self.frame.btn_save_matrix.configure(command=lambda: self.save_matrix(self.frame.frm_matrix))
        self.frame.btn_generate_digits.configure(command=lambda: self.generate_digits(self.model.radix.determinant))
        self.frame.btn_save_digits.configure(command=self.save_digits)
        self.frame.btn_load_from_file.configure(command=self.load_from_file)
        self.frame.btn_open_new_window.configure(command=self.open_new_window)
        self.frame.combo_box.configure(command=self.combobox_selection_changed)


    def generate_matrix(self, master_name) -> None:
        ''' Generate matrix entries '''
        for widget in master_name.winfo_children():
            widget.destroy()

        for widget in self.frame.frm_save_matrix.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.destroy()

        for widget in self.frame.frm_load_from_file.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.destroy()
        
        for widget in self.frame.frm_open_new_window.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.destroy()

        for widget in self.frame.frm_optional.winfo_children():
            widget.grid_forget()

        for widget in self.frame.frm_digits.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.grid_forget()

            if isinstance(widget, ctk.CTkEntry):
                widget.grid_forget()

            if isinstance(widget, ctk.CTkButton):
                widget.grid_forget()

        for widget in self.frame.frm_save_digits.winfo_children():
            widget.pack_forget()

        for widget in self.frame.frm_combo.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.destroy()

        self.frame.lbl_base.pack_forget()
        self.frame.frm_digits.configure(height=10)
        self.frame.frm_optional.configure(height=5)

        try:
            dims = int(self.frame.ent_dimension.get())
            if dims < 1:
                lbl = ctk.CTkLabel(master=master_name, text="Invalid dimension", text_color="red")
                lbl.pack()
                return
            if dims > 10:
                lbl = ctk.CTkLabel(master=master_name, text="The dimension is too high, try loading from file", text_color="red")
                lbl.pack()
                return
            
            self.frame.lbl_base.pack()
            self.model.radix.matrix.fill(0)
            self.model.radix.digits.fill(0)
            self.model.radix.dimension = (int(self.frame.ent_dimension.get()))

            for i in range(dims):
                for j in range(dims):
                    ent = ctk.CTkEntry(master=master_name, width=30, fg_color="#E0FFFF")
                    ent.grid(row=i, column=j, padx=2, pady=2)

        except ValueError:
            lbl = ctk.CTkLabel(master=master_name, text="Invalid dimension", text_color="red")
            lbl.pack()
            self.model.radix.dimension = 0


    def save_matrix(self, master_name) -> None:
        ''' Save matrix entries '''
        for widget in self.frame.frm_save_matrix.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.destroy()

        children = master_name.winfo_children()
        try:
            dimension = int(self.frame.ent_dimension.get())
            if dimension < 1 or dimension > 10:
                lbl = ctk.CTkLabel(self.frame.frm_save_matrix, text="Enter the dimension", text_color="red")
                lbl.pack()
                return
        except ValueError:
            lbl_error = ctk.CTkLabel(self.frame.frm_save_matrix, text="Enter the dimension", text_color="red")
            lbl_error.pack()
            return
        
        # Initialize a NumPy array with zeros
        array = np.zeros((dimension, dimension), dtype=int)
        self.model.radix.matrix.fill(0)

        # Fill the NumPy array with the elements from the entry widgets
        index = 0
        error = False
        for i in range(dimension):
            for j in range(dimension):
                entry_value = children[index].get()

                if not entry_value:
                    error = True
                    break

                # Check if the entry is bigger than sys.maxsize
                try:
                    if int(entry_value) > sys.maxsize:
                        error = True
                        break
                    array[i, j] = int(entry_value)
                    index += 1
                except ValueError:
                    error = True
                    break

        if error:
            lbl_error = ctk.CTkLabel(self.frame.frm_save_matrix, text="Enter another matrix", text_color="red")
            lbl_error.pack()
            return


        self.model.radix.matrix = array
        self.model.radix.set_U_G()
        self.model.radix.determinant = self.model.radix.calculate_determinant_abs()

        if self.model.radix.determinant == 0:
            lbl_error = ctk.CTkLabel(self.frame.frm_save_matrix, text="Matrix is not expansive", text_color="red")
            lbl_error.pack()
            return
        
        lbl = ctk.CTkLabel(self.frame.frm_save_matrix, text="Matrix saved successfully", text_color="green")
        lbl.pack()


    def combobox_selection_changed(self, choice):
        ''' Called when combobox selection changes, set the system's digit set '''

        for widget in self.frame.frm_digits.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.destroy()
            if isinstance(widget, ctk.CTkEntry):
                widget.destroy()
            
        for widget in self.frame.frm_combo.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.destroy()

        for widget in self.frame.frm_optional.winfo_children():
            widget.grid_forget()
        
        for widget in self.frame.frm_save_digits.winfo_children():
            widget.pack_forget()
        
        if not hasattr(self.model.radix, 'determinant'):
            lbl_error = ctk.CTkLabel(self.frame.frm_digits, text="Enter the base matrix", text_color="red")
            lbl_error.pack()
            return
        
        self.frame.frm_optional.pack()

        try:
            dim = int(self.frame.ent_dimension.get())
            if dim == 0:
                lbl_error = ctk.CTkLabel(self.frame.frm_digits, text="Enter the base matrix", text_color="red")
                lbl_error.pack()
                return
        except ValueError:
            lbl_error = ctk.CTkLabel(self.frame.frm_digits, text="Enter the base matrix", text_color="red")
            lbl_error.pack()
            return

        try:
            det = self.model.radix.calculate_determinant_abs()
            if det == 0:
                lbl_error = ctk.CTkLabel(self.frame.frm_digits, text="Enter the base matrix", text_color="red")
                lbl_error.pack()
                return
        except ValueError:
            lbl_error = ctk.CTkLabel(self.frame.frm_digits, text="Enter the base matrix", text_color="red")
            lbl_error.pack()
            return
        
        self.frame.ent_number_of_digits.delete(0, ctk.END)
        
        if choice == "Custom":
            self.generate_custom(self.frame.frm_digits)

        elif choice == "J-canonical":
            self.generate_j()

        elif choice == "Canonical":
            self.frame.ent_number_of_digits.grid_forget()
            self.model.radix.canonical_digits(det)
            lbl = ctk.CTkLabel(self.frame.frm_combo, text="Digits are successfully generated", text_color="green")
            lbl.pack()
        
        elif choice == "J-symmetrical":
            self.generate_j()
        
        elif choice == "Symmetrical":
            self.frame.ent_number_of_digits.pack_forget()
            self.model.radix.symmetric(det)
            lbl = ctk.CTkLabel(self.frame.frm_combo, text="Digits are successfully generated", text_color="green")
            lbl.pack()

        else:
            lbl_error = ctk.CTkLabel(self.frame.frm_combo, text="Invalid digit set type", text_color="red")
            lbl_error.pack()
            return


    def generate_custom(self, master_name):
        ''' If custom digit set was chosen
         Generates an entry for number of digits '''
        for widget in master_name.winfo_children():
            widget.grid_forget()

        for widget in self.frame.frm_optional.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.grid_forget()
            if isinstance(widget, ctk.CTkEntry):
                widget.grid_forget()

        self.frame.lbl_number_of_digits.configure(text="Number of digits:")
        self.frame.lbl_number_of_digits.grid(row=0, column=0, padx=5, pady=5)
        self.frame.ent_number_of_digits.grid(row=0, column=1, padx=5, pady=5)
        self.frame.btn_generate_digits.grid(row=0, column=2, padx=5, pady=5)


    def generate_digits(self, det):
        ''' Generate digits based on the chosen type of digit set '''
        for widget in self.frame.frm_digits.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.grid_forget()

            if isinstance(widget, ctk.CTkEntry):
                widget.destroy()

            if isinstance(widget, ctk.CTkButton):
                widget.grid_forget()

        for widget in self.frame.frm_save_digits.winfo_children():
            widget.pack_forget()

        if self.frame.combo_box.get() == "Custom":
            try:
                rows = int(self.frame.ent_number_of_digits.get())
                if rows > 10:
                    lbl = ctk.CTkLabel(master=self.frame.frm_digits, text="The number of digits is too high, try loading from file", text_color="red")
                    lbl.grid(row=0, column=0)
                    return
                if rows < 1:
                    lbl = ctk.CTkLabel(master=self.frame.frm_digits, text="The number of digits is invalid", text_color="red")
                    lbl.grid(row=0, column=0)
                    return
            except ValueError:
                lbl_error = ctk.CTkLabel(self.frame.frm_digits, text="Invalid number of digits", text_color="red")
                lbl_error.grid(row=0, column=0)
                return
            
            try:
                dimension = int(self.frame.ent_dimension.get())
            except ValueError:
                lbl_error = ctk.CTkLabel(self.frame.frm_digits, text="Invalid dimension", text_color="red")
                lbl_error.grid(row=0, column=0)
                return

            rows = int(self.frame.ent_number_of_digits.get())
            dimension = int(self.frame.ent_dimension.get())

            # Configure row and column weights
            self.frame.frm_digits.columnconfigure(0, weight=1)  # Column 0 takes all available space
            self.frame.frm_digits.rowconfigure(0, weight=1)     # Row 0 takes all available space

            
            for i in range(rows):
                lbl_digits_length = ctk.CTkLabel(master=self.frame.frm_digits, text=f"{i+1}. digit:")
                lbl_digits_length.grid(row=i, column=0, padx=2, pady=2)
                for j in range(dimension):
                    ent = ctk.CTkEntry(master=self.frame.frm_digits, width=30, fg_color="#E0FFFF")
                    ent.grid(row=i, column=j+1, padx=2, pady=2)
            
            self.frame.btn_save_digits.pack()
        
        elif self.frame.combo_box.get() == "J-canonical":
            try:
                index = int(self.frame.ent_number_of_digits.get())
                if index > self.model.radix.dimension or index < 1:
                    lbl = ctk.CTkLabel(master=self.frame.frm_digits, text="The j index is out of range", text_color="red")
                    lbl.grid(row=0, column=0)
                    return
                
                self.model.radix.canonical_j_digits(det, index-1)
                lbl = ctk.CTkLabel(self.frame.frm_digits, text="Digits are successfully generated", text_color="green")
                lbl.grid(row=0, column=0)

            except ValueError:
                lbl_error = ctk.CTkLabel(self.frame.frm_digits, text="Invalid j index", text_color="red")
                lbl_error.grid(row=0, column=0)
                return
            
        elif self.frame.combo_box.get() == "J-symmetrical":
            try:
                index = int(self.frame.ent_number_of_digits.get())
                if index > self.model.radix.dimension or index < 1:
                    lbl = ctk.CTkLabel(master=self.frame.frm_digits, text="The j index is out of range", text_color="red")
                    lbl.grid(row=0, column=0)
                    return
                
                self.model.radix.symmetric_j(det, index-1)
                lbl = ctk.CTkLabel(self.frame.frm_digits, text="Digits are successfully generated", text_color="green")
                lbl.grid(row=0, column=0)

            except ValueError:
                lbl_error = ctk.CTkLabel(self.frame.frm_digits, text="Invalid j index", text_color="red")
                lbl_error.grid(row=0, column=0)
                return


    def save_digits(self) -> None:
        ''' Save digits to a NumPy array if the chosen digit set was custom '''
        if self.frame.combo_box.get() == "Custom":
            for widget in self.frame.frm_save_digits.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.destroy()


            dimension = int(self.frame.ent_dimension.get())
            number_of_digits = int(self.frame.ent_number_of_digits.get())

            self.model.radix.digits.fill(0)

            # Initialize a NumPy array with zeros
            array = np.zeros((number_of_digits, dimension), dtype=int)

            # Fill the NumPy array with the elements from the entry widgets
            row = 0
            col = 0
            error = False
            for child in self.frame.frm_digits.winfo_children():
                if isinstance(child, ctk.CTkEntry):
                    if col >= dimension:
                        col = 0
                        row += 1

                    entry_value = child.get()

                    if not entry_value:
                        error = True
                        break

                    try:
                        if int(entry_value) > sys.maxsize:
                            error = True
                            break
                        array[row, col] = int(child.get())
                        col += 1
                    except ValueError:
                        error = True

            if error:
                lbl_error = ctk.CTkLabel(self.frame.frm_save_digits, text="Invalid digit set", text_color="red")
                lbl_error.pack()
                return

            self.model.radix.digits = array

            lbl = ctk.CTkLabel(self.frame.frm_save_digits, text="Digits saved successfully", text_color="green")
            lbl.pack()

        else:
            return
        

    def generate_j(self):
        ''' Generate entry for j index '''
        for widget in self.frame.frm_digits.winfo_children():
            widget.grid_forget()

        for widget in self.frame.frm_optional.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.grid_forget()
            if isinstance(widget, ctk.CTkEntry):
                widget.grid_forget()

        self.frame.lbl_number_of_digits.configure(text="J index:")
        self.frame.lbl_number_of_digits.grid(row=0, column=0, padx=5, pady=5)
        self.frame.ent_number_of_digits.grid(row=0, column=1, padx=5, pady=5)
        self.frame.btn_generate_digits.grid(row=0, column=2, padx=5, pady=5)


    def extract_number(self, string):
        ''' Helper function for load_from_file, gets the number in parantheses '''

        # Using regular expression to extract the number
        match = re.search(r'\((.*?)\)', string)
        if match:
            number = match.group(1)
            return int(number)
        else:
            raise ValueError("No number found within parentheses")

    
    def load_from_file(self) -> None:
        ''' Load matrix and digits from a file '''
        for widget in self.frame.frm_save_matrix.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.destroy()

        for widget in self.frame.frm_load_from_file.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.destroy()
        
        for widget in self.frame.frm_open_new_window.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.destroy()

        for widget in self.frame.frm_digits.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.destroy()
            if isinstance(widget, ctk.CTkEntry):
                widget.destroy()
        
        for widget in self.frame.frm_matrix.winfo_children():
            widget.destroy()

        self.frame.frm_matrix.configure(height=5)

        self.frame.lbl_base.pack_forget()
        for widget in self.frame.frm_optional.winfo_children():
            widget.grid_forget()

        for widget in self.frame.frm_digits.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.grid_forget()

            if isinstance(widget, ctk.CTkEntry):
                widget.grid_forget()

            if isinstance(widget, ctk.CTkButton):
                widget.grid_forget()

        for widget in self.frame.frm_save_digits.winfo_children():
            widget.pack_forget()

        for widget in self.frame.frm_combo.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.destroy()
        
        self.frame.frm_digits.configure(height=10)
        self.frame.frm_optional.configure(height=5)
        self.frame.ent_dimension.delete(0, ctk.END)

        # Open a file for loading
        filepath = tk.filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if not filepath:
            return

        # Erasing contents
        self.model.radix.matrix.fill(0)
        self.model.radix.digits.fill(0)
        
        # Loading the JSON file contents
        try:
            with open(filepath, mode="r", encoding="utf-8") as input_file:
                data = json.load(input_file)
                
                data["base"][0][0]
                data["digits"][0][0]

                self.model.radix.matrix = np.array(data["base"])
                self.model.radix.dimension = len(self.model.radix.matrix[0])

                # Check if "digits" is a string indicating a special value
                if isinstance(data["digits"], str) and data["digits"] == "canonical()":
                    self.model.radix.canonical_digits(self.model.radix.calculate_determinant_abs())

                elif isinstance(data["digits"], str) and data["digits"].startswith("j-canonical"):
                    self.model.radix.canonical_j_digits(self.model.radix.calculate_determinant_abs(), self.extract_number(data["digits"]))

                elif isinstance(data["digits"], str) and data["digits"] == "symmetrical()":
                    self.model.radix.symmetric(self.model.radix.calculate_determinant_abs())
                
                elif isinstance(data["digits"], str) and data["digits"].startswith("j-symmetrical"):
                    self.model.radix.symmetric_j(self.model.radix.calculate_determinant_abs(), self.extract_number(data["digits"]))

                elif isinstance(data["digits"], list) and isinstance(data["digits"][0], list):
                    self.model.radix.digits = np.array(data["digits"])
                
                else:
                    lbl = ctk.CTkLabel(self.frame.frm_load_from_file, text="Matrix and digits could not be loaded", text_color="red")
                    lbl.pack()
                    return

                self.model.radix.set_U_G()

                lbl_success = ctk.CTkLabel(self.frame.frm_load_from_file, text="Matrix and digits are successfully loaded", text_color="green")
                lbl_success.pack()

        except:
            lbl = ctk.CTkLabel(self.frame.frm_load_from_file, text="Matrix and digits could not be loaded", text_color="red")
            lbl.pack()

    
    def open_new_window(self) -> None:
        ''' Opening Calculations window '''
        for widget in self.frame.frm_open_new_window.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.destroy()

        if self.model.radix.matrix.size == 0 or self.model.radix.digits.size == 0:
            lbl_error = ctk.CTkLabel(self.frame.frm_open_new_window, text="Enter another matrix and/or digit set", text_color="red")
            lbl_error.pack()
        
        elif not self.model.radix.is_radix():
            lbl_error = ctk.CTkLabel(self.frame.frm_open_new_window, text="The given system is not a radix system", text_color="red")
            lbl_error.pack()

        else:
            for widget in self.frame.frm_open_new_window.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.destroy()

            self.model.radix.find_periodic_points()
            if len(self.model.radix.lattice_points) == 0:
                lbl_error = ctk.CTkLabel(self.frame.frm_open_new_window, text="The given system has too many lattice points", text_color="red")
                lbl_error.pack()
                return
            
            self.view.switch("calculations")
