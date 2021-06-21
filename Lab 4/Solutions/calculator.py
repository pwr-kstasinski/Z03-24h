
from bintree import Node
from sys import exit

ADD = 0
SUB = 1
MUL = 2
DIV = 3

def isNumber(argument):
    try:
        float(argument)
        return True
    except ValueError:
        return False

def whatOperator(argument):
    if argument == '+':
        return ADD
    if argument == '-':
        return SUB    
    if argument == '*':
        return MUL
    if argument == '/':
        return DIV
    
    return -1 #unknown operator

def isInputCorrect(inputString):
    
    argumentList = inputString.split()
    
    if len(argumentList) < 1:
        return False

    previousOperator = True

    for arg in argumentList:
        if previousOperator:
            if isNumber(arg):
                previousOperator = False
            else:
                return False
        else:
            if whatOperator(arg) >= 0:
                previousOperator = True
            else:
                return False
    
    if previousOperator:
        return False
    else:
        return True

def buildTree(inputStrig):

    argumentList = inputStrig.split()
    if len(argumentList) < 3:
        root = Node(float(argumentList[0]))
        return root
    
    root = Node(argumentList[1])
    root.left = Node(argumentList[0])
    root.right = Node(argumentList[2])

    previousOperator = False

    nextOperator = -1
    nextVal = -1

    for arg in argumentList[3:]:
        if previousOperator:

            nextVal = float(arg)

            previousOperator = False

            if nextOperator == "+" or nextOperator == "-":
                newRoot = Node(nextOperator,root,Node(nextVal))
                root = newRoot

            else:    
                newRight = Node(nextOperator,root.right,Node(nextVal))
                root.right = newRight

        else:

            nextOperator = arg
            previousOperator = True

    return root

def evaluateTree(root):
    operation = whatOperator(root.val)

    if operation >= 0:
        if operation == ADD:
            return evaluateTree(root.left) + evaluateTree(root.right)
        elif operation == SUB:
            return evaluateTree(root.left) - evaluateTree(root.right)
        elif operation == MUL:
            return evaluateTree(root.left) * evaluateTree(root.right)
        else:
            return evaluateTree(root.left) / evaluateTree(root.right)

    else:
        return float(root.val)

inputStrig = input("Enter the mathematical formula: ")

print(inputStrig.split())

if not isInputCorrect(inputStrig):
    print("Error in input formula. Aborting...")
    exit()

tree = buildTree(inputStrig) 
print(tree)
print("The result of operations: {}".format(evaluateTree(tree)))
