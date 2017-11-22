from Controller import Controller
from View import View


def Main():
    c = Controller()
    v = View(c)
    v.start()


if __name__ == '__main__':
    Main()
