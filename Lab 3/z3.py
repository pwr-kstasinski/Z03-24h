def sortList(list):
    return list.sort()

def showList(list):
    print("Lista: ")

    for elem in list:
        print(elem)

def main():
    list = []
    n = int(input("Podaj liczbe elementow listy: "))

    for i in range(n):
        elem = int(input("Podaj " + str(i+1) + " element: "))
        list.append(elem)
    
    showList(list)
    sortList(list)
    showList(list)

main()

