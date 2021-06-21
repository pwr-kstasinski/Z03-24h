from tkinter import *
from math import *


expression = ""

def press(num):
    global expression

    expression = expression + str(num)
    equation.set(expression)
    

def clear():
    global expression
    expression = ""
    equation.set("")


def eval(toEvaluate, op = 0, guiToDestroy = 0):
    global expression
    out, queue, result = getOutputQueueNRootNResult(toEvaluate)
    if op != 0:
        result = executeAlone(result, op)
        result = round(result, 5)
        press(str(result))
    else:
        clear()
        result = round(result, 5)
        press(str(result))
    
    if guiToDestroy != 0:
        guiToDestroy.destroy()
def enterSubEquation(op):
    gui = Tk()
 
    gui.title("SubEquation")
 

    gui.geometry("220x114")
    sub_equation = StringVar()
    expression_field = Entry(gui, textvariable=sub_equation, font=("Calibri 15"))
    expression_field.grid(padx=0, pady=0, ipadx=5, ipady=15)
    buttonSubmit = Button(gui, text=' SUBMIT ', fg='black', bg='green', command=lambda: eval(expression_field.get(), op, gui), height=3, width=18)
    buttonSubmit.grid(row=1, column=0)
    
def getOutputQueueNRootNResult(validExpression):
    output_queue = getPostfixExpressionList(validExpression)
    root = getExpressionTree(output_queue)
    #printTree(root)
    return output_queue, root, evaluate(root)

def getRoot(expr):
    output_queue = getPostfixExpressionList(expr)
    root = getExpressionTree(output_queue)
    return root

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
        if b == 0: return 0
        return a/b
    elif operator == "*":
        return a * b
    elif operator == "%":
        return a % b
    elif operator == "^":
        return pow(a, b)

def executeAlone(a, operator):
    if operator == "!":
        a = (int)(a)
        if a < 0: a = a* (-1)
        return factorial(a)
    elif operator == "@":
        if a <= 0: return 0
        return round(log10(a), 5)
    elif operator == "$":
        return round(sqrt(a), 5)
    elif operator == "|":
        if a < 0:
            return -1*a
        return a
    elif operator == "#":
        if a == 0: return 0
        return round(1/a, 5)


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


def getExpressionTree(output_queue):
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



operator_precedence = {'(': 1, '+': 2, '-': 2, '%': 3, '/': 4, '*': 4, '^': 5}

gui = Tk()
gui.title("Calculator")
gui.geometry("410x565")

equation = StringVar()
expression_field = Entry(gui, textvariable=equation, font=("Calibri 32"))
expression_field.grid(columnspan=5, padx=0, pady=0, ipadx=5, ipady=15)

