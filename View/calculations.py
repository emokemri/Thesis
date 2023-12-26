import customtkinter as ctk

class CalculationsWindow(ctk.CTkFrame):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.configure(fg_color="#ADD8E6")

        self.frm_calculate = ctk.CTkFrame(self, fg_color="#ADD8E6")
        self.btn_calculate = ctk.CTkButton(master=self, text="Calculate determinant")

        self.btn_phi = ctk.CTkButton(self, text="Phi Function")
        self.btn_phi.pack()

        self.btn_orbit = ctk.CTkButton(self, text="Orbit")
        self.btn_orbit.pack()

        self.btn_coverbox = ctk.CTkButton(self, text="Coverbox for 2D")
        self.btn_coverbox.pack()

        self.btn_periodicpoints = ctk.CTkButton(self, text="Periodic Points")
        self.btn_periodicpoints.pack()

        self.btn_isgns = ctk.CTkButton(self, text="IsGNS")

        self.btn_classify = ctk.CTkButton(self, text="Classification")
        self.btn_classify.pack()

        self.btn_signature = ctk.CTkButton(self, text="Signature")
        self.btn_signature.pack()

        self.lbl_spacemaker = ctk.CTkFrame(self, height=20, fg_color="#ADD8E6")
        self.lbl_spacemaker.pack()

        self.btn_back = ctk.CTkButton(self, text="Back to Main Window")
        self.btn_back.pack()