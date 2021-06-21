class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right



def printTree(node, level=0):
    if node != None:
        printTree(node.left, level + 1)
        print(' ' * 10 * level + '->', node.data)
        printTree(node.right, level + 1)
def isLeaf(node):
    return node.left is None and node.right is None
def evaluate(node):
    if node is None:
        return 0

    if isLeaf(node):
        return float(node.data)
 
    x = evaluate(node.left)
    y = evaluate(node.right)
 
    return execute(x, y, node.data)

def execute(a, b, operator):
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "/":
        return a/b
    elif operator =="*":
        return a * b



def getPostfixExpressionList(expression):
    expression = expression.replace(" ", "")
    output_queue= []
    operator_stack = Stack()
    tmp_number = ""
    lastNum = False

    for element in expression:
        if element.isdigit() or element == "." or (lastNum == False and element == "-") :
            if lastNum:
                tmp_number = output_queue.pop()
            else:
                tmp_number = ""
            tmp_number += element
            output_queue.append(tmp_number)
            lastNum = True
        elif element == "(":
            operator_stack.push(element)
            lastNum = False
        elif element == ")":
            while operator_stack.peek() != "(":
                output_queue.append(operator_stack.pop())
            operator_stack.pop() 
        else:
            while not operator_stack.isEmpty() and operator_precedence[operator_stack.peek()] >= operator_precedence[element]:
                output_queue.append(operator_stack.pop())
            operator_stack.push(element)
            lastNum = False

    while not operator_stack.isEmpty():
        output_queue.append(operator_stack.pop())
    return output_queue


def getExpressionTree(postfixExpressionList):
    new_stack = Stack()   
    for element in output_queue:
        if element in operator_precedence:
            x = new_stack.pop()
            y = new_stack.pop()
            node = Node(element,y,x)
            new_stack.push(node)
        else:
            new_stack.push(Node(element))
    return new_stack.pop()



operator_precedence = {'(': 1, '+': 2, '-': 2, '/': 3, '*': 3}

expression = input("Podaj wyrazenie do obliczenia: ")

output_queue = getPostfixExpressionList(expression)
#print(output_queue)

root = getExpressionTree(output_queue)
printTree(root)
print(evaluate(root))
