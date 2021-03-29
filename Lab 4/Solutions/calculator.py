import os
import sys
from graphviz import Digraph

class Tree:
    def __init__(self):
        self.id = None
        self.left = None
        self.right = None
        self.data = None

def make_tree(exp):
    root = Tree()
    if (queue == ""):
        exit(-1)
    counter = 0
    root.data = queue[0]
    root.id = str(counter)
    dot.node(root.id,root.data)
    position = exp.index(root.data)
    organise_tree(exp[0 : position], root, 0, position, 0, counter)
    organise_tree(exp[position + 1 :], root, position + 1, len(exp), 1, counter)
    return root

def organise_tree(exp, root, index_l, index_r, side, index):
    queue = ""
    node = Tree()
    index += 1
    if (side == 0):
        root.left = node
        node.id = "l" + str(index)
    else:
        root.right = node
        node.id = "r" + str(index)

    for i in exp:
        if i in complex_operators:
            queue += i
    for i in exp:
        if i in simple_operators:
            queue += i
    if (queue != ""):
        node.data = queue[0]
        dot.node(node.id, node.data)
        dot.edge(root.id, node.id)
        position = exp.index(node.data)
        organise_tree(exp[0 : position], node, index_l, position, 0, index)
        organise_tree(exp[position + 1:], node, position + 1, index_r, 1, index)
    elif len(exp) == 1:
        if exp[0] in numbers:
            node.data = exp[0]
            dot.node(node.id, node.data)
            dot.edge(root.id, node.id)
        else:
            raise Exception(exp, "bad value")

def temp():
    

def print_tree(tree):
    print(tree.data)
    if (tree.left != None):
        print_tree(tree.left)
    if (tree.right != None):
        print_tree(tree.right)

expr = sys.argv[1:]
if (len(expr) == 0):
    exit(-1)

dot = Digraph(comment="Expression")
numbers = "0123456789"
simple_operators = "+-"
complex_operators = "*/"
queue = ""

for i in expr:
    if i in complex_operators:
        queue += i
    
for i in expr:
    if i in simple_operators:
        queue += i


print_tree(make_tree(expr))
dot.render('expr.gv', view=True)
