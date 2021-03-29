import random

def showMenu():
    print("Wybierz sposrod podanych wpisujac odpowiednia cyfre: ")
    print("1. Papier")
    print("2. Kamien")
    print("3. Nozyce")

def main():
    rounds = 0
    wins = 0
    compWins = 0
    draws = 0
    chosenRounds = int(input("Podaj liczbe rund w rozgrywce: ")) 

    while rounds < chosenRounds: 

        showMenu()
        choice = int((input("Wpisz cyfre: ")))

        while choice != 1 and choice != 2 and choice!=3: 
            showMenu()
            choice = int(input("Wpisz poprawna wartosc: ")) 
        
        rounds += 1

        if choice == 1: 
            choiceName = 'Papier'
        elif choice == 2: 
            choiceName = 'Kamien'
        else: 
            choiceName = 'Nozyce'
                       
        print("\nWybrales " + choiceName)
        
        compChoice = random.randint(1, 3) 

        if compChoice == 1: 
            compChoiceName = 'Papier'
        elif compChoice == 2: 
            compChoiceName = 'Kamien'
        else: 
            compChoiceName = 'Nozyce'
            
        print("Komputer wybral " + compChoiceName) 

        if (choice == 1 and compChoice == 2) or (choice == 2 and compChoice == 1 ): 
            print("\nPapier wygrywa!") 
            result = "Papier"
            
        elif (choice == 1 and compChoice == 3) or (choice == 3 and compChoice == 1): 
            print("\nNozyce wygrywaja!") 
            result = "Nozyce"
        elif (choice == 2 and compChoice == 3) or (choice == 3 and compChoice == 2): 
            print("\nKamien wygrywa!") 
            result = "Kamien"
        else:
            result = "\nRemis"

        if result == choiceName: 
            print("Pokonales komputer w tej rundzie!\n")
            wins += 1
        elif result == compChoiceName: 
            print("Komputer wygrywa w tej rundzie!\n") 
            compWins += 1
        else:
            print("\nMamy remis w tej rundzie!\n")
            draws += 1

        if(rounds == chosenRounds):
            print("\nKoniec gry!")
        
    if wins > compWins:
        print("\nWygrales! Twoja liczba zwyciestw: " + str(wins))
        print("Komputer wygral tylko: " + str(compWins) + " razy")
        print("Liczba remisow: " + str(draws))
    elif wins == compWins:
        print("\nRemis! Wygrales: " + str(wins) + " razy, a komputer: " + str(compWins) + " razy")
        print("Do remisu w rundach doszlo: " + str(draws) + "-krotnie")
    else: 
        print("\nWygral komputer z liczba zwyciestw: " + str(compWins))
        print("Wygrales tylko: " + str(wins) + " razy")
        print("Liczba remisow: " + str(draws))

main()






