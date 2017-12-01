import time

from Controller import Controller
from ReadFile import ReadFile
from View import View


def Main():
    # c = Controller()
    # v = View(c)
    # v.start()
    start = time.time()
    read_file = ReadFile()
    read_file.read_files("./LA/")
    end = time.time()
    print("Read file time: {0}".format(str(end - start)))


if __name__ == '__main__':
    Main()
