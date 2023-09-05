import customtkinter as ctk
import tkinter as tk
import numpy as np
import json
import sys


matrix = np.array([])
vectors = np.array([])

class RadixSystem:
    def __init__(self, matrix=None, vectors=None):
        self.matrix = matrix if matrix is not None else np.array([])
        self.vectors = vectors if vectors is not None else np.array([])

    def set_matrix(self, matrix):
        self.matrix = np.array(matrix)

    def set_vectors(self, vectors):
        self.vectors = np.array(vectors)

    def get_matrix(self):
        return self.matrix

    def get_vectors(self):
        return self.vectors



# Generate matrix entries
def generate_matrix(master_name):
    for widget in master_name.winfo_children():
        widget.destroy()

    dims = int(ent_dimension.get())

    for i in range(dims):
        for j in range(dims):
            ent = ctk.CTkEntry(master=master_name, width=30, fg_color="#E0FFFF")
            ent.grid(row=i, column=j, padx=2, pady=2)

# Save matrix entries
def save_matrix(master_name):
    global matrix

    children = master_name.winfo_children()
    dimension = int(ent_dimension.get())
    
    # Initialize a NumPy array with zeros
    array = np.zeros((dimension, dimension), dtype=int)
    matrix.fill(0)

    # Fill the NumPy array with the elements from the entry widgets
    index = 0
    for i in range(dimension):
        for j in range(dimension):
            array[i, j] = int(children[index].get())
            index += 1

    matrix = array
    print(matrix)

# Generate vector length entries and labels
def generate_vectors(master_name):
    for widget in master_name.winfo_children():
        widget.destroy()

    rows = int(ent_number_of_vectors.get())
    dimension = int(ent_dimension.get())

    for i in range(rows):
        lbl_vector_length = ctk.CTkLabel(master=master_name, text=f"{i+1}. vector:")
        lbl_vector_length.grid(row=i, column=0, padx=2, pady=2)
        for j in range(dimension):
            ent = ctk.CTkEntry(master=master_name, width=30, fg_color="#E0FFFF")
            ent.grid(row=i, column=j+1, padx=2, pady=2)
 


# Save vectors to a NumPy array
def save_vectors(master_name):
    global vectors

    dimension = int(ent_dimension.get())
    number_of_vectors = int(ent_number_of_vectors.get())

    vectors.fill(0)

    # Initialize a NumPy array with zeros
    array = np.zeros((number_of_vectors, dimension), dtype=int)

    # Fill the NumPy array with the elements from the entry widgets
    row = 0
    col = 0
    for child in master_name.winfo_children():
        if isinstance(child, ctk.CTkEntry):
            if col >= dimension:
                col = 0
                row += 1
            array[row, col] = int(child.get())
            col += 1

    vectors = array



# Load matrix and vectors from a file
def load_from_file():
    global matrix
    global vectors

    # Open a file for loading
    filepath = tk.filedialog.askopenfilename(
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
    )
    if not filepath:
        return

    # Erasing contents
    matrix.fill(0)
    vectors.fill(0)

    # Loading the JSON file contents
    with open(filepath, mode="r", encoding="utf-8") as input_file:
        data = json.load(input_file)
        
        matrix = np.array(data["matrix"])
        vectors = np.array(data["vectors"])
        
    print(matrix)
    print(vectors)
    

# Function to create a new window
def open_new_window(main_window):
    def close_app():
        main_window.destroy()  # Destroy the root window to close the whole app

    main_window.withdraw()
    new_window = ctk.CTkToplevel(fg_color="#ADD8E6")  # Create a new top-level window
    new_window.title("New window")   # Set the title of the new window
    frm_calculate = ctk.CTkFrame(master=new_window, fg_color="#ADD8E6")
    btn_calculate = ctk.CTkButton(master=frm_calculate, text="Calculate", command=calculate)
    btn_calculate.grid(row=0, column=0, padx=5, pady=5)
    frm_calculate.pack()
    btn_back = ctk.CTkButton(new_window, text="Back to Main Window", command=lambda: show_main_window(main_window, new_window))
    btn_back.pack()


    # Bind the closing event to the function that closes the whole app
    new_window.protocol("WM_DELETE_WINDOW", close_app)


def show_main_window(main_window, new_window=None):
    if new_window:
        new_window.destroy()  # Close the new window
    main_window.deiconify()  # Show the main window


# Calculate determinant
def calculate():
    global matrix
    print(np.linalg.det(matrix))

def from_command_line(filepath):
    global matrix
    global vectors

    # Erasing contents
    matrix.fill(0)
    vectors.fill(0)

    # Loading the JSON file contents
    with open(filepath, mode="r", encoding="utf-8") as input_file:
        data = json.load(input_file)
        
        matrix = np.array(data["matrix"])
        vectors = np.array(data["vectors"])

