from Model.model import Model
from View.view import View

from .maincontroller import MainController
from .calculationscontroller import CalculationsController
from .phicontroller import PhiController
from .orbitcontroller import OrbitController
from .periodiccontroller import PeriodicController
from .classificationcontroller import ClassificationController
from .signaturecontroller import SignatureController


class Controller:
    def __init__(self, model: Model, view: View) -> None:
        ''' Initializes model and view and sets the controllers '''
        self.view = view
        self.model = model
        self.main_controller = MainController(model, view)
        self.calculations_controller = CalculationsController(model, view)
        self.phi_controller = PhiController(model, view)
        self.orbit_controller = OrbitController(model, view)
        self.periodic_controller = PeriodicController(model, view)
        self.classification_controller = ClassificationController(model, view)
        self.signature_controller = SignatureController(model, view)

        self.model.radix.add_event_listener("dim_changed", self.dim_state_listener)


    def dim_state_listener(self, dim) -> None:
        ''' Updates views based on the dimension '''
        if dim != 0:
            self.phi_controller.update_view()
            self.orbit_controller.update_view()


    def start(self) -> None:
        ''' Starting the GUI '''
        self.view.switch("mainwindow")
        self.view.start_mainloop()
