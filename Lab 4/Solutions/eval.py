import sys


def is_number(s):
    """ Returns True is string is a number. """
    try:
        float(s)
        return True
    except ValueError:
        return False


"""
Dzieli podany ciąg znaków na tablicę liczb i operatorów
Za operator pwszyjmuje się każdy znak nie będący składową liczb
"""


def tokenize_meth_expr(expr: str) -> list[str]:
    # elementy konstrułujące liczby
    num_fragments = "0123456789."
    # tablica wynikowa
    tokenized = []
    # tymczasowe miejsce na liczbę
    number = ""

    for token in expr:

        # dopóki trafiamy na elementy liczby składamy ją w całość
        # do zmiennej number
        if token in num_fragments:
            number += token

        # trafiamy na jakiś operator
        else:
            if number != "":
                tokenized.append(number)
                number = ""
            if not token.isspace():
                tokenized.append(token)

    # ostatnia liczba
    if number != 0:
        tokenized.append(number)

    return tokenized


def to_binary_expr_tree(expr: str):

    # pryjorytety operacji
    priority = {
        '*': 3, '/': 3,
        '-': 2, '+': 2,
        '(': 1, ')': 1
    }

    # stos operacji "na póżniej"
    opr_stack = []

    val_stack = []

    for token in tokenize_meth_expr(expr):
        # jeśli token jest licznbą
        if is_number(token):
            val_stack.append({"value": token})
        elif token == "(":
            opr_stack.append(token)
        elif token == ")":
            while opr_stack[-1] != '(':
                val_stack.append(opr_stack.pop())
            opr_stack.pop()
        else:
            while len(opr_stack) > 0 and priority[opr_stack[-1]] >= priority[token]:
                # onp.append(opr_stack.pop())
                left = val_stack.pop()
                right = val_stack.pop()
                val_stack.append({
                    "left": left,
                    "right": right,
                    "value": opr_stack.pop()
                })
            opr_stack.append(token)

    while len(opr_stack) > 0:
        left = val_stack.pop()
        right = val_stack.pop()
        val_stack.append({
            "left": left,
            "right": right,
            "value": opr_stack.pop()
        })

    return val_stack[0]


def evaluate_expr_tree(expr_tree):
    if not ("left" in expr_tree and "right" in expr_tree):
        return float(expr_tree["value"])

    operator = expr_tree["value"]
    l_val = evaluate_expr_tree(expr_tree["left"])
    r_val = evaluate_expr_tree(expr_tree["right"])

    if operator == "+":
        return l_val + r_val
    elif operator == "-":
        return l_val - r_val
    elif operator == "*":
        return l_val * r_val
    elif operator == "/":
        return l_val / r_val


if __name__ == "__main__":
    inp = input("Podaj wyrarzenie: ")
    print(inp)
    tokenized_expr = tokenize_meth_expr(inp)
    print("tokenized" + str(tokenized_expr))
    bt_expr = to_binary_expr_tree(tokenized_expr)
    print("Tree representation: " + str(bt_expr))
    print("value: " + str(evaluate_expr_tree(bt_expr)))
