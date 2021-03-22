import os
import random

rounds = int(input('Podaj liczbę rund:'))
pWins = 0
cWins = 0
draws = 0

transToNum = dict({'kamien':1, 'papier':2, 'nozyce':3})
transToWord = dict({1:'kamien', 2:'papier', 3:'nozyce'})

for i in range(1, rounds+1):
	print("Runda ", i)
	pChoice =''
	while True:
		pChoice = input('Wybierz zagranie[kamien/papier/nozyce]:')
		if(pChoice == 'kamien' or pChoice == 'papier' or pChoice == 'nozyce'):
			break
	cChoice = random.randrange(1,4)
	print("Komputer wybrał " + transToWord[cChoice])
	if(transToNum[pChoice]==cChoice):
		print ('Remis\n\n')
		draws += 1
	elif(transToNum[pChoice]>cChoice or (pChoice=='kamien' and cChoice==3)):
		print('Wygrałeś\n\n')
		pWins += 1
	else:
		print('przegrałeś\n\n')
		cWins += 1
		
print('Koncowy wynik:  Gracz -', pWins, '  Komputer -', cWins, '  Remisy -', draws ,'\n\n')		
		