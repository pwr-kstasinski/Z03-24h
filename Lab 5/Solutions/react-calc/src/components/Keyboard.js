import React from 'react';
import "./Keyboard.css"

function Keyboard({ onNuberClick = () => { }, onFunctionClick = () => { }, onEqual = () => { }, onClear = () => { }, clearAll = false }) {
    return (
        <div className="keyboard">
            <div className="keyboard__num-section">
                <button className="keyboard__key keyboard__key-num" onClick={() => onNuberClick("1")}>1</button>
                <button className="keyboard__key keyboard__key-num" onClick={() => onNuberClick("2")}>2</button>
                <button className="keyboard__key keyboard__key-num" onClick={() => onNuberClick("3")}>3</button>
                <button className="keyboard__key keyboard__key-num" onClick={() => onNuberClick("4")}>4</button>
                <button className="keyboard__key keyboard__key-num" onClick={() => onNuberClick("5")}>5</button>
                <button className="keyboard__key keyboard__key-num" onClick={() => onNuberClick("6")}>6</button>
                <button className="keyboard__key keyboard__key-num" onClick={() => onNuberClick("7")}>7</button>
                <button className="keyboard__key keyboard__key-num" onClick={() => onNuberClick("8")}>8</button>
                <button className="keyboard__key keyboard__key-num" onClick={() => onNuberClick("9")}>9</button>
                <button className="keyboard__key keyboard__key-num keyboard__key-zero" onClick={() => onNuberClick("0")}>0</button>
                <button className="keyboard__key keyboard__key-num" onClick={() => onNuberClick(".")}>.</button>
            </div>
            <button className="keyboard__key keyboard__key-func" onClick={() => onFunctionClick("+")}>+</button>
            <button className="keyboard__key keyboard__key-func" onClick={() => onFunctionClick("-")}>-</button>
            <button className="keyboard__key keyboard__key-func" onClick={() => onFunctionClick("*")}>*</button>
            <button className="keyboard__key keyboard__key-func" onClick={() => onFunctionClick("/")}>/</button>
            <button className="keyboard__key keyboard__key-func" onClick={() => onFunctionClick("(")}>(</button>
            <button className="keyboard__key keyboard__key-func" onClick={() => onFunctionClick(")")}>)</button>
            <button className="keyboard__key keyboard__key-func" onClick={() => onFunctionClick("^")}>^</button>
            <button className="keyboard__key keyboard__key-func" onClick={() => onFunctionClick("%")}>%</button>
            <button className="keyboard__key keyboard__key-func" onClick={() => onFunctionClick("!")}>!</button>
            <button className="keyboard__key keyboard__key-func" onClick={() => onFunctionClick("abs")}>abs</button>
            <button className="keyboard__key keyboard__key-func" onClick={() => onFunctionClick("sqrt")}>sqrt</button>
            <button className="keyboard__key keyboard__key-func" onClick={() => onFunctionClick("log")}>log10</button>
            <button className="keyboard__key keyboard__key-func" onClick={() => onFunctionClick("rev")}>rev</button>
            <button className="keyboard__key keyboard__key-func keyboard__key-clr" onClick={onClear}>{clearAll ? "C" : "CE"}</button>
            <button className="keyboard__key keyboard__key-func keyboard__key-equ" onClick={onEqual}>=</button>


        </div>
    )
}

export default Keyboard