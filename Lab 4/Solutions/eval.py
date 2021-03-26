import sys
# https://github.com/pydot/pydot
import pydot
import webbrowser


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
    if number != "":
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

    def merge_operation_node():
        right = val_stack.pop()
        left = val_stack.pop()
        val_stack.append({
            "left": left,
            "right": right,
            "value": opr_stack.pop()
        })

    for token in tokenize_meth_expr(expr):
        # jeśli token jest licznbą
        if is_number(token):
            val_stack.append({"value": token})
        elif token == "(":
            opr_stack.append(token)
        elif token == ")":
            while opr_stack[-1] != '(':
                merge_operation_node()
            opr_stack.pop()
        else:
            while len(opr_stack) > 0 and priority[opr_stack[-1]] >= priority[token]:
                merge_operation_node()
            opr_stack.append(token)

    while len(opr_stack) > 0:
        merge_operation_node()

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


def make_graph(root):
    # obejście przekazwywanie przez wartość
    node_id = [0]
    graph = pydot.Dot('my_graph', graph_type='graph', bgcolor='white')
    generate_graph(root, graph, node_id)
    return graph


def generate_graph(root, graph, node_id):
    node = pydot.Node(str(node_id[0]), label=str(root["value"]), color='black')
    root_node_id = node_id[0]
    node_id[0] += 1
    graph.add_node(node)

    if 'left' in root:
        left_node_id = generate_graph(root['left'], graph, node_id)
        graph.add_edge(pydot.Edge(str(root_node_id),
                       str(left_node_id), color='black'))

    if 'right' in root:
        right_node_id = generate_graph(root['right'], graph, node_id)
        graph.add_edge(pydot.Edge(str(root_node_id),
                       str(right_node_id), color='blue'))

    return root_node_id


if __name__ == "__main__":
    inp = input("Podaj wyrarzenie: ")
    print(inp)
    tokenized_expr = tokenize_meth_expr(inp)
    print("tokenized: " + str(tokenized_expr))
    bt_expr = to_binary_expr_tree(tokenized_expr)
    print("Tree representation: " + str(bt_expr))
    print("value: " + str(evaluate_expr_tree(bt_expr)))
    graph = make_graph(bt_expr)
    graph.write_png("output.png")
    webbrowser.open("output.png")
