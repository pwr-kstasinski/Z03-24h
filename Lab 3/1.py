import os

path = input("Podaj sciezke: ")
extension = "." + input("Podaj rozszerzenie: ")
for element in os.listdir(path):
    if element.endswith(extension):
        print(element)

