import React from 'react';
import './DayForecastTile.css'
import cloud_rain from '../icons/cloud-rain.svg'

export default function DayForecastTile({ styleName = "", dayLabel = "Today", dayTemp = "8", nightTemp = "5", rainChance = "10", iconUrl }) {
    return (
        <div className={`forecast-tile ${styleName}`}>
            <div className="forecast-tile__day">
                {dayLabel}
            </div>
            <div className="forecast-tile__temp-day">
                {dayTemp}°
            </div>
            <div className="forecast-tile__temp-night">
                {nightTemp}°
            </div>
            {iconUrl && <img className="forecast-tile__icon" alt="weather" />}
            <div className="forecast-tile__rain-chance">
                <img src={cloud_rain} className="forecast-tile__rain-chance-img" alt="rain clounds" />
                {rainChance}%
            </div>
        </div>
    )
}