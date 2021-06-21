import os

extension = input('extension:')
path = input('path:')

for file in os.listdir(path):
    if file.endswith('txt'):
        print(file)