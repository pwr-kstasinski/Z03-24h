import sys
import os
import random

def choose():
    print("Choose from below:")
    print("1: Paper")
    print("2: Rock")
    print("3: Scissors")
    print("4: Stop")
    choice = int(input())
    if (choice == 1 or choice == 2 or choice == 3):
        return choice
    else:
        print()
        return 1

def score():
    print("Your points: ", human_wins)
    print("Computers points: ", computer_wins)
    if (human_wins == computer_wins):
        print("TIE")
    elif (human_wins > computer_wins):
        print("You win")
    else:
        print("You lose")


table = {1: 'Paper', 2:'Rock', 3: "Scissors"}
computer_wins = 0
human_wins = 0
print("How many rounds would you like to play?")
number_of_rounds = int(input())
if (number_of_rounds < 1):
     print("You must provide number bigger than 0!")
     exit(-1)
for i in range(number_of_rounds):
     computer_choice = random.randint(1,3)
     human_choice = choose()
     print("You have chosen: " + table[human_choice])
     print("Computer has chosen: " + table[computer_choice])
     if (human_choice == computer_choice):
         print("TIE")
     elif ((computer_choice == 1 and human_choice == 3) or (computer_choice == 2 and human_choice == 1) or (computer_choice == 3 and human_choice == 2)):
        human_wins += 1
        print("You win")
     else:
        computer_wins += 1
        print("You lose")
score()
