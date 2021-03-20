import random

roundNum = int(input('Enter number of rounds: '))

if roundNum < 1:
    print('Number have to be positive')
    exit(1)

playerPoints = 0
compPoints = 0
draws = 0
choices = ['rock', 'paper', 'scissors']

for r in range(1, roundNum + 1):
    print(f'=== Round {r} ===')
    print(f'({", ".join(choices)})')
    playerChoice = input("Player choice: ")

    if playerChoice not in choices:
        print("You can't play...")
        exit(2)

    compChoice = random.choice(choices)

    print(f'Computer choice: {compChoice}')

    if playerChoice == compChoice:
        draws += 1
    elif playerChoice == 'rock':
        if compChoice == 'scissors':
            playerPoints += 1
        else:
            compPoints +=1
    elif playerChoice == 'paper':
        if compChoice == 'rock':
            playerPoints += 1
        else:
            compPoints += 1
    else:
        if compChoice == 'paper':
            playerPoints +=1
        else:
            compPoints +=1

    print(f'= After {r} round =')
    print(f'Player: {playerPoints}')
    print(f'Computer: {compPoints}\n')


print("==== THE END ====")
if playerPoints == compPoints:
    print("Nobody won and nobody lost")
elif playerPoints > compPoints:
    print("Player won!")
else:
    print("Computer won!")

print(f'Player: {playerPoints}')
print(f'Computer: {compPoints}')
print(f'Draws: {draws}')
