import sys
import os

elemTab = "├───"
lastElemTab = "└───"
dirTab = "│   "
clearTab = "    "

startPath = os.path.abspath("")

if(len(sys.argv) > 1):
   startPath = sys.argv[1]

def printTree(path, curTab):
    list = os.listdir(path)
    list.reverse()
    for _ in range(1, len(list)):
        curElem = list.pop()
        print(f"{curTab}{elemTab}{curElem}")
        absPath = f"{path}{os.path.sep}{curElem}"
        if os.path.isdir(absPath):
            printTree(absPath, f"{curTab}{dirTab}")
    if len(list) > 0:
        print(f"{curTab}{lastElemTab}{list[0]}")
        if os.path.isdir(f"{path}{os.path.sep}{list[0]}"):
            printTree(f"{path}{os.path.sep}{list[0]}", f"{curTab}{clearTab}")


print(f"{startPath[:2]}.")
printTree(startPath, "")
