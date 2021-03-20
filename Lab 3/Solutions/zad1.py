import sys
import os

if(len(sys.argv) < 3):
    print("Wymagane rozszerzenie oraz ścieżka")
    exit(1)

def printFilesWithExt(path, ext):
    for file in os.listdir(path):
        absPath = f"{path}{os.path.sep}{file}"
        if file.endswith(f".{ext}"):
            print(absPath)
        elif os.path.isdir(absPath):
            printFilesWithExt(absPath, ext)


printFilesWithExt(sys.argv[2], sys.argv[1])