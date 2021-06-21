import sys
import os

startpath = sys.argv[1]

def tree(path, spacing):
    for f in os.listdir(path):
        print(spacing+f)
        if os.path.isdir(f'{path}/{f}'):
            tree(f'{path}/{f}',"|"+"\t"+spacing)

tree(startpath,"|___")
    