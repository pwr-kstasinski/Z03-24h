import re


class Equation:
    """Calculates the result of a mathematical equation basing on a tree, where
    operators are parent nodes, and operands are leaves."""

    def __init__(self, string):
        self.equation = string
        self.splitted = self.split()
        self.tree = self.make_tree()

    def split(self):
        """Splits string equation into a list of elements (values or
        operands)."""
        elements = re.findall(re.compile('(\\d+(\.\d+)?|[^ 0-9])'),
                              self.equation)
        for idx, element in enumerate(elements):
            elements[idx] = element[0]
        return elements

    def make_tree(self):
        """Makes a binary tree from splitted equation elements."""
        # ranks of operands are used for the correct order of operations
        rank = {'/': 2, '*': 2, '+': 1, '-': 1, '(': 0, ')': 0}

        # stacks will ensure proper order of elements in the tree
        operations = []
        values = []

        def merge():
            right = values.pop()
            left = values.pop()
            values.append({'left': left, 'right': right, 'value':
                operations.pop()})

        for element in self.splitted:
            if element.replace('.', '', 1).isdigit():  # if it's a number
                values.append({'value': element})
            elif element == '(':
                operations.append(element)
            elif element == ')':
                while operations[-1] != '(':
                    merge()
                operations.pop()
            else:
                while len(operations) > 0 and rank[operations[-1]] >= \
                        rank[element]:
                    merge()
                operations.append(element)

        while len(operations) > 0:
            merge()

        return values[0]

    def print_tree(self):
        """Visualizes a binary tree."""

        def print_tree_helper(dictionary):
            # no children
            if 'right' not in dictionary.keys() and 'left' not in dictionary.keys():
                line = '%s' % dictionary['value']
                width = len(line)
                height = 1
                middle = width // 2
                return [line], width, height, middle

            # only left child
            if 'right' not in dictionary.keys():
                lines, n, p, x = print_tree_helper(dictionary['left'])
                s = '%s' % dictionary['value']
                u = len(s)
                first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
                second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
                shifted_lines = [line + u * ' ' for line in lines]
                return [first_line,
                        second_line] + shifted_lines, n + u, p + 2, n + u // 2

            # only right child
            if 'left' not in dictionary.keys():
                lines, n, p, x = print_tree_helper(dictionary['right'])
                s = '%s' % dictionary['value']
                u = len(s)
                first_line = s + x * '_' + (n - x) * ' '
                second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
                shifted_lines = [u * ' ' + line for line in lines]
                return [first_line,
                        second_line] + shifted_lines, n + u, p + 2, u // 2

            # two children
            left, n, p, x = print_tree_helper(dictionary['left'])
            right, m, q, y = print_tree_helper(dictionary['right'])
            s = '%s' % dictionary['value']
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (
                    m - y) * ' '
            second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (
                    m - y - 1) * ' '
            if p < q:
                left += [n * ' '] * (q - p)
            elif q < p:
                right += [m * ' '] * (p - q)
            zipped_lines = zip(left, right)
            lines = [first_line, second_line] + [a + u * ' ' + b for a, b in
                                                 zipped_lines]

            return lines, n + m + u, max(p, q) + 2, n + u // 2

        lines, *_ = print_tree_helper(self.tree)
        for line in lines:
            print(line)

    def calculate_result(self):
        """Returns the result of an equation basing on a tree."""

        def calculate_result_helper(tree):
            if not ('left' in tree and 'right' in tree):
                return float(tree['value'])

            operator = tree['value']
            value_left = calculate_result_helper(tree['left'])
            value_right = calculate_result_helper(tree['right'])

            if operator == "*":
                return value_left * value_right
            elif operator == "/":
                return value_left / value_right
            elif operator == "+":
                return value_left + value_right
            elif operator == "-":
                return value_left - value_right

        return calculate_result_helper(self.tree)


if __name__ == "__main__":
    equation = Equation(input("equation: "))
    print(f'splitted: {equation.splitted}')
    print(f'tree: {equation.tree}')
    equation.print_tree()
    print(f'result = {equation.calculate_result()}')
