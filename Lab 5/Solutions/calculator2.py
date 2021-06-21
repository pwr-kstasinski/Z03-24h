from bintree import Node
from sys import exit
import math
import tkinter as tk

LBr = 10
RBr = 11

ADD = 20
SUB = 21

MUL = 32
DIV = 33
MOD = 34

POW = 35

ABS = 80
INV = 81
FAC = 82
LOG = 83
SQR = 84

def isNumber(argument):
    try:
        float(argument)
        return True
    except ValueError:
        return False


def isBracket(argument):
    if argument == '(':
        return LBr
    if argument == ')':
        return RBr
    return -1  # unknown symbol


def whatOperator(argument):
    if argument == '+':
        return ADD
    if argument == '-':
        return SUB
    if argument == '*':
        return MUL
    if argument == '/':
        return DIV
    if argument == 'abs':
        return ABS
    if argument == '^':
        return POW
    if argument == "sqrt":
        return SQR
    if argument == "inv":
        return INV
    if argument == "fac":
        return FAC
    if argument == "log":
        return LOG
    if argument == "%":
        return MOD
    return -1  # unknown operator

def isBracketCorrect(argumentList):
    if len(argumentList) < 3:
        return -1

    previousOperator = True

    if argumentList[1] == ')':
        return -1

    i = 1
    while i < len(argumentList):
        if previousOperator:
            if isNumber(argumentList[i]):
                previousOperator = False
            elif isBracket(argumentList[i]) == LBr:
                new_i = isBracketCorrect(argumentList[i:])
                if new_i >= 0:
                    i = new_i + i
                    previousOperator = False
                else:
                    return -1
            else:
                return -1
        else:
            if whatOperator(argumentList[i]) >= ADD:
                if whatOperator(argumentList[i]) >= ABS:
                    pass
                else:
                    previousOperator = True
            elif isBracket(argumentList[i]) == RBr:
                return i
            else:
                return -1
        i += 1

    return -1


def isInputCorrect(inputString):
    argumentList = inputString.split()

    if len(argumentList) < 1:
        return False

    previousOperator = True

    i = 0
    while i < len(argumentList):
        if previousOperator:
            if isNumber(argumentList[i]):
                previousOperator = False
            elif isBracket(argumentList[i]) == LBr:
                new_i = isBracketCorrect(argumentList[i:])
                if new_i >= 0:
                    i = new_i + i
                    previousOperator = False
                else:
                    return False
            else:
                return False
        else:
            if whatOperator(argumentList[i]) >= ADD:
                if whatOperator(argumentList[i]) >= ABS:
                    pass
                else:
                    previousOperator = True
            elif isBracket(argumentList[i]) == RBr:
                return False
            else:
                return False
        i += 1

    if previousOperator:
        return False
    else:
        return True


def buildNodeFromBracket(argumentList):
    if argumentList[1] == '(':
        newNode, newIndex = buildNodeFromBracket(argumentList[1:])
    else:
        newIndex = 0
        newNode = Node(argumentList[1])

    newIndex += 1

    if argumentList[newIndex+1] == ')':
        return newNode, newIndex+1

    root = Node(argumentList[newIndex + 1])
    root.left = newNode

    nextOperator = root.val
    if whatOperator(root.val) >= ABS:
        previousOperator = False
    else:
        previousOperator = True

    i = 2 + newIndex
    while i < len(argumentList):
        if previousOperator:
            if isBracket(argumentList[i]) == LBr:
                newNode, newIndex = buildNodeFromBracket(argumentList[i:])
                i = i + newIndex
            else:
                newNode = Node(float(argumentList[i]))

            previousOperator = False
            if root.right is None and whatOperator(root.val) < ABS:
                root.right = newNode
            else:
                nextOperatorPriority = whatOperator(nextOperator) // 10
                currentOperatorPriority = whatOperator(root.val) // 10

                if nextOperatorPriority <= currentOperatorPriority:
                    newRoot = Node(nextOperator, root, newNode)
                    root = newRoot
                else:
                    newRight = Node(nextOperator, root.right, newNode)
                    root.right = newRight
        else:
            if whatOperator(argumentList[i]) >= ABS:
                if root.right is None:
                    newRoot = Node(argumentList[i], root, None)
                    root = newRoot
                else:
                    newRight = Node(argumentList[i], root.right, None)
                    root.right = newRight
            elif isBracket(argumentList[i]) == RBr:
                return root, i
            else:
                nextOperator = argumentList[i]
                previousOperator = True
        i += 1

    return None, -1


