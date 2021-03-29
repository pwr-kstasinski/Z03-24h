import os

def showFiles(path, depth):
    dirs = os.listdir(path)

    for file in dirs:
        try:
            showLines(depth, file)
            if not os.path.isfile(path + "\\" + file):
                showFiles(path + "\\" + file, depth+4)
        except PermissionError:
            print("Nie masz dostepu")

def showLines(depth, file):
    c = " " * depth
    print(c + file)

def main():
    path = input("Podaj sciezke: ")
    showFiles(path, 0)

main()
