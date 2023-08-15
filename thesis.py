import customtkinter as ctk
import tkinter as tk
import numpy as np


matrix = []
matrix_entries = []
vector_length_entries = []
vector_length_labels = []
vector_entries = []
vectors = []
matrix_np = []

# Generate matrix entries
def generate_matrix(master_name):
    global matrix_entries

    # Clear the existing matrix before creating a new one
    for row in matrix_entries:
        for entry in row:
            entry.destroy()

    matrix_entries = []

    rows = int(ent_rows.get())
    cols = int(ent_columns.get())

    for i in range(rows):
        row_entries = []
        for j in range(cols):
            ent = ctk.CTkEntry(master=master_name, width=30, fg_color="#E0FFFF")
            ent.grid(row=i, column=j, padx=2, pady=2)
            row_entries.append(ent)
        matrix_entries.append(row_entries)

# Save matrix entries to a 2D array
def save_matrix(master_name):
    global matrix
    children = master_name.winfo_children()
    # Initialize an empty 2D array with the specified number of rows and columns
    array_2d = [[0 for _ in range(int(ent_columns.get()))] for _ in range(int(ent_rows.get()))]

    # Fill the 2D array with the elements from the 1D array
    index = 0
    for i in range(int(ent_rows.get())):
        for j in range(int(ent_columns.get())):
            array_2d[i][j] = int(children[index].get())
            index += 1

    matrix = array_2d

# Generate vector length entries and labels
def generate_vector_lengths(master_name):
    global vector_length_entries
    global vector_length_labels
    global vector_entries

    # Clear the existing vectors before creating a new one
    for row in vector_entries:
        row.destroy()

    # Clear the existing matrix before creating a new one
    for row in vector_length_labels:
        row.destroy()

    for row in vector_length_entries:
        row.destroy()

    vector_length_entries = []
    vector_length_labels = []

    rows = int(ent_number_of_vectors.get())

    for i in range(rows):
        lbl_vector_length = ctk.CTkLabel(master=master_name, text=f"length of {i+1}. vector:")
        lbl_vector_length.grid(row=i, column=0, padx=2, pady=2)
        ent = ctk.CTkEntry(master=master_name, width=30)
        ent.grid(row=i, column=1, padx=2, pady=2)
        vector_length_entries.append(ent)
        vector_length_labels.append(lbl_vector_length)

# Create vector entries
def generate_vectors(master_name):
    global vector_entries

    # Clear the existing vectors before creating a new one
    for row in vector_entries:
        row.destroy()

    vector_entries = []

    rows = int(ent_number_of_vectors.get())

    for i in range(rows*2):
        if i%2 == 1:
            vector_length = int(master_name.winfo_children()[i].get())
            for j in range(vector_length):
                ent = ctk.CTkEntry(master=master_name, width=30, fg_color="#E0FFFF")
                ent.grid(row=int(i/2), column=2+j, padx=2, pady=2)
                vector_entries.append(ent)

# Save vectors to a list
def save_vectors(master_name):
    global vectors

    vectors.clear()

    rows = int(ent_number_of_vectors.get())

    vector_lengths = []
    
    index = 0
    
    i = 0
    while i < len(master_name.winfo_children()):
        if i%2 == 1 and i < rows*2:
            vector_lengths.append(int(master_name.winfo_children()[i].get()))
            i += 1
        elif i >= rows*2 and index < len(vector_lengths):
            curr_vector = []
            for j in range(vector_lengths[index]):
                curr_vector.append(int(master_name.winfo_children()[i+j].get()))
            i += vector_lengths[index]
            vectors.append(curr_vector)
            index += 1
        else:
            i += 1
    
