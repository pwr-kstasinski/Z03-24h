import os
import sys
from graphviz import Digraph
import math
from tkinter import *

expression = ""
def enter(symbol):
	global expression
	float_symbol = str(symbol)
	if expression != "":
		expression = expression + " "
	expression += float_symbol
	equation.set(expression)

def clear():
	global expression
	expression = ""
	equation.set(expression)

class Tree:
    def __init__(self, value, left = None, right = None):
        self.value = value
        self.left = left
        self.right = right

def make_tree(exp):
    if (len(exp) == 1 or len(exp) == 2):
        return Tree(exp)
    leftE, rightE = exp.split(" ", 1)
    if (leftE == '('):
        inside, rightE = bracketSplit(rightE)
        leftN = make_tree(inside)
    elif (leftE == "sqrt" or leftE == "log"):
        inside, rightE = bracketSplit(rightE[2:])
        print(inside)
        temp = make_tree(inside)
        leftN = Tree(leftE,temp)
    else:
        leftN = Tree(leftE)
    
    if (rightE == ""):
        return leftN

    rightE, exp = rightE.split(" ", 1)
    root = Tree(rightE, leftN)
    
    if (len(exp) == 1 or len(exp) == 2):
        leftE = exp
    else:
        leftE, rightE = exp.split(" ", 1)
    if (leftE == '('):
        inside, rightE = bracketSplit(rightE)
        rightN = make_tree(inside)
    else:
        rightN = Tree(leftE)
        if (exp != leftE):
            exp = rightE
    root.right = rightN

    while (exp != exp.split(" ", 1)[0]):
        leftE, exp = exp.split(" ", 1)
        left, rightE = exp.split(" ", 1)
        if (exp.split(" ", 1)[0] == '('):
            inside, exp = bracketSplit(exp[2:])
            rightN = make_tree(inside[1:])
        elif (left == "sqrt" or left == "log"):
            inside, rightE = bracketSplit(rightE[2:])
            temp = make_tree(inside)
            rightN = Tree(left, temp)
            exp = rightE
        else:
            rightN = Tree(exp.split(" ", 1)[0])
            if(exp.split(" ", 1)[0] != exp):
                exp = exp.split(" ", 1)[1]
        print(leftE)
        if (leftE == '+' or leftE == "-"):
            root = Tree(leftE, root, rightN)
        else:
            root.right = Tree(leftE, root.right, rightN)

    return root

def bracketSplit(inside):
	evaluation = ''
	leftE, inside = inside.split(" ", 1)
	counter = 1
	while(counter > 0):
	
		if(leftE == '('):
			counter += 1
			evaluation += ' ('
		elif(leftE == ')'):
			counter -= 1
			if(counter > 0):
				evaluation += (' )') 
			else:
				break
		else:
			evaluation += (' ' + leftE)
		if (len(inside) == 1):
			leftE = inside
			inside = ""
		else:
			leftE, inside = inside.split(" ", 1)
	return evaluation.split(' ', 1)[1], inside

def eval(tree):
	if(tree.right == None and tree.left == None):
		return float(tree.value)
	else:
		if(tree.value == '+'):
			return eval(tree.left) + eval(tree.right)
		elif(tree.value == '-'):
			return eval(tree.left) - eval(tree.right)
		elif(tree.value == '*'):
			return eval(tree.left) * eval(tree.right)
		elif(tree.value == '/'):
			return eval(tree.left) / eval(tree.right)
		elif(tree.value == "mod"):
			return eval(tree.left) % eval(tree.right)
		elif(tree.value == '^'):
			return eval(tree.left) ** eval(tree.right)
		elif(tree.value == 'log'):
			return math.log(eval(tree.left),10)
		elif(tree.value == 'sqrt'):
			return math.sqrt(eval(tree.left))            
counter = 0
def labelTree(dot, tree):
    global counter
    counter += 1
    label = counter
    dot.node(str(label), tree.value)
    if (tree.left != None and tree.right != None):
        leftLabel = labelTree(dot, tree.left)
        rightLabel = labelTree(dot, tree.right)
        dot.edge(str(label), str(leftLabel))
        dot.edge(str(label), str(rightLabel))
    elif (tree.left != None):
        leftLabel = labelTree(dot, tree.left)
        dot.edge(str(label), str(leftLabel))
    elif (tree.right != None):
        rightLabel = labelTree(dot, tree.right)
        dot.edge(str(label), str(rightLabel))
    return label

