import os
from os.path import isdir


def tree(path, spacer):
    for item in os.listdir(path):
        print(spacer + item)
        if isdir(f'{path}/{item}'):
            tree(f'{path}/{item}', spacer + '\t')


tree('.', '')