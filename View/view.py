from .root import Root
from .mainwindow import MainWindow
from .calculations import CalculationsWindow
from .phi import PhiWindow
from .orbit import OrbitWindow
from .periodic import PeriodicWindow
from .classification import ClassificationWindow
from .signature import SignatureWindow

from typing import TypedDict

class Frames(TypedDict):
    mainwindow: MainWindow
    calculations: CalculationsWindow
    phi: PhiWindow
    orbit: OrbitWindow
    periodic: PeriodicWindow
    classification: ClassificationWindow
    signature: SignatureWindow


class View:
    def __init__(self):
        self.root = Root()
        self.frames: Frames = {}    
        
        self._add_frame(MainWindow, "mainwindow")
        self._add_frame(CalculationsWindow, "calculations")
        self._add_frame(PhiWindow, "phi")
        self._add_frame(OrbitWindow, "orbit")
        self._add_frame(PeriodicWindow, "periodic")
        self._add_frame(ClassificationWindow, "classification")
        self._add_frame(SignatureWindow, "signature")

    def _add_frame(self, Frame, name: str) -> None:
        self.frames[name] = Frame(self.root)
        self.frames[name].grid(row=0, column=0, sticky="nsew")

    def switch(self, name: str) -> None:
        frame = self.frames[name]
        frame.tkraise()

    def start_mainloop(self) -> None:
        self.root.mainloop()

