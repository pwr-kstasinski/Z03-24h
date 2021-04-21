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
  return fetch(`https://api.weatherbit.io/v2.0/forecast/hourly?city=${city}&country=${country}&key=${keys.API_KEY_2}`)
}

const weekDays = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]

const status = Object.freeze({ OK: 1, NOT_FOUND: 2, LOADING: 3, ERROR: 4 })

function App() {
  const [cityName, setCityname] = useState("Wrocław")
  const [currentStatus, setCurrentStatus] = useState(status.LOADING) // powinno być oddzielnie dla każdecho fetcha !!!
  const [dailyData, setDailyData] = useState(null)
  const [selectedTile, setSelectedTile] = useState(0)
  const [hourlyData, sethourlyData] = useState(null)
  const [chartData, setChartData] = useState(null)
  const textFieldRef = useRef(null)

  const handleBtnClick = e => {
    setCurrentStatus(status.LOADING)
    setCityname(textFieldRef.current.value)
  }

  const handleTileClick = (date, tileID) => {
    if (!hourlyData)
      return
    setSelectedTile(tileID)
    const _date = new Date(date.split(':')[0])
    const temperatures = hourlyData.filter(data => {
      const { timestamp_utc } = data
      const _date2 = new Date(timestamp_utc.split('T')[0])
      return _date.getTime() == _date2.getTime()
    }).map(data => data.temp)
    setChartData(temperatures)
  }

  useEffect(() => {
    getDaily(cityName, "", 3)
      .then(response => {
        if (response.status === 200) {
          setCurrentStatus(status.OK)
          return response.json()
        }
        if (response.status === 204)
          setCurrentStatus(status.NOT_FOUND)
        else
          setCurrentStatus(status.ERROR)
      })
      .then(data => {
        if (data) {
          if (data.city_name != cityName)
            setCityname(data.city_name)
        }
        setDailyData(data)
      })

    getHourly(cityName, "")
      .then(response => {
        if (response.status === 200) {
          setCurrentStatus(status.OK)
          return response.json()
        }
        if (response.status === 204)
          setCurrentStatus(status.NOT_FOUND)
        else
          setCurrentStatus(status.ERROR)
      })
      .then(data => {
        if (data)
          sethourlyData(data.data)
      })


  }, [cityName])

  const weather_tiles = []

  // generate tiles for evry foracast day
  if (currentStatus == status.OK && dailyData) {
    let first_elem = true
    let tileIndex = 0
    const tiles = dailyData.data.map(data => {
      const { min_temp, max_temp, valid_date, pop, weather } = data
      const style = (tileIndex == selectedTile) ? { fontWeight: "bold", boxShadow: "0 0 2px 2px" } : {}
      const tile = (<DailyForecastTile
        onClick={((tileIndex) => handleTileClick(valid_date, tileIndex)).bind(null, tileIndex)}
        dayLabel={first_elem ? "Today" : weekDays[new Date(valid_date).getDay() - 1]}
        dayTemp={max_temp}
        nightTemp={min_temp}
        rainLbl={pop + "%"}
        iconUrl={`https://www.weatherbit.io/static/img/icons/${weather.icon}.png`}
        style={style}
      />)
      tileIndex++
      first_elem = false
      return tile
    })
    weather_tiles.push(...tiles)
  }


  return (
    <div className="App">
      <div>
        <input type="text" placeholder="nazwa miasta" ref={textFieldRef}></input>
        <button onClick={handleBtnClick}>Szukaj</button>
      </div>
      <h2>Dzisiejsza prognoza dla {cityName}:</h2>
      {currentStatus == status.NOT_FOUND && <label style={{ color: "red", fontSize: "30px", fontWeight: "bold" }}>Nie odnaleziono mista</label>}
      {currentStatus == status.LOADING && <label style={{ fontSize: "30px", fontWeight: "bold" }}>Ładuję...</label>}
      <div className="tiles-container">
        {weather_tiles}
      </div>
      {chartData && currentStatus == status.OK && <TemperatureChart temperatures={chartData}></TemperatureChart>}
    </div >
  );
}

export default App;
