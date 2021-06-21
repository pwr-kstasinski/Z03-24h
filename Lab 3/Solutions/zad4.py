if __name__ == "__main__":
    import random

    def pokazMenu():
        print("\n1: papier")
        print("2: nozyce")
        print("3: kamien")
        print("Wybierz 1-3: ", end="")
    try:
        print("Papier-kamien-nozyce")
        slownik = {1:"papier", 2:"nozyce", 3:"kamien"}
        rundyKomputera = rundyGracza = remisy = 0
        ileRund = int(input("Ile rund?: "))

        for i in range(ileRund):
            pokazMenu()
            wyborGracza = int(input())
            wyborKomputera = random.randrange(1, 4, 1) # randrange(start, stop, step)
            print("Komputer wylosowal: ", slownik[wyborKomputera])
            if wyborGracza == wyborKomputera:
                remisy += 1
            elif  ((wyborGracza == 1 and wyborKomputera == 2) or    # papier-nozyce
                (wyborGracza == 2 and wyborKomputera == 3) or    # nozyce-kamien
                (wyborGracza == 3 and wyborKomputera == 1)):     # kamien-papier
                rundyKomputera += 1
            else:
                rundyGracza += 1

        if rundyGracza > rundyKomputera:
            print("\nWYGRAL GRACZ")
        elif rundyGracza < rundyKomputera:
            print("\nWYGRAL KOMPUTER")
        else:
            print("\nREMIS")
        print("Wygrane gracza: ", rundyGracza)
        print("Wygrane komputera: ", rundyKomputera)
        print("Remisy: ", remisy)
    except:
        print("Blad, niepoprawny argument")
    