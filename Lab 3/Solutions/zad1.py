if __name__ == "__main__":
    import sys
    import os

    # sys.argv[0] = sciezka pliku skryptu
    if len(sys.argv) != 3:
        print("Podaj dwa argumenty: rozszerzenie pliku oraz sciezke")
    else:
    # sys.argv[1], sys.argv[2] = pierwszy, drugi argument przekazany do skryptu z konsoli
        for plik in os.listdir(sys.argv[2]):
            if plik.endswith(sys.argv[1]):
                print(plik)
