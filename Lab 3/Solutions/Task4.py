import os
import random
def startGame(amountOfRounds):

    counterWins = 0
    counterLoses = 0
    counterDraws = 0

    while(amountOfRounds > 0):
        choiceOfUser = int(input("Choose your weapon: 1 - paper, 2 - rock, 3 - scissors ---> "))
        choiceOfComputer = random.randint(1, 3)

        if choiceOfUser == 1:     # user : paper
            if choiceOfComputer == 3:     # computer : scissors
                print("COMPUTER WINS")
                counterLoses = counterLoses + 1 
            elif choiceOfComputer == 1:     # computer : paper
                print("DRAW")
                counterDraws = counterDraws + 1
            else:
                print("USER WINS")
                counterWins = counterWins + 1
        if choiceOfUser == 2:     # user : rock
            if choiceOfComputer == 2:     # computer : rock 
                print("DRAW")
                counterDraws = counterDraws + 1 
            elif choiceOfComputer == 3:     # computer : scissors
                print("USER WINS")
                counterWins = counterWins + 1
            else:
                print("COMPUTER WINS")
                counterLoses = counterLoses + 1
        if choiceOfUser == 3:     # user : scissors
            if choiceOfComputer == 3:     # computer : scissors
                print("DRAW")
                counterDraws = counterDraws + 1 
            elif choiceOfComputer == 1:     # computer : paper
                print("USER WINS")
                counterWins = counterWins + 1
            else:
                print("COMPUTER WINS")
                counterLoses = counterLoses + 1

        amountOfRounds = amountOfRounds - 1


    if counterWins == counterLoses:
        print("DRAW")
    elif counterLoses > counterWins:
        print("COMPUTER HAS WON")
    else:
        print("USER HAS WON")


    print ("AMOUNT OF USER WINS: " , counterWins)
    print ("AMOUNT OF COMPUTER WINS: " , counterLoses)
    print ("AMOUNT OF DRAWS: " , counterDraws)

inputRounds = int(input("Write number of rounds you want to play: ---> "))
startGame(inputRounds)