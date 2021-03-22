import random
import os

def game(rounds):

    (wins, draws, loses) = (0, 0, 0)

    while(rounds>0):
        choice = int(input("Choose 1-rock, 2-paper, 3-scissors"))
        rand = random.randint(1, 3)

        if choice == 1:
            if rand == 1:
                print("draw")
                draws = draws + 1 
            elif rand == 2:
                print("lose")
                loses = loses + 1
            else:
                print("win")
                wins = wins + 1
        if choice == 2:
            if rand == 2:
                print("draw")
                draws = draws + 1 
            elif rand == 3:
                print("lose")
                loses = loses + 1
            else:
                print("win")
                wins = wins + 1
        if choice == 3:
            if rand == 3:
                print("draw")
                draws = draws + 1 
            elif rand == 1:
                print("lose")
                loses = loses + 1
            else:
                print("win")
                wins = wins + 1

        rounds = rounds - 1

    if (wins > loses):
        print("You've won")
    elif (wins < loses):
        print("You've lost")
    else:
        print("It's a draw")

    print (f"Wins: {wins}")
    print (f"Draws: {draws}")
    print (f"Loses: {loses}")

rounds = int(input("Write number of rounds you want to play:"))
game(rounds)
