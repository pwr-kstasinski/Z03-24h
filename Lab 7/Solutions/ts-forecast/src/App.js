import React from 'react'
import DailyForecastTile from "./Components/DayForecastTile"
import TemperatureChart from "./Components/TemperatureChart"

function App() {
  return (
    <div className="App">
      <input type="text" placeholder="nazwa miasta"></input>
      <button>Szukaj</button>
      <DailyForecastTile></DailyForecastTile>
      <TemperatureChart temperatures = {[0, 2, 3, 7, 8, 10, 12, 6, 3, -2, -4]}></TemperatureChart>
    </div>
  );
}

export default App;
