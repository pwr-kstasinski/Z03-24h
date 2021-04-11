import os
import sys
from graphviz import Digraph

class Tree:
    def __init__(self, value, left = None, right = None):
        self.value = value
        self.left = left
        self.right = right

def make_tree(exp):
    if (len(exp) == 1):
        return Tree(exp)
    leftE, rightE = exp.split(" ", 1)
    if (leftE == '('):
        inside, rightE = bracketSplit(rightE)
        leftN = make_tree(inside)
    else:
        leftN = Tree(leftE)
    
    if (rightE == ""):
        return leftN

    root = Tree(rightE[0], leftN)
    exp = rightE.split(" ", 1)[1]
    if (len(exp) == 1):
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
        if (exp[0] == '('):
            inside, exp = bracketSplit(exp[1:])
            rightN = make_tree(inside[1:])
        else:
            rightN = Tree(exp[0])
            if(exp[0] != exp):
                exp = exp.split(" ", 1)[1]
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
	if(tree.right == None or tree.left == None):
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
    return label

def drawTree(tree):
    dot = Digraph(format = 'png')
    labelTree(dot, tree)
    dot.render('tree.gv', view = True)

userInput = input()

tree = make_tree(userInput)
print(eval(tree))
drawTree(tree)