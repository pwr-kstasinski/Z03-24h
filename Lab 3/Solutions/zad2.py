import sys
import os

# ASCII 179 = │
# ASCII 192 = └
# ASCII 195 = ├
# ASCII 196 = ─

def pokaListe(lista):                               # konwersja listy na string
    napis = ''
    for l in lista:
        napis += l
    return napis

def wyswietlDrzewo(sciezka, wyswietl):
    podfolderLicznik = 0
    for obiekt in os.listdir(sciezka):
        if obiekt == os.listdir(sciezka)[-1]:       # ostatni obiekt w liscie
            wyswietl.append('└────')
        else:
            wyswietl.append('├────')
        print(pokaListe(wyswietl) + obiekt)
        wyswietl.pop()  
        if os.path.isdir(os.path.join(sciezka, obiekt)):    # os.path.join() tworzy sciezke zaleznie od systemu (dodaje \ albo /)
            if podfolderLicznik == 0:
                wyswietl.append('│    ')
            else:
                wyswietl.append('     ')
            podfolderLicznik += 1
            wyswietlDrzewo(os.path.join(sciezka, obiekt), wyswietl)
            wyswietl.pop()
            podfolderLicznik -= 1

if __name__ == "__main__":            
    # sys.argv[0] = sciezka pliku skryptu
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        print('Podaj sciezke')
    else:
        print(os.path.abspath(sys.argv[1])[:2] + ".")
        wyswietlDrzewo(os.path.abspath(sys.argv[1]), [])