if __name__ == "__main__":

    # Get the command-line arguments
    arguments = sys.argv

    app = ctk.CTk(fg_color="#ADD8E6")
    app.title("Szakdolgozat")

    # The first argument (arguments[0]) is the script filename, so skip it
    # The second argument (arguments[1]) is the first command-line argument
    if len(arguments) > 1:
        filepath = arguments[1]
        from_command_line(filepath)
        open_new_window(app)

    frm_form = ctk.CTkFrame(master=app, fg_color="#ADD8E6")

    lbl_dimension = ctk.CTkLabel(master=frm_form, text="The system's dimension:")
    ent_dimension = ctk.CTkEntry(master=frm_form, width=50)

    btn_generate = ctk.CTkButton(master=frm_form, text="Generate", command=lambda: generate_matrix(frm_matrix))

    for i in range(3):
        app.columnconfigure(i, weight=1)

    # Use the grid geometry manager to place the Label and Entry widgets
    frm_form.pack()
    lbl_dimension.grid(row=0, column=0, padx=5, pady=5)
    ent_dimension.grid(row=0, column=1, padx=5, pady=5)
    btn_generate.grid(row=0, column=2, padx=5, pady=5)

    lbl_spacemaker = ctk.CTkFrame(master=app, height=20, fg_color="#ADD8E6")

    frm_matrix = ctk.CTkFrame(master=app, fg_color="#ADD8E6", height=20)
    frm_matrix.pack()

    frm_save_matrix = ctk.CTkFrame(master=app, fg_color="#ADD8E6")
    btn_save_matrix = ctk.CTkButton(master=frm_save_matrix, text="Save matrix", command=lambda: save_matrix(frm_matrix))
    frm_save_matrix.pack()
    btn_save_matrix.grid(row=0, column=0, padx=5, pady=5)

    lbl_spacemaker.pack()

    frm_number_of_vectors = ctk.CTkFrame(master=app, fg_color="#ADD8E6")
    lbl_number_of_vectors = ctk.CTkLabel(master=frm_number_of_vectors, text="number of vectors:")
    ent_number_of_vectors = ctk.CTkEntry(master=frm_number_of_vectors, width=50)
    lbl_number_of_vectors.grid(row=0, column=0, padx=5, pady=5)
    ent_number_of_vectors.grid(row=0, column=1, padx=5, pady=5)

    frm_vectors = ctk.CTkFrame(master=app, fg_color="#ADD8E6", height=20)
    btn_generate_vector_lengths = ctk.CTkButton(master=frm_number_of_vectors, text="Generate", command=lambda: generate_vectors(frm_vectors))
    btn_generate_vector_lengths.grid(row=0, column=2, padx=5, pady=5)
    frm_number_of_vectors.pack()
    frm_vectors.pack()

    frm_generate_vectors = ctk.CTkFrame(master=app, fg_color="#ADD8E6", height=20)
    btn_save_vectors = ctk.CTkButton(master=frm_generate_vectors, text="Save vectors", command=lambda: save_vectors(frm_vectors))
    btn_save_vectors.grid(row=0, column=0, padx=5, pady=5)
    frm_generate_vectors.pack()

    lbl_spacemaker = ctk.CTkFrame(master=app, height=20, fg_color="#ADD8E6")
    lbl_spacemaker.pack()

    frm_load_from_file = ctk.CTkFrame(master=app, fg_color="#ADD8E6")
    btn_load_from_file = ctk.CTkButton(master=frm_load_from_file, text="Load from file", command=load_from_file)
    btn_load_from_file.grid(row=0, column=0, padx=5, pady=5)
    frm_load_from_file.pack()

    lbl_spacemaker = ctk.CTkFrame(master=app, height=20, fg_color="#ADD8E6")
    lbl_spacemaker.pack()

    '''
    frm_calculate = ctk.CTkFrame(master=app, fg_color="#ADD8E6")
    btn_calculate = ctk.CTkButton(master=frm_calculate, text="Calculate", command=calculate)
    btn_calculate.grid(row=0, column=0, padx=5, pady=5)
    frm_calculate.pack()
    '''

    # Create a button to open the new window
    frm_open_new_window = ctk.CTkFrame(master=app, fg_color="#ADD8E6")
    btn_open_new_window = ctk.CTkButton(frm_open_new_window, text="Open New Window", command=lambda: open_new_window(app))
    btn_open_new_window.grid(row=0, column=0, padx=5, pady=5)
    frm_open_new_window.pack()

    app.mainloop()
