import React from 'react';

function Keyboard({ onNuberClick = () => { }, onFunctionClick = () => { }, onClrear = () => { }, onEqual = () => { } }) {
    return (
        <div className="keyboard">
            <button className="keyboard__key" onClick={() => onNuberClick("1")}>1</button>
            <button className="keyboard__key" onClick={() => onNuberClick("2")}>2</button>
            <button className="keyboard__key" onClick={() => onNuberClick("3")}>3</button>
            <button className="keyboard__key" onClick={() => onNuberClick("4")}>4</button>
            <button className="keyboard__key" onClick={() => onNuberClick("5")}>5</button>
            <button className="keyboard__key" onClick={() => onNuberClick("6")}>6</button>
            <button className="keyboard__key" onClick={() => onNuberClick("7")}>7</button>
            <button className="keyboard__key" onClick={() => onNuberClick("8")}>8</button>
            <button className="keyboard__key" onClick={() => onNuberClick("9")}>9</button>
            <button className="keyboard__key" onClick={() => onNuberClick("0")}>0</button>
            <button className="keyboard__key" onClick={() => onNuberClick(".")}>.</button>
            <button className="keyboard__key" onClick={() => onFunctionClick("+")}>+</button>
            <button className="keyboard__key" onClick={() => onFunctionClick("-")}>-</button>
            <button className="keyboard__key" onClick={() => onFunctionClick("*")}>*</button>
            <button className="keyboard__key" onClick={() => onFunctionClick("/")}>/</button>
            <button className="keyboard__key" onClick={() => onFunctionClick("(")}>(</button>
            <button className="keyboard__key" onClick={() => onFunctionClick(")")}>)</button>
            <button className="keyboard__key" onClick={() => onFunctionClick("^")}>^</button>
            <button className="keyboard__key" onClick={() => onFunctionClick("%")}>%</button>
            <button className="keyboard__key" onClick={() => onFunctionClick("!")}>!</button>
            <button className="keyboard__key" onClick={() => onFunctionClick("abs")}>abs</button>
            <button className="keyboard__key" onClick={() => onFunctionClick("sqrt")}>sqrt</button>
            <button className="keyboard__key" onClick={() => onFunctionClick("log")}>log10</button>
            <button className="keyboard__key" onClick={() => onFunctionClick("rev")}>rev</button>
            <button className="keyboard__key" onClick={onEqual}>=</button>


        </div>
    )
}

export default Keyboard