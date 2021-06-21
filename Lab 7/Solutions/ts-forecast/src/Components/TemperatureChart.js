import React from 'react';
import TempBar from './TemperatureBar'
import './TemperetureChart.css'

export default function TemperatureChart({ temperatures = [0, 2, 3] }) {
    let max_temp = Math.max(...temperatures)
    let min_temp = Math.min(...temperatures)
    const range = max_temp - min_temp
    const elem_width = 100 / temperatures.length

    const bars = temperatures.map(temp => {
        const height = Math.max(((temp - min_temp) / range) * 100, 20)
        return (
            <TempBar temperature={temp} style={{ width: `${elem_width}%`, height: `${height}%`, margin: "2px" }} />
        )
    })
    return (
        <div className="temp-chart">
            {bars}
        </div>
    )
}