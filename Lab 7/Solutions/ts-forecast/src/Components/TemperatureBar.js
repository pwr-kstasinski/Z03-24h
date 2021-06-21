import React from 'react';
import './TemperatureBar.css'

export default function TemperatureBar({ temperature = 3, style }) {
    const hue = temperature > 0 ? Math.abs(-temperature + 45) % 360 : Math.abs(temperature - 180) % 360
    const color = `hsl(${hue}, 100%, 50%)`
    return (
        <div className="temp-bar" style={{ backgroundColor: color, ...style }}>
            <label className="temp-bar__label">
                {temperature}°
            </label>
        </div>
    )
}