
from random import randrange
import numpy as np

def printAvailableMoves():
    print("Dostepne ruchy:")
    print("0 - kamien")
    print("1 - papier")
    print("2 - nozyce")
    return

def readPlayerMove():
    playerMove = -1
    playerMove = int(input(""))
    while playerMove < 0 or playerMove > 2 :
        print("Nieprawidlowy ruch")
        playerMove = int(input("Podaj poprawny ruch: "))
    return playerMove

def showComputerMove(x):
    if x == 0:
        print("Komputer gra kamien")
    elif x == 1:
        print("Komputer gra papier")
    else:
        print("Komputer gra nozyce")
    return 

def interpretResult(playerMove, computerMove):
    if playerMove == computerMove:
        return 0 # - draw
    if playerMove >= (computerMove % 2):
        return 1 # - player wins
    return 2 # - computer wins

def showRoundResult(x):
    if x == 0:
        print("Remis")
    elif x == 1:
        print("Gracz wygrywa runde")
    else:
        print("Komputer wygrywa runde")
    return    

numberOfRounds = int(input("Podaj liczbe rund: "))
winsComputer = 0
winsPlayer = 0
draws = 0

while numberOfRounds < 1:
    print("Nieprawidlowa liczba rund")
    numberOfRounds = int(input("Podaj poprawna liczbe rund: "))

print("Wczytana liczba rund {}".format(numberOfRounds))

currentRound = 1
while currentRound <= numberOfRounds:
    print("Runda {}".format(currentRound))
    print("\nPodaj swoj ruch")
    printAvailableMoves()

    playerMove = readPlayerMove()

    computerMove = randrange(3)
    showComputerMove(computerMove)

    roundResult = interpretResult(playerMove,computerMove)
    showRoundResult(roundResult)

    if roundResult == 0:
        draws +=1
    elif roundResult == 1:
        winsPlayer+=1
    else:
        winsComputer+=1

    if winsPlayer > numberOfRounds/2 or winsComputer > numberOfRounds/2:
        break

    currentRound+=1

if winsComputer == winsPlayer:
    print("\nRemis gry")
elif winsComputer > winsPlayer:
    print("\nKomputer wygrywa gre")
else:
    print("\nGracz wygrywa gre")

print("Statystyki gry:")
print("Remisy {}".format(draws))
print("Wygrane rundy gracza {}".format(winsPlayer))
print("Wygrane rundy komputera {}".format(winsComputer))
