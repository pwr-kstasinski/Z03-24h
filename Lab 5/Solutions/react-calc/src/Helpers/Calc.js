
const oneArgOperators = ['!', 'abs', 'log', 'sqrt', 'rev', 'log']
const twoArgOperations = ['+', '-', '/', '*', '^', '%']
export const operations = ['+', '-', '/', '*', '(', ')', '^', '%', '!', 'abs', 'log', 'sqrt', 'rev', 'log']

const opr_priotity = Object.freeze({
    '^': 4, 'sqrt': 4, 'abs': 4, 'log': 4, 'rev': 4, '!': 4,
    '*': 3, '/': 3, '%': 3,
    '-': 2, '+': 2,
    '(': 1, ')': 1
})

export function isOneArgOperation(opr) {
    return oneArgOperators.indexOf(opr) >= 0
}

export function isTwoArgOperation(opr) {
    return twoArgOperations.indexOf(opr) >= 0
}

let f = [];
function factorial(n) {
    if (n === 0 || n === 1)
        return 1;
    if (f[n] > 0)
        return f[n];
    return f[n] = factorial(n - 1) * n;
}

/**
 *  Słóży do oblaiczania wrowadzonych formół matematycznych
 *  Formóły są przechowywane w formie binarnego drzewa wyrażeń
 * @returns interfejs kalkulatora
 */
export default function Calc() {
    const opr_stack = []
    const val_stack = []
    let last_typed = ""

    // łączty operaje ze zdjętymi ze stosu wartościami 
    // tworzy z nich węzeł drzewa i dokłada na stos wartości
    const mergeOperationNode = (values = val_stack, operations = opr_stack) => {
        // operacja która będzie rootem dla wartości ze stosu
        const opr = operations[operations.length - 1]
        // jeśli przyjmuje jeden argument
        if (isOneArgOperation(opr)) {
            if (values.length < 1)
                throw Error("Niepoprawna składnia formuły!")
            const left = values.pop()
            values.push({
                "left": left,
                "value": operations.pop()
            })
        }
        // jeśli przyjmuje dwa argumenty
        else if (isTwoArgOperation(opr)) {
            if (values.length < 2)
                throw Error("Niepoprawna składnia formuły!")
            const right = values.pop()
            const left = values.pop()
            values.push({
                "left": left,
                "right": right,
                "value": operations.pop()
            })
        }

    }

    // służy do dodawania kolejnych liczb do formóły
    // uwaga poprawność składni nie jest sprawdzana
    const addNumber = number => {
        if (typeof number === 'number') {
            val_stack.push({ "value": number })
            last_typed = number
        }
    }

    // służy do dodwania operatorów do formóły
    // uwaga poprawność składni nie jest sprawdzana
    const addOperation = (opr) => {
        // jeśli podano nieistniejącą operację
        if (operations.indexOf(opr) === -1)
            return

        if (opr === "(")
            opr_stack.push(opr)
        else if (opr === ")") {
            while (opr_stack[opr_stack.length - 1] !== '(') {
                if (opr_stack.length <= 0)
                    throw Error("Brakujące nawiasy")
                mergeOperationNode()
            }
            opr_stack.pop()
        }
        else {
            while ((opr_stack.length > 0) && (opr_priotity[opr_stack[opr_stack.length - 1]] >= opr_priotity[opr]))
                mergeOperationNode()
            opr_stack.push(opr)
        }

        last_typed = opr
    }

    const evaluate_tree = (root) => {
        // root jest liściem, więc musi przechowywać wartość którą zwrócimy
        if (!root["left"] && !root["right"])
            return root["value"]
        // w każdym innym wypadku mamy doczynienia z operatorem
        // operaor infiksowy musim mieć obie wartości do działania
        else if (isTwoArgOperation(root["value"])) {
            const l_val = evaluate_tree(root["left"])
            const r_val = evaluate_tree(root["right"])
            console.log("YEE")
            switch (root["value"]) {
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
                    throw Error("Nieoczekiwany operator: " + root["value"])
            }
        }
        // w każdym innym waypadku mamy doczynienia z operatorami jednoargumentowymi
        // które muszą mieć tylko jeden z liści
        else {
            const val = evaluate_tree(root["left"] ? root["left"] : root["right"])
            console.log("YEE")
            switch (root["value"]) {
                case "!":
                    return factorial(val)
                case "abs":
                    return Math.abs(val)
                case "sqrt":
                    return Math.sqrt(val)
                case "log":
                    return Math.log10(val)
                case "rev":
                    return 1 / val
                default:
                    throw Error("Nieoczekiwany operator: " + root["value"])
            }
        }

    }

    // mówi ile wartości pozostanie na stosie wartości po
    // dodaniuy wszyskich operacji ze stosu
    const valuesLeftAfterEvaluation = (values = val_stack, operations = opr_stack) => {
        let vals = val_stack.length
        opr_stack.map(opr => {
            if (isTwoArgOperation(opr))
                vals -= 1
        })
        return vals
    }

    const clear = () => {
        opr_stack.splice(0, opr_stack.length)
        val_stack.splice(0, val_stack.length)
        last_typed = ""
    }

    const peekNode = () => {
        return val_stack[val_stack.length - 1]
    }

    // zwraca wartość przechowywanego drzewa wyrażeń algebraicznych
    // jeśli jest to możliwe,
    // mówi nam o tym parametr isOK jeśli jest prawdą to mamy wartość
    // jeśli false to drzewo nie może być zwartościowane
    const evaluate = () => {
        while (opr_stack.length > 0)
            mergeOperationNode()

        if (val_stack.length != 1)
            return { isOk: false }

        const outcome = evaluate_tree(val_stack[0])
        clear()

        return { isOk: true, outcome }
    }

    const getLastTyped = () => last_typed

    return { addNumber, addOperation, evaluate, clear, getLastTyped, peekNode, valuesLeftAfterEvaluation }
}