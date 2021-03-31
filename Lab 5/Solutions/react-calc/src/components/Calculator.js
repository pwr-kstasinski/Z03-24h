import React, { useState } from 'react';
import Display from './Display'
import Keyboard from './Keyboard'
import Calc, { isOneArgOperation, isTwoArgOperation } from "../Helpers/Calc"
import "./Calculator.css"


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
        // wartość z wyświetlacza
        const disp_num = parseFloat(currDisp)
        // jeśli urzyto operacji infiksowe, biąroącej dwa argumenty
        if (isTwoArgOperation(opr)) {
            // jeśli bedzie za mało argumentów to dodaj argument z wyświetlacza
            if (calc.valuesLeftAfterEvaluation() < 1) {
                calc.addNumber(disp_num)
                setDispFormula(prev => prev + disp_num.toString() + opr.toString())
            }
            else
                setDispFormula(prev => prev + opr.toString())

            calc.addOperation(opr)
            setFuncUsed(true)
            setCurrDisp("0")
            setDotUsed(false)
        }
        // jeśli jest to operacja jednoargumentowa
        else if (isOneArgOperation(opr)) {
            // wczytaj liczbę z wyświetlacza aby zachować spójność formóły
            if (calc.valuesLeftAfterEvaluation() < 1) {
                calc.addNumber(disp_num)
                setDispFormula(prev => prev + disp_num.toString() + opr.toString())
            }
            else {
                setDispFormula(prev => prev + opr.toString())
            }
            calc.addOperation(opr)
            setFuncUsed(true)
            setCurrDisp("0")
            setDotUsed(false)
        }
        else if (opr === "(") {
            setOpnBrckets(prev => prev + 1)
            setDispFormula(prev => prev + opr.toString())
            calc.addOperation(opr)
        }
        else if (opr == ")") {
            if (opnBrckets > clsBrckets) {
                // jeśli ostatnio urzyto operacji dwuargumantowej
                // wczytaj liczbę z wyświetlacza aby zachować spójnoiść
                if (isTwoArgOperation(calc.getLastTyped())) {
                    calc.addNumber(disp_num)
                    setDispFormula(prev => prev + disp_num.toString() + opr.toString())
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
        if (isTwoArgOperation(calc.getLastTyped()))
            calc.addNumber(parseFloat(currDisp))
        try {
            const outcome = calc.evaluate().outcome
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