buttonMul = Button(gui, text=' * ', fg='black', bg='grey', command=lambda: press("*"), height=3, width=8)
buttonMul.grid(row=1, column=0)
buttonDiv = Button(gui, text=' / ', fg='black', bg='grey', command=lambda: press("/"), height=3 , width=8)  #TOFIX
buttonDiv.grid(row=1, column=1, pady=10)
buttonAdd = Button(gui, text=' + ', fg='black', bg='grey', command=lambda: press("+"), height=3, width=8)
buttonAdd.grid(row=1, column=2)
buttonSub = Button(gui, text=' - ', fg='black', bg='grey', command=lambda: press("-"), height=3, width=8)
buttonSub.grid(row=1, column=3)
buttonOpBracket = Button(gui, text=' ( ', fg='black', bg='grey', command=lambda: press("("), height=3, width=8)
buttonOpBracket.grid(row=2, column=1)
buttonClBracket = Button(gui, text=' ) ', fg='black', bg='grey', command=lambda: press(")"), height=3 , width=8)
buttonClBracket.grid(row=2, column=2)
buttonPow = Button(gui, text=' ^ ', fg='black', bg='grey', command=lambda: press("^"), height=3, width=8) 
buttonPow.grid(row=2, column=3)
buttonFact = Button(gui, text=' x! ', fg='black', bg='grey', command=lambda: enterSubEquation("!"), height=3 , width=8) #TOFIX
buttonFact.grid(row=2, column=0)
buttonQuit = Button(gui, text=' QUIT ', fg='black', bg='red', command=lambda: gui.destroy(), height=3, width=8)
buttonQuit.grid(row=3, column=0)
buttonDel = Button(gui, text=' PRINT ', fg='black', bg='grey', command=lambda: printTree(getRoot(expression_field.get())), height=3 , width=8)  #TOFIX
buttonDel.grid(row=3, column=1, pady=10)
buttonClear = Button(gui, text=' C ', fg='black', bg='grey', command=lambda: clear(), height=3, width=8)
buttonClear.grid(row=3, column=2)
buttonLog = Button(gui, text=' log(x) ', fg='black', bg='grey', command=lambda: enterSubEquation("@"), height=3, width=8)
buttonLog.grid(row=3, column=3)
button7 = Button(gui, text=' 7 ', fg='black', bg='grey', command=lambda: press(7), height=3, width=8)
button7.grid(row=4, column=0)
button8 = Button(gui, text=' 8 ', fg='black', bg='grey', command=lambda: press(8), height=3 , width=8)
button8.grid(row=4, column=1)
button9 = Button(gui, text=' 9 ', fg='black', bg='grey', command=lambda: press(9), height=3, width=8)
button9.grid(row=4, column=2)
buttonRev = Button(gui, text=' 1/x ', fg='black', bg='grey', command=lambda: enterSubEquation("#"), height=3, width=8)
buttonRev.grid(row=4, column=3)
button4 = Button(gui, text=' 4 ', fg='black', bg='grey', command=lambda: press(4), height=3, width=8)
button4.grid(row=5, column=0)
button5 = Button(gui, text=' 5 ', fg='black', bg='grey', command=lambda: press(5), height=3 , width=8)
button5.grid(row=5, column=1)
button6 = Button(gui, text=' 6 ', fg='black', bg='grey', command=lambda: press(6), height=3, width=8)
button6.grid(row=5, column=2, pady=10)
buttonSqrt = Button(gui, text=' sqrt(x) ', fg='black', bg='grey', command=lambda: enterSubEquation("$"), height=3, width=8)  #TOFIX
buttonSqrt.grid(row=5, column=3)
button1 = Button(gui, text=' 1 ', fg='black', bg='grey', command=lambda: press(1), height=3, width=8)
button1.grid(row=6, column=0)
button2 = Button(gui, text=' 2 ', fg='black', bg='grey', command=lambda: press(2), height=3 , width=8)
button2.grid(row=6, column=1)
button3 = Button(gui, text=' 3 ', fg='black', bg='grey', command=lambda: press(3), height=3, width=8)
button3.grid(row=6, column=2)
buttonModulo = Button(gui, text=' mod(x) ', fg='black', bg='grey', command=lambda: press('%'), height=3, width=8)
buttonModulo.grid(row=6, column=3)
buttonMod = Button(gui, text=' |x| ', fg='black', bg='grey', command=lambda: enterSubEquation("|"), height=3, width=8)   #TOFIX
buttonMod.grid(row=7, column=0)
button0 = Button(gui, text=' 0 ', fg='black', bg='grey', command=lambda: press(0), height=3 , width=8)
button0.grid(row=7, column=1)
buttonDot = Button(gui, text=' . ', fg='black', bg='grey', command=lambda: press('.'), height=3, width=8)
buttonDot.grid(row=7, column=2, pady=10)
buttonEquals = Button(gui, text=' = ', fg='black', bg='green', command=lambda: eval(expression_field.get()), height=3, width=8)
buttonEquals.grid(row=7, column=3) 

gui.mainloop()
