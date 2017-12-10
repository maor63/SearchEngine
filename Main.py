import time

from Controller import Controller
from ReadFile import ReadFile
from Master import Master
from View import View
from Parser import Parser


def Main():
    c = Controller()
    v = View(c)
    v.start()

    # start = time.time()
    # m = Master()
    # m.run_process()
    #
    # end = time.time()
    # print("Read file time: {0}".format(str(end - start)))

if __name__ == '__main__':
    Main()
