import React from 'react';
import './DayForecastTile.css'
import cloud_rain from '../icons/cloud-rain.svg'

export default function DayForecastTile({ styleName = "", dayLabel = "Today", dayTemp = "8", nightTemp = "5", rainLbl = "10", iconUrl, style, onClick }) {
    return (
        <div className={`forecast-tile ${styleName}`} style={style} onClick={onClick}>
            <div className="forecast-tile__day">
                {dayLabel}
            </div>
            <div className="forecast-tile__temp-day">
                {dayTemp}{dayTemp != "" && "°"}
            </div>
            <div className="forecast-tile__temp-night">
                {nightTemp}{nightTemp != "" && "°"}
            </div>
            { iconUrl && <img src={iconUrl} className="forecast-tile__icon" alt="weather" />}
            <div className="forecast-tile__rain-chance">
                <img src={cloud_rain} className="forecast-tile__rain-chance-img" alt="rain clounds" />
                {rainLbl}
            </div>
        </div >
    )
}