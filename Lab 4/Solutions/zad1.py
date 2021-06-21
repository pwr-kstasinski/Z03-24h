# bez drzewa/slownika
if __name__ == '__main__':
    wyrazenie = input("Podaj wyrazenie do obliczenia:\n")

    # zabezpiecznie eval przed liczeniem 'untrusted input', ktore byloby pominiete w try except
    # np przed wpisaniem __import__('os').system('clear')
    poprawne_znaki = (' ', '+', '-', '/', '*', '.', '(', ')', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    def czyPoprawne(ciag_znakow):
        for znak in ciag_znakow:
            if not znak in poprawne_znaki:
                return False
        return True

    if czyPoprawne(wyrazenie):
        try:
            print(wyrazenie, "=", eval(wyrazenie))
        except:                 # jezeli zawiera tylko dozwolone znaki ale samo wyrazenie jest niepoprawne np '2 * (3 + '
            print("Blad, wyrazenie niepoprawne gramatycznie.")
    else:
        print("Blad, wyrazenie niepoprawne. Wyrazenie moze zawierac znaki:")
        print('spacja', end=" ")     # chyba lepiej niz ' '
        # for'em ladniej wyswietla
        for znak in poprawne_znaki[1:]:
            print(znak, end=" ")
