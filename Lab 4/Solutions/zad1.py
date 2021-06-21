import os
from graphviz import Digraph
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value  # The node value (integer)
        self.left = left    # Left child
        self.right = right  # Right child		

def convToTree(str):
	#Pierwsz Node
	if(str.split(' ', 1)[0] == '('):
		(isolated, rest) = bracketSplit(str.split(' ', 1)[1])
		leftN = convToTree(isolated)
		str = rest
	else:
		leftN = Node(str.split(' ', 1)[0])
		str = str.split(' ', 1)[1]
	
	root = Node(str.split(' ', 1)[0], leftN)
	str = str.split(' ', 1)[1]
	if(str.split(' ', 1)[0] == '('):
		(isolated, rest) = bracketSplit(str.split(' ', 1)[1])
		rightN = convToTree(isolated)
		str = rest
	else:
		rightN = Node(str.split(' ', 1)[0])
		if(str.split(' ', 1)[0] != str):
			str = str.split(' ', 1)[1]
	root.right = rightN
	#/Pierwszy Node
	
	while(str.split(' ', 1)[0] != str):
		op = str.split(' ', 1)[0]
		str = str.split(' ', 1)[1]
		
		#sprawdzanie (
		if(str.split(' ', 1)[0] == '('):
			(isolated, rest) = bracketSplit(str.split(' ', 1)[1])
			rightN = convToTree(isolated)
			str = rest
		else:
			rightN = Node(str.split(' ', 1)[0])
			if(str.split(' ', 1)[0] != str):
				str = str.split(' ', 1)[1]
		#/sprawdzanie (
		
		#wrzucenie do drzewa
		
		if(op == '+' or op == '-'):
			root = Node(op, root, rightN)
		else:
			root.right = Node(op, root.right, rightN)
		#/wrzucanie do drzewa
		
	return root
#bierze string bez pierwszego "( " i zwraca parę ('[odizolowany string bez głównej pary "()"]','[reszte stringa]')
def bracketSplit(str):
	
	isoBrackets = ''
	bracketCounter = 1
	while(bracketCounter>0):
		if(str.split(' ', 1)[0] == '('):
			bracketCounter += 1
			isoBrackets += ' ('
		elif(str.split(' ', 1)[0] == ')'):
			bracketCounter -= 1
			if(bracketCounter>0):
				isoBrackets += (' ' + str.split(' ', 1)[0])
		else:
			isoBrackets += (' ' + str.split(' ', 1)[0])
		
		
		if(len(str) == 1): #na wypadek jakby nawias konczył wyrażenie
			str = ''
		else:
			str = str.split(' ', 1)[1]
	
	return (isoBrackets.split(' ', 1)[1], str)

def testPrint(root, space):
	space = space + '  '
	print(space + root.value)
	if(root.right != None):
		testPrint(root.right, space)	
	if(root.left != None):
		testPrint(root.left, space)
	
def calc(node):
	if(node.right == None or node.left == None):
		return float(node.value)
	else:
		if(node.value == '+'):
			return calc(node.left) + calc(node.right)
		elif(node.value == '-'):
			return calc(node.left) - calc(node.right)
		elif(node.value == '*'):
			return calc(node.left) * calc(node.right)
		elif(node.value == '/'):
			return calc(node.left) / calc(node.right)

#rysowanie drzewa 
globalKeyCounter = 0
def addToDrawning(dot, node):
	global globalKeyCounter
	globalKeyCounter += 1
	myKey = globalKeyCounter
	dot.node(str(myKey), node.value)
	if(node.right != None and node.left != None):
		leftKey = addToDrawning(dot, node.left)
		rightKey = addToDrawning(dot, node.right)
		dot.edge(str(myKey), str(leftKey))
		dot.edge(str(myKey), str(rightKey))
	return myKey
def drawTree(root):
	dot = Digraph(format = 'png')
	addToDrawning(dot, root)
	dot.render('tree.gv', view = True)

print('Podaj wyrazenie do wyliczenia')
inStr = input()
tree = convToTree(inStr)
print(inStr + ' = ' + str(calc(tree)))
drawTree(tree)


#2 * ( ( 1.5 + 3 + 1 ) * 2.5 + 2 ) / ( 3 - 1 + 1 - 1 )

