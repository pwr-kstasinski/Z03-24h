import React, { useState } from 'react';
import { Route, BrowserRouter as Router, Redirect } from 'react-router-dom'
import Login from './Layouts/Login'


function App() {
  const [username, setUsername] = useState(null)
  const [loginMessage, setLoginMessage] = useState(null)

  const handleLoginSucces = (username, loginMessage) => {
      alert("YES")
  }

  return (
    <Router>
      {username || <Redirect to="/login" />}
      <div className="App">
        <Route exact path="/login" render={() => (<Login onLoginSucces={handleLoginSucces} />)} />
      </div>
    </Router>
  );
}

export default App;
