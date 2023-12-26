import customtkinter as ctk

class MainWindow(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configure(fg_color="#ADD8E6")

        self.frm_form = ctk.CTkFrame(self, fg_color="#ADD8E6")
        self.fg_color="#ADD8E6"

        self.lbl_dimension = ctk.CTkLabel(self.frm_form, text="System's dimension:")
        self.ent_dimension = ctk.CTkEntry(self.frm_form, width=50)
        self.btn_generate = ctk.CTkButton(self.frm_form, text="Generate")

        for i in range(3):
            self.columnconfigure(i, weight=1)

        # Use the grid geometry manager to place the Label and Entry widgets
        self.lbl_dimension.grid(row=0, column=0, padx=5, pady=5)
        self.ent_dimension.grid(row=0, column=1, padx=5, pady=5)
        self.btn_generate.grid(row=0, column=2, padx=5, pady=5)
        self.frm_form.pack()

        self.frm_base = ctk.CTkFrame(self, fg_color="#ADD8E6", height=5)
        self.lbl_base = ctk.CTkLabel(self.frm_base, text="System base:")
        self.frm_base.pack()

        self.frm_matrix = ctk.CTkFrame(self, fg_color="#ADD8E6", height=20)
        self.frm_matrix.pack()

        self.frm_save_matrix = ctk.CTkFrame(self, fg_color="#ADD8E6")
        self.btn_save_matrix = ctk.CTkButton(master=self.frm_save_matrix, text="Save matrix")
        self.frm_save_matrix.pack()
        self.btn_save_matrix.pack()

        self.lbl_spacemaker = ctk.CTkFrame(self, height=30, fg_color="#ADD8E6")
        self.lbl_spacemaker.pack()

        # Define options for the combobox
        options = ["Canonical", "J-canonical", "Symmetrical", "J-symmetrical", "Custom"]

        button_color = self.btn_generate.cget("fg_color")

        self.frm_combo = ctk.CTkFrame(self, fg_color="#ADD8E6")
        # Create a combobox and configure it with the available options
        self.combo_box = ctk.CTkComboBox(master=self.frm_combo, values=options, button_color=button_color, dropdown_fg_color="white")
        # Set a default value for the combobox
        self.combo_box.set("Select digit set")
        self.combo_box.pack()
        self.frm_combo.pack()

        self.frm_optional = ctk.CTkFrame(master=self, fg_color="#ADD8E6", height=5, bg_color="#ADD8E6")
        self.lbl_number_of_digits = ctk.CTkLabel(master=self.frm_optional)
        self.ent_number_of_digits = ctk.CTkEntry(master=self.frm_optional, width=50)
        self.btn_generate_digits = ctk.CTkButton(master=self.frm_optional, text="Generate")
        self.frm_optional.pack()

        self.frm_digits = ctk.CTkFrame(master=self, fg_color="#ADD8E6", height=10, bg_color="#ADD8E6")
        self.frm_digits.pack()

        self.frm_save_digits = ctk.CTkFrame(self, fg_color="#ADD8E6", height=5)
        self.btn_save_digits = ctk.CTkButton(master=self.frm_save_digits, text="Save digits")
        self.frm_save_digits.pack()

        self.lbl_spacemaker = ctk.CTkFrame(self, height=20, fg_color="#ADD8E6")
        self.lbl_spacemaker.pack()

        self.frm_load_from_file = ctk.CTkFrame(self, fg_color="#ADD8E6")
        self.btn_load_from_file = ctk.CTkButton(master=self.frm_load_from_file, text="Load from file")
        self.btn_load_from_file.pack()
        self.frm_load_from_file.pack()

        self.lbl_spacemaker = ctk.CTkFrame(self, height=20, fg_color="#ADD8E6")
        self.lbl_spacemaker.pack()

        # Create a button to open the new window
        self.frm_open_new_window = ctk.CTkFrame(self, fg_color="#ADD8E6")
        self.btn_open_new_window = ctk.CTkButton(self.frm_open_new_window, text="Calculate")
        self.btn_open_new_window.pack()
        self.frm_open_new_window.pack()
