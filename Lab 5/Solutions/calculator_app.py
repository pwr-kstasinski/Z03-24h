from tkinter import *
from dataclasses import dataclass

win = Tk()
win.geometry("312x324")
win.resizable(0, 0)
win.title("Calculator")
expression = ""
input_text = StringVar()
last_digits = []
num_of_digits = 0
last = ''


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
                return self.evaluate(node.left) / self.evaluate(node.right)

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


def btn_click(item, special=None):
    global expression
    global last_digits
    global last
    global num_of_digits
    if special is not None:
        if special == "inverse":
            num = last_digits[-1]
            temp = expression[:-num_of_digits]
            temp += f'(1/{num})'
            expression = temp
    else:
        expression = expression + item
    if item.isdigit() and last.isdigit():
        last_digits.append(last_digits.pop() + item)
        num_of_digits += 1
    elif item.isdigit():
        last_digits.append(item)
        num_of_digits = 1
    last = item
    input_text.set(expression)


def bt_clear():
    global expression
    expression = ""
    input_text.set("")


def bt_equal():
    global expression
    tree = Tree.build(expression)
    result = tree.evaluate()
    input_text.set(result)
    expression = ""


def create_window():
    input_frame = Frame(win, width=312, height=50, bd=0, highlightbackground="black", highlightcolor="black",
                        highlightthickness=2)
    input_frame.pack(side=TOP)

    input_field = Entry(input_frame, font=('arial', 18, 'bold'), textvariable=input_text, width=50, bg="#fff", bd=0,
                        justify=RIGHT)

    input_field.grid(row=0, column=0)
    input_field.pack(ipady=10)

    btns_frame = Frame(win, width=312, height=272.5, bg="grey")
    btns_frame.pack()

    clear = Button(btns_frame, text="C", fg="black", width=21, height=3, bd=0, bg="#eee", cursor="hand2",
                   command=bt_clear).grid(row=0, column=0, columnspan=2, padx=1, pady=1)

    parent_left = Button(btns_frame, text="(", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2",
                         command=lambda: btn_click("(")).grid(row=0, column=2, padx=1, pady=1)

    parent_right = Button(btns_frame, text=")", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2",
                          command=lambda: btn_click(")")).grid(row=0, column=3, padx=1, pady=1)

    seven = Button(btns_frame, text="7", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                   command=lambda: btn_click('7')).grid(row=1, column=0, padx=1, pady=1)

    eight = Button(btns_frame, text="8", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                   command=lambda: btn_click('8')).grid(row=1, column=1, padx=1, pady=1)

    nine = Button(btns_frame, text="9", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                  command=lambda: btn_click('9')).grid(row=1, column=2, padx=1, pady=1)

    multiply = Button(btns_frame, text="*", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2",
                      command=lambda: btn_click("*")).grid(row=1, column=3, padx=1, pady=1)

    four = Button(btns_frame, text="4", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                  command=lambda: btn_click('4')).grid(row=2, column=0, padx=1, pady=1)

    five = Button(btns_frame, text="5", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                  command=lambda: btn_click('5')).grid(row=2, column=1, padx=1, pady=1)

    six = Button(btns_frame, text="6", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                 command=lambda: btn_click('6')).grid(row=2, column=2, padx=1, pady=1)

    minus = Button(btns_frame, text="-", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2",
                   command=lambda: btn_click("-")).grid(row=2, column=3, padx=1, pady=1)

    one = Button(btns_frame, text="1", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                 command=lambda: btn_click('1')).grid(row=3, column=0, padx=1, pady=1)

    two = Button(btns_frame, text="2", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                 command=lambda: btn_click('2')).grid(row=3, column=1, padx=1, pady=1)

    three = Button(btns_frame, text="3", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                   command=lambda: btn_click('3')).grid(row=3, column=2, padx=1, pady=1)

    plus = Button(btns_frame, text="+", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2",
                  command=lambda: btn_click("+")).grid(row=3, column=3, padx=1, pady=1)

    zero = Button(btns_frame, text="0", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                  command=lambda: btn_click('0')).grid(row=4, column=0, padx=1, pady=1)

    inverse = Button(btns_frame, text="1/x", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2",
                     command=lambda: btn_click("1/x", "inverse")).grid(row=4, column=1, padx=1, pady=1)

    divide = Button(btns_frame, text="/", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2",
                    command=lambda: btn_click("/")).grid(row=4, column=2, padx=1, pady=1)

    equals = Button(btns_frame, text="=", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2",
                    command=bt_equal).grid(row=4, column=3, padx=1, pady=1)


if __name__ == '__main__':
    create_window()
    win.mainloop()
