from graphviz import Digraph


class Node:
    def __init__(self, value, left = None, right = None):
        self.value = value
        self.leftNode = right
        self.rightNode = left


OPERATORS = ['+', '-', '*', '/']


def RPN(exp: [str]):
    stack = []

    res = []

    for el in exp:
        if el == '=':
            while len(stack) > 0:
                res.append(stack.pop())
        else:
            if el == '(':
                stack.append('(')
            elif el == ')':
                while stack[-1] != '(':
                    res.append(stack.pop())
                stack.pop()
            elif OPERATORS.__contains__(el):
                while len(stack) > 1:
                    if priority(el) == 3 or (priority(el) > priority(stack[-1])):
                        break
                    res.append(stack.pop())
                stack.append(el)
            else:
                res.append(el)
    return res


def prepareTree(exp: [str]):
    nodes: [Node] = []
    for el in exp:
        if OPERATORS.__contains__(el):
            node = Node(el, nodes.pop(), nodes.pop())
            nodes.append(node)
        else:
            nodes.append(Node(el))
    return nodes[0]


def priority(operator):
    if operator == '+' or operator == '-':
        return 1
    if operator == '*' or operator == '/':
        return 2
    return 0


def genTreeToVisualize(tree, dot=None):
    # Create Digraph object
    if dot is None:
        dot = Digraph()
        dot.node(name=str(tree), label=str(tree.value))

    # Add nodes
    if tree.leftNode:
        dot.node(name=str(tree.leftNode), label=str(tree.leftNode.value))
        dot.edge(str(tree), str(tree.leftNode))
        dot = genTreeToVisualize(tree.leftNode, dot=dot)

    if tree.rightNode:
        dot.node(name=str(tree.rightNode), label=str(tree.rightNode.value))
        dot.edge(str(tree), str(tree.rightNode))
        dot = genTreeToVisualize(tree.rightNode, dot=dot)

    return dot


def calculateExpression(tree: Node):
    if tree.leftNode is None and tree.rightNode is None:
        return float(tree.value)
    else:
        return calcNode(calculateExpression(tree.leftNode), calculateExpression(tree.rightNode), tree.value)


def calcNode(val1: float, val2: float, operator: chr):
    if operator == '+':
        return val1 + val2
    elif operator == '-':
        return val1 - val2
    elif operator == '*':
        return val1 * val2
    return val1 / val2


def main():
    exp = input("Podaj wyrażenie(znaki oddziel spacjami): ")
    if not exp.__contains__(' '):
        print("Proszę nie utrudniać i podać wyrażenie ze spacjami pomiędzy znakami")
        return
    splittedExpression = RPN(exp.split(' '))
    tree = prepareTree(splittedExpression)
    print(calculateExpression(tree))
    graph = genTreeToVisualize(tree)
    graph.format = 'png'
    graph.view(filename='digraph', directory='./')


if __name__ == "__main__":
    main()
