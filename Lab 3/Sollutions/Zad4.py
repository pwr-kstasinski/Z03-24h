import random

# stałe kolory
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'

# zmienne globalne
rounds = 0
playerWins = 0
pcWins = 0

# mapa stanów wygrywających
winingStates = {
    "p": "k",
    "k": "n",
    "n": "p"
}

# pełne nazwy do wyświetlenia
etykiety = {
    "p": "papier",
    "k": "kamień",
    "n": "norzyce"
}

# róchy w zapisie skrótowym
moves = ["p", "k", "n"]

print("=================PAPIER,KAMIEN,NORZYCE=================")

# Pytanie o liczbę rund
while True:
    try:
        rounds = int(input("Wprowadz liczbę rund:"))
        if not rounds > 0:
            raise ValueError("rounds must be positive")
        break
    except:
        print("Oczekiwano liczby większej od 0")


print("""Instrukcja:
Aby wykonać róch wprowadź jeden z poniższych symboli:
    > k - kamień
    > n - norzyce
    > p - papier
""")

# procedura odpalana na jedną rundę gry
# zwraca nazwię zwycięscy rundy lub "" w przypadku remisu


def doGameRound():
    global playerWins
    global pcWins

    while True:
        plMove = input("    Podaj róch [k,p,n]: ")
        if plMove in moves:
            break
        else:
            print("    Wybierz jedną z opcji [k,p,n]!")

    pcMove = random.choice(moves)
    print(f"    PC wybrał {etykiety[pcMove]}")

    if winingStates[plMove] == pcMove:
        playerWins += 1
        return "Player"

    if winingStates[pcMove] == plMove:
        pcWins += 1
        return "PC"


# główna pentla gry
for round in range(rounds):
    print(f"Runda {round}:")
    winner = doGameRound()
    if winner:
        color = GREEN if winner == "Player" else RED
        print(f"{color}    rundę wygrał {winner}{ENDC}")
    else:
        print("    remis")

# wyświetl wyniki gry
if pcWins == playerWins:
    print(f"{YELLOW}Gra zakończona remisem{ENDC}")
elif pcWins > playerWins:
    print(f"{RED}Pc wygrywa grę{ENDC}")
elif playerWins > pcWins:
    print(f"{GREEN}Player wygrywa grę{ENDC}")

print(f"Wynik: [Player:PC] = [{playerWins}:{pcWins}]")
