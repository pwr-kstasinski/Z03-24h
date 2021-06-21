import os

extension = input("Podaj rozszerzenie: ")
path = input("Podaj sciezke: ")
dirs = os.listdir(path)

for file in dirs:
    if file.endswith("." + extension):
        print(file)

