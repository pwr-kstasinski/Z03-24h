import React from 'react';
import "./Display.css"

function Display({ smallDisp = "", mianDisp = "" }) {
    return (
        <div className="display">
            <div className="display__small">{smallDisp}</div>
            <div className="display__main">{mianDisp}</div>
        </div>
    )
}

export default Display