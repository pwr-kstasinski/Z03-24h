import React, { useState } from 'react';
import Display from './Display'
import Keyboard from './Keyboard'
import Calc from "../Helpers/Calc"
import "./Calculator.css"

const infixOperations = ["+", "-", "/", "*", "^", "%"]
const oneArgOperations = ["!", "log", 'sqrt', 'abs', 'rev', 'log']

function Calculator(params) {
    const [dispFormula, setDispFormula] = useState("")
    const [currDisp, setCurrDisp] = useState("0")
    const [calc] = useState(Calc())
    // mówi czy w tej liczbie kropka była już użyta
    const [dotUsed, setDotUsed] = useState(false)
    const [funcUsed, setFuncUsed] = useState(false)
    const [clsBrckets, setClsBrckets] = useState(0)
    const [opnBrckets, setOpnBrckets] = useState(0)

    const handleNumberClick = num => {
        // prevent multiple dots
        if (num === ".") {
            if (dotUsed)
                return

            setDotUsed(true)
            if (currDisp === "")
                setCurrDisp("0.")
            else
                setCurrDisp(prev => prev + '.')
        }
        // prevent multiple leading zeros
        else if (num === "0" && currDisp.length == 1 && currDisp[0] == "0")
            setCurrDisp("0")
        // first digit typed
        else if (currDisp.length == 1 && currDisp[0] == "0")
            setCurrDisp(num)
        else
            setCurrDisp(prev => prev + num)
    }

    const handleFuncClick = opr => {
        const num = parseFloat(currDisp)
        // if infix operation used
        if (infixOperations.indexOf(opr) >= 0) {
            if (calc.getLastTyped() !== ")") {
                if (oneArgOperations.indexOf(calc.getLastTyped()) < 0) {
                    calc.addNumber(num)
                    setDispFormula(prev => prev + num.toString() + opr.toString())
                }
                else {
                    setDispFormula(prev => prev + opr.toString())
                }
                calc.addOperation(opr)
                setFuncUsed(true)
                setCurrDisp("0")
                setDotUsed(false)
            }
            else {
                calc.addOperation(opr)
                setFuncUsed(true)
                setDispFormula(prev => prev + opr.toString())
                setDotUsed(false)
            }
        }
        else if (oneArgOperations.indexOf(opr) >= 0) {
            console.log("LAST TYPED: " + calc.getLastTyped());
            if (infixOperations.indexOf(calc.getLastTyped()) >= 0) {
                calc.addNumber(num)
                setDispFormula(prev => prev + num.toString() + opr.toString())
            }
            else {
                setDispFormula(prev => prev + opr.toString())
            }
            calc.addOperation(opr)
            setFuncUsed(true)
            setCurrDisp("0")
            setDotUsed(false)
        }
        else {
            if (opr == "(" && typeof calc.getLastTyped() !== 'number') {
                setOpnBrckets(prev => prev + 1)
                setDispFormula(prev => prev + opr.toString())
                calc.addOperation(opr)
            }
            else if (opr == ")" && opnBrckets > clsBrckets) {
                if (oneArgOperations.indexOf(calc.getLastTyped()) < 0) {
                    calc.addNumber(num)
                    setDispFormula(prev => prev + num.toString() + opr.toString())
                }
                else {
                    setDispFormula(prev => prev + opr.toString())
                }
                setClsBrckets(prev => prev + 1)
                calc.addOperation(opr)
                setCurrDisp("0")
                setDotUsed(false)
            }
        }
    }

    // only for debug
    const handleEqualClick = () => {
        if (infixOperations.indexOf(calc.getLastTyped()) >= 0)
            calc.addNumber(parseFloat(currDisp))
        try {
            const outcome = calc.evaluate()
            console.log(outcome)
            setDispFormula("")
            setCurrDisp(outcome.toString())
        }
        catch (e) {
            console.log(e);
        }
    }

    return (
        <div className="calculator">
            <Display smallDisp={dispFormula} mianDisp={currDisp} />
            <Keyboard onFunctionClick={handleFuncClick} onNuberClick={handleNumberClick} onEqual={handleEqualClick} />
        </div>
    )
}

export default Calculator