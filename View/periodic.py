import customtkinter as ctk

class PeriodicWindow(ctk.CTkFrame):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.configure(fg_color="#ADD8E6")

        self.dimension = 0

        self.lbl_spacemaker = ctk.CTkFrame(self, height=20, fg_color="#ADD8E6")
        self.lbl_spacemaker.pack()

        self.frm_calculate = ctk.CTkFrame(self, fg_color="#ADD8E6", height=5)
        self.btn_calculate = ctk.CTkButton(self.frm_calculate, text="Calculate Periodic Points")
        self.frm_calculate.pack()
        self.btn_calculate.pack()

        self.lbl_spacemaker = ctk.CTkFrame(self, height=20, fg_color="#ADD8E6")
        self.lbl_spacemaker.pack()

        self.frm_solution = ctk.CTkFrame(self, height=20, fg_color="#ADD8E6")
        self.frm_solution.pack()

        self.lbl_spacemaker = ctk.CTkFrame(self, height=10, fg_color="#ADD8E6")
        self.lbl_spacemaker.pack()

        self.frm_file = ctk.CTkFrame(self, height=20, fg_color="#ADD8E6")
        self.btn_file = ctk.CTkButton(self.frm_file, text="Save periodic points to file")
        self.frm_file.pack()
        self.btn_file.pack()

        self.lbl_spacemaker = ctk.CTkFrame(self, height=20, fg_color="#ADD8E6")
        self.lbl_spacemaker.pack()

        self.btn_back = ctk.CTkButton(self, text="Back to Calculations")
        self.btn_back.pack()