
import os
import sys

def printDirs(dirPath, prevTree):
    #print(os.listdir(dirPath))
    folderCount = 0
    for dirName in os.listdir(dirPath):
        if os.path.isdir(dirPath +"\\"+ dirName):
            folderCount += 1

    for dirName in os.listdir(dirPath):
        if os.path.isdir(dirPath +"\\"+ dirName):
            print(prevTree + "|---" + dirName)
            
            folderCount-=1
            if folderCount == 0:
                printDirs(dirPath +"\\"+ dirName,prevTree + "    ")
            else:
                printDirs(dirPath +"\\"+ dirName,prevTree + "|   ")
    return

if len(sys.argv)==2:
    currentDir = sys.argv[1]
else:
    currentDir = os.getcwd()+"\\."

print(currentDir+"\\.")

folderCount = 0
for dirName in os.listdir(currentDir):
    if os.path.isdir(currentDir +"\\"+ dirName):
        folderCount += 1

for dirName in os.listdir(currentDir):
    if os.path.isdir(currentDir +"\\"+ dirName):
        print("|---"+dirName)
        
        folderCount-=1
        if folderCount == 0:
            printDirs(currentDir +"\\"+ dirName,"    ")
        else:
            printDirs(currentDir +"\\"+ dirName,"|   ")
