from dataclasses import dataclass


@dataclass
class Node:
    symbol: str
    left: None
    right: None

    def is_leaf(self):
        return self.left is None and self.right is None


@dataclass
class Tree:
    root: Node

    @classmethod
    def to_stack(cls, text):
        prev = ''
        stack = []
        for char in text:
            if prev.isdigit() and char.isdigit():
                stack.append(stack.pop() + char)
            else:
                stack.append(char)
            prev = char
        return stack

    def evaluate(self, node=None):
        node = node or self.root
        if node.is_leaf():
            return int(node.symbol)
        else:
            if node.symbol == '+':
                return self.evaluate(node.left) + self.evaluate(node.right)
            elif node.symbol == '-':
                return self.evaluate(node.left) - self.evaluate(node.right)
            elif node.symbol == '*':
                return self.evaluate(node.left) * self.evaluate(node.right)
            elif node.symbol == '/':
                return self.evaluate(node.left) // self.evaluate(node.right)

    @classmethod
    def build(cls, text):
        operator_stack = []
        operand_stack = []
        for char in cls.to_stack(text):
            if char.isdigit():
                operand_stack.append(Node(symbol=char, left=None, right=None))
            elif char in '+-' and len(operator_stack) > 0 and operator_stack[-1] in '*/':
                right = operand_stack.pop()
                op = operator_stack.pop()
                left = operand_stack.pop()
                operand_stack.append(Node(symbol=op, left=left, right=right))
                operator_stack.append(char)
            elif char == ')':
                while len(operator_stack) > 0 and operator_stack[-1] != '(':
                    right = operand_stack.pop()
                    op = operator_stack.pop()
                    left = operand_stack.pop()
                    operand_stack.append(Node(symbol=op, left=left, right=right))
                operator_stack.pop()
            else:
                operator_stack.append(char)
        while len(operator_stack) > 0:
            right = operand_stack.pop()
            op = operator_stack.pop()
            left = operand_stack.pop()
            operand_stack.append(Node(symbol=op, left=left, right=right))
        print(operator_stack, operand_stack)
        return cls(root=operand_stack.pop())


if __name__ == '__main__':
    tree = Tree.build('10*3+(2+2)')
    print(tree.evaluate())
