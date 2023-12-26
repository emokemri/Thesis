from Model.model import Model
from View.view import View
from Controller.controller import Controller


def main():
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.start()


if __name__ == "__main__":
    main()
