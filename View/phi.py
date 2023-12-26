import customtkinter as ctk

class PhiWindow(ctk.CTkFrame):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.configure(fg_color="#ADD8E6")

        self.frm_z = ctk.CTkFrame(self, fg_color="#ADD8E6")
        self.lbl_z = ctk.CTkLabel(master=self.frm_z, text="Enter the lattice point:")
        self.frm_z.pack()
        self.lbl_z.pack()

        self.frm_entries = ctk.CTkFrame(self, fg_color="#ADD8E6")
        self.frm_entries.pack()

        self.frm_calculate = ctk.CTkFrame(self, fg_color="#ADD8E6", height=5)
        self.btn_calculate = ctk.CTkButton(self.frm_calculate, text="Calculate Phi")
        self.frm_calculate.pack()
        self.btn_calculate.pack()

        self.lbl_spacemaker = ctk.CTkFrame(self, height=20, fg_color="#ADD8E6")
        self.lbl_spacemaker.pack()

        self.frm_solution = ctk.CTkFrame(self, height=20, fg_color="#ADD8E6")
        self.frm_solution.pack()

        self.lbl_spacemaker = ctk.CTkFrame(self, height=20, fg_color="#ADD8E6")
        self.lbl_spacemaker.pack()

        self.btn_back = ctk.CTkButton(self, text="Back to Calculations")
        self.btn_back.pack()