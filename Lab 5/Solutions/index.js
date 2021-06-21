const calculator_app = Vue.createApp({
    data() {
        return {
            equation: ''
        }
    },
    methods: {
        update(value) {
            if ("1234567890().+-*/^%".includes(value)) {
                this.equation += value
            } else if (value === 'C') {
                this.equation = ''
            } else if (value === '🠔') {
                this.equation = this.equation.substring(0, this.equation.length - 1)
            } else if (value === '=') {
                this.calculate()
            } else if (value === '1/x') {
                this.calculate()
                this.equation = String(1 / this.equation)
            }  else if (value === '🌴') {
                pretty_tree = ''
                tree_print(eq.tree)
                tree.tree = pretty_tree
            } else if (value === 'log') {
                this.calculate()
                this.equation = String(Math.log10(this.equation))
            } else if (value === '√') {
                this.calculate()
                this.equation = String(Math.sqrt(this.equation))
            } else if (value === '|x|') {
                if (this.equation.split(/([\(\)\^\%\+\-\*\/])/).filter((x) => x !== "").length > 2) {
                    this.calculate()
                }

                this.equation = String(Math.abs(this.equation))
            } else if (value === '!') {
                this.calculate()

                function factorial(n) {
                    return (n != 1) ? n * factorial(n - 1) : 1;
                }

                this.equation = String(factorial(this.equation))
            } else {
                console.log(value)
            }
        },
        calculate() {
            if (this.equation) {
                eq = new Equation(this.equation)
                this.equation = String(eq.result)
            }
        }
    }
})

calculator_app.component('btn', {
    props: ['val'],
    template: `
    <button class="btn" @click="update()">
      {{ val }}
    </button>`,
    methods: {
        update() {
            calc.update(this.val)
        }
    }
})

const calc = calculator_app.mount('#calculator')

tree = Vue.createApp({
    data() {
        return {
            tree: ''
        }
    }
}).mount('#tree')

class Equation {
    constructor(string) {
        this.equation = string
        this.splitted = string.split(/([\(\)\^\%\+\-\*\/])/).filter((x) => x !== "")
        this.tree = this.make_tree()
        this.result = this.calculate_result()
    }

    make_tree() {
        // ranks for proper order of operations
        const rank = {
            '^': 3,
            '%': 2,
            '/': 2,
            '*': 2,
            '+': 1,
            '-': 1,
            '(': 0,
            ')': 0
        }

        // stacks will ensure proper order of elements in the tree
        let operations = []
        let values = []

        function merge() {
            let right = values.pop()
            let left = values.pop()
            values.push({
                'left': left,
                'right': right,
                'value': operations.pop()
            })
        }

        for (let key in this.splitted) {
            let element = this.splitted[key]
            if (!isNaN(element)) {
                values.push({'value': element})
            } else if (element === '(') {
                operations.push(element)
            } else if (element === ')') {
                while (operations[operations.length - 1] !== '(') {
                    merge()
                }
                operations.pop()
            } else {
                while (operations.length > 0 && rank[operations[-1]] >= rank[element]) {
                    merge()
                }
                operations.push(element)
            }
        }

        while (operations.length > 0) {
            merge()
        }

        return values[0]
    }

    calculate_result() {

        function calculate_result_helper(tree) {
            if (!('left' in tree && 'right' in tree))
                return parseFloat(tree['value'])

            let operator = tree['value']
            let value_left = calculate_result_helper(tree['left'])
            let value_right = calculate_result_helper(tree['right'])

            if (operator === "*") {
                return value_left * value_right
            } else if (operator === "/") {
                return value_left / value_right
            } else if (operator === "+") {
                return value_left + value_right
            } else if (operator === "-") {
                return value_left - value_right
            } else if (operator === "^") {
                return Math.pow(value_left, value_right)
            } else if (operator === "%") {
                return value_left % value_right
            }
        }
        return calculate_result_helper(this.tree)
    }
}

pretty_tree = ''

function tree_print(root, space = '') {
    space = space + '    '
    pretty_tree += space + root['value'] + '\n'
    if (root['right'] != null)
        tree_print(root['right'], space)
    if (root['left'] != null)
        tree_print(root['left'], space)
}