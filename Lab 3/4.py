import random

statistics = [0, 0, 0]

def game(rounds):
    while(rounds > 0):
        usersChoice = int(input("Wybierz jedna opcje wpisujac numer: (1 - papier, 2 - nozyce, 3 - kamien): "))
        computersChoice = random.randint(1, 3)
        if usersChoice == 1:
            if computersChoice == 2:
                statistics[2] += 1
            elif computersChoice == 3:
                statistics[0] += 1
        elif usersChoice == 2:
            if computersChoice == 1:
                statistics[0] += 1
            elif computersChoice == 3:
                statistics[2] += 1
        elif usersChoice == 3:
            if computersChoice ==1:
                statistics[2] += 1
            elif computersChoice == 2:
                statistics[0] += 1
        if usersChoice == computersChoice:
            statistics[1] += 1
        rounds -= 1
    if(statistics[0] > statistics[2]):
        print("Wygrales ", end='')
    elif(statistics[0] < statistics[2]):
        print("Przegrales ", end='')
    else:
        print("Zremisowales ", end='')
    print("te rozgrywke")
    print("Twoj wynik: ", statistics[0], "zwyciestw", statistics[1], "remisow", statistics[2], "porazek")
        
       
rounds = int(input("Podaj liczbe rund: "))
game(rounds)

