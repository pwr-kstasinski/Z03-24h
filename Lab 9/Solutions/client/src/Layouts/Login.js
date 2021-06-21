import React, { useRef, useState } from 'react';

function login(username, password) {
    return fetch('http://localhost:5000/login', {
        method: 'POST',
        credentials: 'include',
        body: JSON.stringify({ usr_name: username, passwd: password }),
        headers: {
            'Content-Type': 'application/json'
        }

    })
}

function register(username, password) {
    return fetch('http://localhost:5000/create_account', {
        method: 'POST',
        credentials: 'include',
        body: JSON.stringify({ usr_name: username, passwd: password }),
        headers: {
            'Content-Type': 'application/json'
        }

    })
}

function Login({ onLoginSucces = (username, loginMessage) => { } }) {
    const passRef = useRef()
    const loginRef = useRef()
    const [loginMessage, setLoginMessage] = useState(null)

    const handleLogin = () => {
        const username = loginRef.current.value
        const password = passRef.current.value

        login(username, password)
            .then(response => response.json())
            .then(data => {
                if (data) {
                    if (data.status == "succes") {
                        onLoginSucces(username, data.message)
                    }
                    setLoginMessage(data.message)
                }
            })
    }

    const handleCreateAccount = () => {
        const username = loginRef.current.value
        const password = passRef.current.value

        register(username, password)
            .then(response => response.json())
            .then(data => {
                if (data) {
                    console.log(data);
                    setLoginMessage(data.message)
                }
            })
    }

    return (
        <div className="login">
            <input type="text" ref={loginRef}></input>
            <input type="text" ref={passRef}></input>
            <button onClick={handleLogin}>Zaloguj</button>
            <button onClick={handleCreateAccount}>Zarejestruj</button>
            {loginMessage}
        </div>
    )

}

export default Login