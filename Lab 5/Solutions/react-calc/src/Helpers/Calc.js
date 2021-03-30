var f = [];
function factorial(n) {
    if (n == 0 || n == 1)
        return 1;
    if (f[n] > 0)
        return f[n];
    return f[n] = factorial(n - 1) * n;
}

function Calc() {
    const opr_priotity = Object.freeze({
        '^': 4, 'sqrt': 4, 'abs': 4, 'log': 4, 'rev':4,
        '*': 3, '/': 3, '%': 3,
        '-': 2, '+': 2,
        '(': 1, ')': 1
    })

    const operations = ['+', '-', '/', '*', '(', ')', '^', '%', '!', 'abs', 'log', 'sqrt', 'rev', 'log']
    const oneArgOperators = ['!', 'abs', 'log', 'sqrt','rev','log']
    const opr_stack = []
    const val_stack = []
    let str_repr = []
    let last_typed = ""

    const getStrRepr = () => str_repr.join("")

    const mergeOperationNode = () => {
        if (oneArgOperators.indexOf(opr_stack[opr_stack.length - 1]) >= 0) {
            const left = val_stack.pop()
            val_stack.push({
                "left": left,
                "value": opr_stack.pop()
            })
        }
        else {
            if (val_stack.length < 2)
                throw Error("Niepoprawna składnia formuły!")
            const right = val_stack.pop()
            const left = val_stack.pop()
            val_stack.push({
                "left": left,
                "right": right,
                "value": opr_stack.pop()
            })
        }

    }

    const addNumber = number => {
        console.log(number);
        if (typeof number === 'number') {
            val_stack.push({ "value": number })
            str_repr.push(number)
            last_typed = number
        }
        console.log(val_stack);
    }

    const addOperation = (opr) => {
        console.log("OPR: " + opr);
        if (operations.indexOf(opr) === -1)
            return

        if (opr === "(")
            opr_stack.push(opr)
        else if (opr === ")") {
            while (opr_stack[opr_stack.length - 1] !== '(')
                mergeOperationNode()
            opr_stack.pop()
        }
        else {
            while ((opr_stack.length > 0) && (opr_priotity[opr_stack[opr_stack.length - 1]] >= opr_priotity[opr]))
                mergeOperationNode()
            opr_stack.push(opr)
        }

        str_repr.push(opr)
        last_typed = opr

        console.log("vals: ", val_stack);
        console.log("opr: ", opr_stack);
    }

    const evaluate_tree = (root) => {
        // case root is leaf
        if (!root["left"] && !root["right"])
            return root["value"]
        // case 2 arg operations
        else if (root["left"] && root["right"]) {
            const l_val = evaluate_tree(root["left"])
            const r_val = evaluate_tree(root["right"])

            const operator = root["value"]

            switch (operator) {
                case "+":
                    return l_val + r_val
                case "-":
                    return l_val - r_val
                case "*":
                    return l_val * r_val
                case "/":
                    return l_val / r_val
                case "^":
                    return Math.pow(l_val, r_val)
                case "%":
                    return l_val % r_val
                default:
                    throw Error("Nieoczekiwany operator: " + operator)
            }
        }
        // case 1 arg operations
        else {
            const val = evaluate_tree(root["left"] ? root["left"] : root["right"])

            const operator = root["value"]
            console.log("fdsafasdfdsaf");
            switch (operator) {
                case "!":
                    return factorial(val)
                case "abs":
                    return Math.abs(val)
                case "sqrt":
                    return Math.sqrt(val)
                case "log":
                    return Math.log10(val)
                case "rev":
                    return 1/val
                default:
                    throw Error("Nieoczekiwany operator: " + operator)
            }
        }

    }

    const clear = () => {
        opr_stack.splice(0, opr_stack.length)
        val_stack.splice(0, val_stack.length)
        str_repr = []
    }

    const evaluate = () => {
        console.log(val_stack);
        console.log(opr_stack);
        while (opr_stack.length > 0)
            mergeOperationNode()

        console.log("OPR: ", val_stack)
        console.log("VAL: ", val_stack)
        const outcome = evaluate_tree(val_stack[0])
        clear()

        return outcome
    }

    const getLastTyped = () => last_typed

    return { addNumber, addOperation, evaluate, clear, getLastTyped }
}

export default Calc