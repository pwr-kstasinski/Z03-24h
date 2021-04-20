import React, { useEffect, useRef, useState } from 'react'
import DailyForecastTile from "./Components/DayForecastTile"
import TemperatureChart from "./Components/TemperatureChart"
import keys from './keys'
import './App.css'

function getToday(city, country) {
  return fetch(`https://api.weatherbit.io/v2.0/current?city=${city}&country=${country}&key=${keys.API_KEY_2}`)
}

function getDaily(city, country, days) {
  return fetch(`https://api.weatherbit.io/v2.0/forecast/daily?city=${city}&country=${country}&days=${days}&key=${keys.API_KEY_2}`)
}

function getHourly(city, country) {
  return fetch(`https://api.weatherbit.io/v2.0/forecast/hourly?city=${city}&country=${country}=PL&key=${keys.API_KEY_2}`)
}

const weekDays = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]

function App() {
  const [cityName, setCityname] = useState("Wrocław")
  const [dailyData, setDailyData] = useState(null)
  const [todayData, setTodayData] = useState(null)
  const [hourlyData, sethourlyData] = useState(null)
  const textFieldRef = useRef(null)

  const handleBtnClick = e => {
   
  }

  useEffect(() => {
    getToday(cityName, "", 2)
      .then(response => response.ok ? response.json() : false)
      .then(data => setTodayData(data))
      .catch(e => alert("coś poszło nie tak"))

    getDaily(cityName, "", 2)
      .then(response => {
        if (response.ok)
          return response.json()
        else throw new Error(response.status)
      })
      .then(data => setDailyData(data))
      .catch(e => alert("coś poszło nie tak"))

    getHourly(cityName, "PL")
      .then(response => response => {
        if (response.ok)
          return response.json()
        else throw new Error(response.status)
      })
      .catch(e => alert("coś poszło nie tak"))


  }, [cityName])


  // generate first day tile
  const weather_tiles = []
  if (todayData) {
    const { min_temp, max_temp, pop, weather } = todayData.data[0]
    weather_tiles.push(<DailyForecastTile
      dayLabel="Dzisiaj"
      dayTemp={max_temp}
      nightTemp={min_temp}
      rainChance={pop}
      iconUrl={`https://www.weatherbit.io/static/img/icons/${weather.icon}.png`}
      style={{ "font-weight": "bold" }}
    />)
  }

  // generate tiles for evry foracast day
  if (dailyData) {
    const tiles = dailyData.data.map(data => {
      const { min_temp, max_temp, datetime, pop, weather } = data
      return (<DailyForecastTile
        dayLabel={weekDays[new Date(datetime).getDay()]}
        dayTemp={max_temp}
        nightTemp={min_temp}
        rainChance={pop}
        iconUrl={`https://www.weatherbit.io/static/img/icons/${weather.icon}.png`}
      />)
    })
    weather_tiles.push(...tiles)
  }


  return (
    <div className="App">
      <input type="text" placeholder="nazwa miasta" ref={textFieldRef}></input>
      <button onClick={handleBtnClick}>Szukaj</button>
      <h2>Dzisiejsza prognoza dla {cityName}:</h2>
      <div className="tiles-container">
        {weather_tiles}
      </div>
      <TemperatureChart temperatures={[0, 2, 3, 7, 8, 10, 12, 6, 3, -2, -4]}></TemperatureChart>
    </div>
  );
}

export default App;