def drawTree(tree):
    dot = Digraph(format = 'png')
    labelTree(dot, tree)
    dot.render('tree.gv', view = True)

def showEval():
    global expression
    expression = expressionField.get()
    tree = make_tree(expression)
    expression = str(eval(tree))
    drawTree(tree)
    equation.set(expression)

numberButtons = []
symbolButtons = []


window = Tk()
window.title("Calculator")
window.geometry("280x350")

equation = StringVar()
clearButton = Button(window, padx=14, pady= 14, text = "Clear",command = lambda: clear())
equationButton = Button(window, padx=14, pady=14, text = "=", command = lambda: showEval())
dotButton = Button(window, padx = 14, pady = 14, text = ".", command = lambda: enter("."))
leftBracketButton = Button(window, padx=14, pady=14, text = '(', command = lambda: enter("("))
rightBracketButton = Button(window, padx=14, pady=14, text = ')', command = lambda: enter(")"))

expressionField = Entry(window, textvariable = equation, width = 25)
expressionField.grid(columnspan = 4)

numberButtons.append(Button(window, padx=14, pady=14, text = 0,command = lambda: enter(0)))
numberButtons.append(Button(window, padx=14, pady=14, text = 1,command = lambda: enter(1)))
numberButtons.append(Button(window, padx=14, pady=14, text = 2,command = lambda: enter(2)))
numberButtons.append(Button(window, padx=14, pady=14, text = 3,command = lambda: enter(3)))
numberButtons.append(Button(window, padx=14, pady=14, text = 4,command = lambda: enter(4)))
numberButtons.append(Button(window, padx=14, pady=14, text = 5,command = lambda: enter(5)))
numberButtons.append(Button(window, padx=14, pady=14, text = 6,command = lambda: enter(6)))
numberButtons.append(Button(window, padx=14, pady=14, text = 7,command = lambda: enter(7)))
numberButtons.append(Button(window, padx=14, pady=14, text = 8,command = lambda: enter(8)))
numberButtons.append(Button(window, padx=14, pady=14, text = 9,command = lambda: enter(9)))

symbolButtons.append(Button(window, padx=14, pady=14, text = "+", command = lambda: enter("+")))
symbolButtons.append(Button(window, padx=14, pady=14, text = "-", command = lambda: enter("-")))
symbolButtons.append(Button(window, padx=14, pady=14, text = "*", command = lambda: enter("*")))
symbolButtons.append(Button(window, padx=14, pady=14, text = "/", command = lambda: enter("/")))
symbolButtons.append(Button(window, padx=14, pady=14, text = "^", command = lambda: enter("^")))
symbolButtons.append(Button(window, padx=14, pady=14, text = "!", command = lambda: enter("!")))
symbolButtons.append(Button(window, padx=14, pady=14, text = "sqrt(x)", command = lambda: enter("sqrt ( x )")))
symbolButtons.append(Button(window, padx=14, pady=14, text = "mod", command = lambda: enter("mod")))
symbolButtons.append(Button(window, padx=14, pady=14, text = "|x|", command = lambda: enter("| x |")))
symbolButtons.append(Button(window, padx=14, pady=14, text = "1/x", command = lambda: enter("1 / x")))
symbolButtons.append(Button(window, padx=14, pady=14, text = "log(x)", command = lambda: enter("log ( x )")))


for i in range(3):
	for j in range(3):
		numberButtons[i * 3 + j + 1].grid(row = i + 2, column = j)

numberButtons[0].grid(row = 5, column = 0)
dotButton.grid(row = 5, column = 2)
symbolButtons[3].grid(row = 5, column = 3)
equationButton.grid(row = 5, column = 1)
clearButton.grid(row = 7, column = 3)
leftBracketButton.grid(row = 2, column = 4)
rightBracketButton.grid(row = 3, column = 4)

for j in range(4):
	symbolButtons[j + 4].grid(row = 6, column = j)
for i in range(3):
	symbolButtons[i].grid(row = i + 2, column = 3)
	symbolButtons[i + 8].grid(row = 7, column = i)

# poprawne wyrazenie to takie, gdzie pomiedzy symbolami mamy spacje odstepu
# przyklad: 1 + 3 * 2 - log ( 10 + 3 )
# dzialaja wszystkie operacje poza silnią=a, odwrotnoscia i wartoscia bezwzgledna
window.mainloop()