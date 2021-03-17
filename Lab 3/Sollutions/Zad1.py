import os
import sys

arg_count = len(sys.argv)
nothingFound = True

if arg_count <= 1 or arg_count > 3:
    print("""Niepoprawna ilość argumentów. Przykładowa składnia
    >>py Zad1.py <extension> <path>(optional)""")
    exit(-1)


ext = sys.argv[1]

if len(sys.argv) > 2:
    path = sys.argv[2]
else:
    path = "./"

if not os.path.isdir(path):
    print("Podana lokalizacja nie istnieje")
    exit(-1)

for file in os.listdir(path):
    if file.endswith(ext) and os.path.isfile(os.path.join(path, file)):
        nothingFound = False
        print(file)

if nothingFound:
    print("Nic nie znaleziono")
