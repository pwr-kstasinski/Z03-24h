import sys
import os


def displayTree(path, spacing):
    for f in os.listdir(path):
        print(spacing+f)
        if os.path.isdir(f'{path}/{f}'):
            displayTree(f'{path}/{f}',"|"+"\t"+spacing)

print("Type path: ")
displayTree(sys.argv[1],"|___")