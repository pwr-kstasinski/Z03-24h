if __name__ == "__main__":
    import sys

    listaArgumentow = []
    try:
        for argument in sys.argv[1:]:
            listaArgumentow.append(float(argument))
        listaArgumentow = sorted(listaArgumentow)
        for wartosc in listaArgumentow:
            print(wartosc, end=' ')
    except:
        print("Argumenty powinny byc liczbami")