def buildTree(inputString):
    argumentList = inputString.split()

    if argumentList[0] == '(':
        newNode, newIndex = buildNodeFromBracket(argumentList)
    else:
        newIndex = 0
        newNode = Node(argumentList[0])

    if newIndex >= len(argumentList) - 1:
        return newNode

    root = Node(argumentList[newIndex + 1])
    root.left = newNode

    nextOperator = root.val
    if whatOperator(root.val) >= ABS:
        previousOperator = False
    else:
        previousOperator = True


    i = 2 + newIndex
    while i < len(argumentList):
        if previousOperator:

            if isBracket(argumentList[i]) == LBr:
                newNode, newIndex = buildNodeFromBracket(argumentList[i:])
                i = i + newIndex
            else:
                newNode = Node(float(argumentList[i]))

            previousOperator = False
            if root.right is None and whatOperator(root.val) < ABS:
                root.right = newNode
            else:
                nextOperatorPriority = whatOperator(nextOperator) // 10
                currentOperatorPriority = whatOperator(root.val) // 10

                if nextOperatorPriority <= currentOperatorPriority:
                    newRoot = Node(nextOperator, root, newNode)
                    root = newRoot
                else:
                    newRight = Node(nextOperator, root.right, newNode)
                    root.right = newRight
        else:
            if whatOperator(argumentList[i]) >= ABS:
                if root.right is None:
                    newRoot = Node(argumentList[i], root, None)
                    root = newRoot
                else:
                    newRight = Node(argumentList[i], root.right, None)
                    root.right = newRight
            else:
                nextOperator = argumentList[i]
                previousOperator = True
        i += 1
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
        elif operation == POW:
            return math.pow(evaluateTree(root.left), evaluateTree(root.right))
        elif operation == SQR:
            return math.sqrt(evaluateTree(root.left))
        elif operation == ABS:
            return abs(evaluateTree(root.left))
        elif operation == INV:
            return 1/evaluateTree(root.left)
        elif operation == FAC:
            return math.factorial(int(evaluateTree(root.left)))
        elif operation == LOG:
            return math.log10(evaluateTree(root.left))
        elif operation == MOD:
            return evaluateTree(root.left) % evaluateTree(root.right)
        elif operation == DIV:
            return evaluateTree(root.left) / evaluateTree(root.right)
        else:
            return None
    else:
        return float(root.val)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.argumentList = []
        self.currentNumber = "0"
        self.isDecimal = False

        self.currentOperator = ""
        self.numberOfOpenedBrackets = 0
        self.lastOperator = True

        self.inputText = tk.StringVar()
        self.inputText.set(self.argumentListToString())

        self.resulText = tk.StringVar()
        self.resulText.set("Result")

        self.createUI()

        self.updateInputDisplay()

    def argumentListToString(self):
        result = ""
        for arg in self.argumentList:
            result = result + " " + arg

        if self.lastOperator or self.currentOperator == ")":
            result = result + " " + self.currentOperator
        else:
            result = result + " " + self.currentNumber
        return result

    def updateInputDisplay(self):
        self.inputText.set(self.argumentListToString())
        return

    def toggleOnDecimal(self):
        if not self.isDecimal:
            self.isDecimal = True
            self.currentNumber = self.currentNumber + "."
            self.updateInputDisplay()

    def changeSign(self):
        if not self.lastOperator:
            try:
                if int(self.currentNumber) == 0:
                    return
            except ValueError:
                pass

            if self.currentNumber[0] == "-":
                self.currentNumber = self.currentNumber[1:]
            else:
                self.currentNumber = "-" + self.currentNumber
            self.updateInputDisplay()

    def isCurrentNumberZero(self):
        try:
            if int(self.currentNumber) == 0:
                return True
        except:
            return False

    def addNumber(self, number):
        if not whatOperator(self.currentOperator) >= ABS and not whatOperator(self.currentOperator) == RBr:
            if not self.currentOperator == "":
                self.argumentList.append(self.currentOperator)
            self.currentOperator = ""

            self.lastOperator = False

            if self.isCurrentNumberZero():
                self.currentNumber = str(number)
            else:
                self.currentNumber = self.currentNumber + str(number)
            self.updateInputDisplay()
        return

    def addOperator(self, operator):
        if self.lastOperator:
            if whatOperator(self.currentOperator) >= ADD:
                if whatOperator(self.currentOperator) >= ABS:
                    self.argumentList.append(self.currentOperator)
                self.currentOperator = operator
        else:
            if self.currentOperator == ")":
                self.argumentList.append(self.currentOperator)
            else:
                self.argumentList.append(self.currentNumber)
            self.lastOperator = True
            self.currentNumber = "0"
            self.isDecimal = False
            self.currentOperator = operator
        self.updateInputDisplay()
        return

    def addLeftBracket(self):
        if (self.lastOperator or self.currentOperator == "(") and whatOperator(self.currentOperator) < ABS:
            self.argumentList.append(self.currentOperator)
            self.currentOperator = "("
            self.numberOfOpenedBrackets += 1
            self.lastOperator = True
            self.updateInputDisplay()

        return

    def addRightBracet(self):
        if self.numberOfOpenedBrackets > 0:
            if not self.lastOperator:
                if not self.isCurrentNumberZero():
                    self.argumentList.append(self.currentNumber)
                self.currentNumber = "0"
                self.isDecimal = False
                if self.currentOperator == ")":
                    self.argumentList.append(")")
                self.currentOperator = ")"
                self.numberOfOpenedBrackets -= 1
                self.updateInputDisplay()
        return

    def resetInput(self):
        self.argumentList = []
        self.currentNumber = "0"
        self.isDecimal = False

        self.currentOperator = ""
        self.numberOfOpenedBrackets = 0
        self.lastOperator = True

        self.inputText.set(self.argumentListToString())

        self.updateInputDisplay()

    def calculateInput(self):

        argString = self.argumentListToString()

        print(argString.split())

        if not isInputCorrect(self.argumentListToString()):
            self.resulText.set("Error")
        else:
            tree = buildTree(self.argumentListToString())
            print(tree)
            self.resulText.set(evaluateTree(tree))
        self.resetInput()

    def createUI(self):
        self.master.title("Calculator")

        self.labelResult = tk.Label(self, textvariable=self.resulText)
        self.labelResult.grid(row=0, columnspan=3, sticky = tk.W+tk.E)

        self.btnEnter = tk.Button(self, text="Enter", command = self.calculateInput)
        self.btnEnter.grid(row = 0, column = 3, sticky = tk.W+tk.E)

        self.labelInput = tk.Label(self, textvariable=self.inputText)
        self.labelInput.grid(row=1, columnspan=4, sticky = tk.W+tk.E)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.btnModulo = tk.Button(self, text="%", command = lambda: self.addOperator("%"))
        self.btnModulo.grid(row = 2, column = 0, sticky = tk.W+tk.E)

        self.btnRev = tk.Button(self, text="1/X", command = lambda: self.addOperator("inv"))
        self.btnRev.grid(row = 2, column = 1, sticky = tk.W+tk.E)

        self.btnLog = tk.Button(self, text="Log X", command = lambda: self.addOperator("log"))
        self.btnLog.grid(row = 2, column = 2, sticky = tk.W+tk.E)

        self.btnDel = tk.Button(self, text="Del", command = self.resetInput)
        self.btnDel.grid(row = 2, column = 3, sticky = tk.W+tk.E)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.btnPow = tk.Button(self, text="X^Y", command = lambda: self.addOperator("^"))
        self.btnPow.grid(row = 3, column = 0, sticky = tk.W+tk.E)

        self.btnFac = tk.Button(self, text="X!", command = lambda: self.addOperator("!"))
        self.btnFac.grid(row = 3, column = 1, sticky = tk.W+tk.E)

        self.btnSqrt = tk.Button(self, text="sqrt X", command = lambda: self.addOperator("sqrt"))
        self.btnSqrt.grid(row = 3, column = 2, sticky = tk.W+tk.E)

        self.btnAbs = tk.Button(self, text="abs X", command = lambda: self.addOperator("abs"))
        self.btnAbs.grid(row = 3, column = 3, sticky = tk.W+tk.E)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.btnLBr = tk.Button(self, text="(", command = self.addLeftBracket)
        self.btnLBr.grid(row = 4, column = 0, columnspan=2, sticky = tk.W+tk.E)

        self.btnRBr = tk.Button(self, text=")", command = self.addRightBracet)
        self.btnRBr.grid(row = 4, column = 2, columnspan=2, sticky = tk.W+tk.E)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.btn7 = tk.Button(self, text="7", command= lambda: self.addNumber(7))
        self.btn7.grid(row = 5, column = 0, sticky = tk.W+tk.E)

        self.btn8 = tk.Button(self, text="8", command= lambda: self.addNumber(8))
        self.btn8.grid(row = 5, column = 1, sticky = tk.W+tk.E)

        self.btn9 = tk.Button(self, text="9", command= lambda: self.addNumber(9))
        self.btn9.grid(row = 5, column = 2, sticky = tk.W+tk.E)

        self.btnDiv = tk.Button(self, text="/", command = lambda: self.addOperator("/"))
        self.btnDiv.grid(row = 5, column = 3, sticky = tk.W+tk.E)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.btn4 = tk.Button(self, text="4", command= lambda: self.addNumber(4))
        self.btn4.grid(row = 6, column = 0, sticky = tk.W+tk.E)

        self.btn5 = tk.Button(self, text="5", command= lambda: self.addNumber(5))
        self.btn5.grid(row = 6, column = 1, sticky = tk.W+tk.E)

        self.btn6 = tk.Button(self, text="6", command= lambda: self.addNumber(6))
        self.btn6.grid(row = 6, column = 2, sticky = tk.W+tk.E)

        self.btnMul = tk.Button(self, text="*", command = lambda: self.addOperator("*"))
        self.btnMul.grid(row = 6, column = 3, sticky = tk.W+tk.E)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.btn1 = tk.Button(self, text="1", command= lambda: self.addNumber(1))
        self.btn1.grid(row = 7, column = 0, sticky = tk.W+tk.E)

        self.btn2 = tk.Button(self, text="2", command= lambda: self.addNumber(2))
        self.btn2.grid(row = 7, column = 1, sticky = tk.W+tk.E)

        self.btn3 = tk.Button(self, text="3", command= lambda: self.addNumber(3))
        self.btn3.grid(row = 7, column = 2, sticky = tk.W+tk.E)

        self.btnSub = tk.Button(self, text="-", command = lambda: self.addOperator("-"))
        self.btnSub.grid(row = 7, column = 3, sticky = tk.W+tk.E)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.btnSign = tk.Button(self, text="+/-", command = self.changeSign)
        self.btnSign.grid(row = 8, column = 0, sticky = tk.W+tk.E)

        self.btn0 = tk.Button(self, text="0", command= lambda: self.addNumber(0))
        self.btn0.grid(row = 8, column = 1, sticky = tk.W+tk.E)

        self.btnComa = tk.Button(self, text=",", command=self.toggleOnDecimal)
        self.btnComa.grid(row = 8, column = 2, sticky = tk.W+tk.E)

        self.btnAdd = tk.Button(self, text="+", command = lambda: self.addOperator("+"))
        self.btnAdd.grid(row = 8, column = 3, sticky = tk.W+tk.E)


inputString = input("Enter the mathematical formula: ")

print(inputString.split())

if not isInputCorrect(inputString):
    print("Error in input formula. Aborting...")
    exit()

tree = buildTree(inputString)
print(tree)
print("The result of operations: {}".format(evaluateTree(tree)))


root = tk.Tk()
app = Application(master=root)
app.mainloop()

#['59', '*', '8', '/', '(', '3', ')']