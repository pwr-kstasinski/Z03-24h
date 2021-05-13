import React, { useState } from 'react';
import { Route, BrowserRouter as Router, Redirect } from 'react-router-dom'
import Login from './Layouts/Login'
import UserPanel from './Layouts/UserPanel'


function App() {
  const [username, setUsername] = useState(null)
  const [loginMessage, setLoginMessage] = useState(null)

  const handleLoginSucces = (username, loginMessage) => {
    setUsername(username)
    setLoginMessage(loginMessage)
  }

  return (
    <Router>
      {username ? <Redirect to="/panel" /> : <Redirect to="/login" />}
      <div className="App">
        <Route exact path="/login" render={() => (<Login onLoginSucces={handleLoginSucces} />)} />
        <Route exact path="/panel" render={() => (<UserPanel username={username} />)} />
      </div>
    </Router>
  );
}

export default App;
