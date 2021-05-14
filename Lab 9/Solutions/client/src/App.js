import React, { useState } from 'react';
import { Route, BrowserRouter as Router, Redirect } from 'react-router-dom'
import Login from './Layouts/Login'
import UserPanel from './Layouts/UserPanel'

function logut() {
  return fetch("http://localhost:5000/logout", { credentials: 'include' })
}


function App() {
  const [username, setUsername] = useState(localStorage.getItem("username"))
  const [loginMessage, setLoginMessage] = useState(null)

  const handleLoginSucces = (username, loginMessage) => {
    localStorage.setItem("username", username)
    setUsername(username)
    setLoginMessage(loginMessage)
  }


  const handleLogout = () => {
    logut()
    localStorage.removeItem("username")
    setUsername("")
  }

  return (
    <Router>
      {username ? <Redirect to="/panel" /> : <Redirect to="/login" />}
      <div className="App">
        <Route exact path="/login" render={() => (<Login onLoginSucces={handleLoginSucces} />)} />
        <Route exact path="/panel" render={() => (<UserPanel username={username} onLogout={handleLogout} />)} />
      </div>
    </Router>
  );
}

export default App;
