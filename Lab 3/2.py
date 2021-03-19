import os

def printTree(path, stage):
    for element in os.listdir(path):
        tmpPath = os.path.join(path, element)
        for i in range(stage):
            if i == stage-1:
                print("|----", end="")
            else:
                print("|    ", end="")

        print(os.path.splitext(element)[0])
        if os.path.isdir(tmpPath):
            printTree(tmpPath, stage+1)

path = input("Podaj sciezke: ")
print(path)
printTree(path, 1)