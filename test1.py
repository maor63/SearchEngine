import os

os.chdir('corpus')


for folder in os.listdir(os.curdir):
    os.chdir(folder)
    # print(os.listdir(os.curdir))
    for file in os.listdir(os.curdir):
        # open file
        fob = open(file, 'r')
        for line in file:
            if line == '<DOC>':
                continue
        # close file
        fob.close()
        os.chdir("..")
