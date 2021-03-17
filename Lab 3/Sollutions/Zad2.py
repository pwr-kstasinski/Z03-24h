import os
import sys

# unicode blocks: https://en.wikipedia.org/wiki/Box_Drawing_(Unicode_block)
line = chr(0x2501) + chr(0x2501) + chr(0x2501) + chr(0x2501)
space = "     "
innerSymbol = chr(0x2523)
lastSymbol = chr(0x2517)

root = sys.argv[1] if len(sys.argv) == 2 else "./"


def listFoldersRec(rootDir, printPrefix=""):
    if not os.path.isdir(rootDir):
        return

    # liczba elementów w katalogu
    # potrzebna do określienia ostatniego elementu
    leftToPrintCount = len(os.listdir(rootDir))

    # listowanie plików
    for file in os.listdir(rootDir):
        if not os.path.isdir(os.path.join(rootDir, file)):
            leftToPrintCount -= 1
            # ┣━ albo ┗ jeśli ostatni
            symbol = lastSymbol if leftToPrintCount == 0 else innerSymbol
            print(f"{printPrefix}{symbol}{line}{file}")

    # listowanie katalogów
    for file in os.listdir(rootDir):
        if os.path.isdir(os.path.join(rootDir, file)):
            leftToPrintCount -= 1
            # ┣━ albo ┗ jeśli ostatni
            if leftToPrintCount == 0:
                symbol = lastSymbol
                prefix = printPrefix+" "+space
            else:
                symbol = innerSymbol
                prefix = printPrefix+chr(0x2503)+space

            print(f"{printPrefix}{symbol}{line}{file}")
            listFoldersRec(os.path.join(rootDir, file), prefix)


print(root)
listFoldersRec(root)
