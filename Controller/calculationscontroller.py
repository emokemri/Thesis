from Model.model import Model
from View.view import View

import matplotlib.pyplot as plt

class CalculationsController:
    def __init__(self, model: Model, view: View) -> None:
        ''' Initializes model and view and sets the frame to "calculations" '''
        self.model = model
        self.view = view
        self.frame = self.view.frames["calculations"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.btn_back.configure(command=self.show_main_window)
        self.frame.btn_phi.configure(command=self.phi)
        self.frame.btn_orbit.configure(command=self.orbit)
        self.frame.btn_coverbox.configure(command=self.coverbox)
        self.frame.btn_periodicpoints.configure(command=self.periodic_points)
        self.frame.btn_classify.configure(command=self.classify)
        self.frame.btn_signature.configure(command=self.signature)


    def show_main_window(self) -> None:
        ''' Switch to MainWindow '''
        button_color = self.frame.btn_back.cget("fg_color")
        self.frame.btn_isgns.configure(fg_color=button_color)
        self.view.switch("mainwindow")

    def phi(self):
        ''' Trigger dimension changed and switch to Phi window '''
        self.model.radix.trigger_event("dim_changed")
        self.view.switch("phi")

    def orbit(self):
        ''' Trigger dimension changed and switch to Orbit window '''
        self.model.radix.trigger_event("dim_changed")
        self.view.switch("orbit")

    def coverbox(self):
        ''' Create plot for coverbox '''
        if self.model.radix.dimension != 2:
            return

        li = self.model.radix.li
        ui = self.model.radix.ui

        # Create a figure and axis
        fg, ax = plt.subplots()

        # Create a rectangle using the coordinates
        rectangle = plt.Rectangle(ui, li[0] - ui[0], li[1] - ui[1], fill=False, color="blue", label="coverbox")

        # Add the rectangle to the plot
        ax.add_patch(rectangle)

        self.model.radix.H_x = []
        self.model.radix.H_y = []

        # Define the maximum depth
        max_depth = 1
        while(pow(len(self.model.radix.digits), max_depth) < 25000):
            max_depth += 1

        self.model.radix.set_H(0, max_depth)

        plt.scatter(self.model.radix.H_x, self.model.radix.H_y, c ="red", label="set -H", s=0.2)

        plt.legend()

        # Show the plot
        plt.show()

        return


    def periodic_points(self):
        ''' Switch to PeriodicPointsWindow '''
        self.model.radix.find_periodic_points()
        self.view.switch("periodic")

    
    def classify(self):
        ''' Switch to ClassificationWindow '''
        self.model.radix.classify()
        self.view.switch("classification")


    def signature(self):
        ''' Switch to SignatureWindow '''
        self.model.radix.find_signature()
        self.view.switch("signature")