# Load matrix and vectors from a file
def load_from_file():
    # Open a file for loading
    global matrix
    global vectors
    filepath = tk.filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return

    # Erasing contents
    matrix.clear()
    matrix = []
    vectors.clear()
    vectors = []

    # Loading the file contents
    with open(filepath, mode="r", encoding="utf-8") as input_file:
        text = input_file.read().split('*')

        # Split the matrix_text[0] into lines
        matrix_lines = text[0].split('\n')
        
        # Remove any empty lines
        matrix_lines = [line for line in matrix_lines if line.strip()]

        matrix = [[int(num) for num in line.split(',')] for line in matrix_lines]
        
        vector_lines = text[1].split('\n')
        vector_lines = [line for line in vector_lines if line.strip()]
        vectors = [[int(num) for num in line.split(',')] for line in vector_lines]
        
        print(matrix)
        print(vectors)
    
# Calculate determinant and check if it matches the specified value
def calculate():
    global matrix_np
    global matrix

    matrix_np = np.array(matrix)
    print(np.linalg.det(matrix_np))
    if np.linalg.det(matrix_np) == int(ent_number_of_vectors.get()):
        print("Radix")
    else:
        print("Not radix")



if __name__ == "__main__":
    app = ctk.CTk(fg_color="#ADD8E6")
    app.title("Szakdolgozat")
    frm_form = ctk.CTkFrame(master=app, fg_color="#ADD8E6")

    lbl_rows = ctk.CTkLabel(master=frm_form, text="rows:")
    ent_rows = ctk.CTkEntry(master=frm_form, width=50)

    lbl_columns = ctk.CTkLabel(master=frm_form, text="columns:")
    ent_columns = ctk.CTkEntry(master=frm_form, width=50)

    btn_generate = ctk.CTkButton(master=frm_form, text="Generate", command=lambda: generate_matrix(frm_matrix))

    for i in range(4):
        app.columnconfigure(i, weight=1)

    # Use the grid geometry manager to place the Label and Entry widgets
    frm_form.pack()
    lbl_rows.grid(row=0, column=0, padx=5, pady=5)
    ent_rows.grid(row=0, column=1, padx=5, pady=5)
    lbl_columns.grid(row=0, column=2, padx=5, pady=5)
    ent_columns.grid(row=0, column=3, padx=5, pady=5)
    btn_generate.grid(row=0, column=4, padx=5, pady=5)

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
    btn_generate_vector_lengths = ctk.CTkButton(master=frm_number_of_vectors, text="Generate", command=lambda: generate_vector_lengths(frm_vectors))
    btn_generate_vector_lengths.grid(row=0, column=2, padx=5, pady=5)
    frm_number_of_vectors.pack()
    frm_vectors.pack()

    frm_generate_vectors = ctk.CTkFrame(master=app, fg_color="#ADD8E6", height=20)
    btn_generate_vectors = ctk.CTkButton(master=frm_generate_vectors, text="Create vectors", command=lambda: generate_vectors(frm_vectors))
    btn_generate_vectors.grid(row=0, column=0, padx=5, pady=5)
    btn_save_vectors = ctk.CTkButton(master=frm_generate_vectors, text="Save vectors", command=lambda: save_vectors(frm_vectors))
    btn_save_vectors.grid(row=0, column=1, padx=5, pady=5)
    frm_generate_vectors.pack()

    lbl_spacemaker = ctk.CTkFrame(master=app, height=20, fg_color="#ADD8E6")
    lbl_spacemaker.pack()

    frm_load_from_file = ctk.CTkFrame(master=app, fg_color="#ADD8E6")
    btn_load_from_file = ctk.CTkButton(master=frm_load_from_file, text="Load from file", command=load_from_file)
    btn_load_from_file.grid(row=0, column=0, padx=5, pady=5)
    frm_load_from_file.pack()

    lbl_spacemaker = ctk.CTkFrame(master=app, height=20, fg_color="#ADD8E6")
    lbl_spacemaker.pack()

    frm_calculate = ctk.CTkFrame(master=app, fg_color="#ADD8E6")
    btn_calculate = ctk.CTkButton(master=frm_calculate, text="Calculate", command=calculate)
    btn_calculate.grid(row=0, column=0, padx=5, pady=5)
    frm_calculate.pack()

    app.mainloop()
