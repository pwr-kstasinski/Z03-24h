
function Calc() {
    const opr_priotity = Object.freeze({
        '*': 3, '/': 3,
        '-': 2, '+': 2,
        '(': 1, ')': 1
    })

    const operations = ['+', '-', '/', '*', '(', ')']

    const opr_stack = []
    const val_stack = []
    let str_repr = []
    let last_typed = ""

    const getStrRepr = () => str_repr.join("")

    const mergeOperationNode = () => {
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

    const evaluate_tree = (expr_tree) => {
        if (!(expr_tree["left"] && expr_tree["right"]))
            return expr_tree["value"]

        const l_val = evaluate_tree(expr_tree["left"])
        const r_val = evaluate_tree(expr_tree["right"])

        const operator = expr_tree["value"]

        switch (operator) {
            case "+":
                return l_val + r_val
            case "-":
                return l_val - r_val
            case "*":
                return l_val * r_val
            case "/":
                return l_val / r_val
            default:
                throw Error("Nieoczekiwany operator: " + operator)
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