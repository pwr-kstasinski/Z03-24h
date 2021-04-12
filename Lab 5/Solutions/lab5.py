
from tkinter import *
#Drzewo
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
	dot.render('tree.gv')


#GUI
#Main window
app = Tk()
app.geometry("400x400")
app.resizable(0, 0)
app.configure(background='gray')
app.title("Calculator")

#button functions
def bt_num_click(number):
	global input_equation
	input_equation = input_equation + str(number)
	input_text.set(input_equation)
	

def bt_exp_click(exp):
	global input_equation
	if(input_equation[-1]==' '):
		input_equation = input_equation + exp + " "
	else:
		input_equation = input_equation + " " + exp + " "
	input_text.set(input_equation)

def bt_eval_click():
	global input_equation
	print(input_equation)
	tree = convToTree(input_equation)
	input_text.set(calc(tree))
	drawTree(tree)
	input_equation = ''

#input frame
input_equation = ''
input_text = StringVar() #string to display
input_frame = Frame(app, width=400, height=50, highlightbackground="black", highlightcolor="black", highlightthickness=2)
input_frame.pack(side=TOP)
input_field = Entry(input_frame, font=('arial', 18, 'bold'),
					textvariable=input_text, width=50, bg="#eee", bd=0, justify=RIGHT)
input_field.grid(row=0, column=0)
input_field.pack(ipady=10) #internal padding

#buttons frame
bt_frame = Frame(app, bd=0, bg="grey")
bt_frame.pack()

#num buttons
one = Button(bt_frame, text = "1", width = 10, height = 3, bd = 0, bg = "#fff", command = lambda: bt_num_click(1)).grid(row = 2, column = 0, padx = 1, pady = 1)
two = Button(bt_frame, text = "2", width = 10, height = 3, bd = 0, bg = "#fff", command = lambda: bt_num_click(2)).grid(row = 2, column = 1, padx = 1, pady = 1)
three = Button(bt_frame, text = "3", width = 10, height = 3, bd = 0, bg = "#fff", command = lambda: bt_num_click(3)).grid(row = 2, column = 2, padx = 1, pady = 1)
four = Button(bt_frame, text = "4", width = 10, height = 3, bd = 0, bg = "#fff", command = lambda: bt_num_click(4)).grid(row = 1, column = 0, padx = 1, pady = 1)
five = Button(bt_frame, text = "5", width = 10, height = 3, bd = 0, bg = "#fff", command = lambda: bt_num_click(5)).grid(row = 1, column = 1, padx = 1, pady = 1)
six = Button(bt_frame, text = "6", width = 10, height = 3, bd = 0, bg = "#fff", command = lambda: bt_num_click(6)).grid(row = 1, column = 2, padx = 1, pady = 1)
seven = Button(bt_frame, text = "7", width = 10, height = 3, bd = 0, bg = "#fff", command = lambda: bt_num_click(7)).grid(row = 0, column = 0, padx = 1, pady = 1)
eight = Button(bt_frame, text = "8", width = 10, height = 3, bd = 0, bg = "#fff", command = lambda: bt_num_click(8)).grid(row = 0, column = 1, padx = 1, pady = 1)
nine = Button(bt_frame, text = "9", width = 10, height = 3, bd = 0, bg = "#fff", command = lambda: bt_num_click(9)).grid(row = 0, column = 2, padx = 1, pady = 1)
zero = Button(bt_frame, text = "0", width = 10, height = 3, bd = 0, bg = "#fff", command = lambda: bt_num_click(0)).grid(row = 3, column = 1, padx = 1, pady = 1)
point = Button(bt_frame, text = ".", width = 10, height = 3, bd = 0, bg = "#fff", command = lambda: bt_num_click(".")).grid(row = 3, column = 2, padx = 1, pady = 1)
#operation buttons
plus = Button(bt_frame, text = "+", width = 10, height = 3, bd = 0, bg = "#fff", command = lambda: bt_exp_click("+")).grid(row = 0, column = 3, padx = 1, pady = 1)
minus = Button(bt_frame, text = "-", width = 10, height = 3, bd = 0, bg = "#fff", command = lambda: bt_exp_click("-")).grid(row = 0, column = 4, padx = 1, pady = 1)
multiply = Button(bt_frame, text = "*", width = 10, height = 3, bd = 0, bg = "#fff", command = lambda: bt_exp_click("*")).grid(row = 1, column = 3, padx = 1, pady = 1)
divide = Button(bt_frame, text = "/", width = 10, height = 3, bd = 0, bg = "#fff", command = lambda: bt_exp_click("/")).grid(row = 1, column = 4, padx = 1, pady = 1)
right_bracket = Button(bt_frame, text = ")", width = 10, height = 3, bd = 0, bg = "#fff", command = lambda: bt_exp_click(")")).grid(row = 2, column = 4, padx = 1, pady = 1)
left_bracket = Button(bt_frame, text = "(", width = 10, height = 3, bd = 0, bg = "#fff", command = lambda: bt_exp_click("(")).grid(row = 2, column = 3, padx = 1, pady = 1)

#ev button

ev_frame = Frame(app, bd=0, bg="grey")
ev_frame.pack(side=TOP)
equal = Button(ev_frame, text = "=", width = 50, height = 3, bd = 0, bg = "#fff", command = lambda: bt_eval_click()).pack()


app.mainloop()