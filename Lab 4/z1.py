# bez drzewa/slownika:

equation = input("Podaj rownanie: ")

try:
    score = eval(equation)
    print(equation + " = " + str(score))
except SyntaxError: 
    print("Blad skladniowy np. przy 9-")
except TypeError:
    print("Blad typu np. przy 3(2-4)")
except NameError:  
    print("Nie nalezy uzywac liter oraz nieodpowiednich symbolow")



